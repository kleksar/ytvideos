"""One transactional store for state, deduplication, claims and an audit log.

SQLite is a single-host development backend; PostgreSQL is the multi-host backend.
All state transitions lock a run. External calls happen AFTER a committed intent.
The run rows are also a durable polling outbox: dispatch never depends on an
in-memory notification surviving the process that committed an approval.
"""

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from .errors import Conflict, WorkflowError
from .util import canonical, utc_now


SCHEMA = (
    "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY)",
    "CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, request_id TEXT UNIQUE NOT NULL, "
    "channel TEXT NOT NULL, version INTEGER NOT NULL, doc TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, run_id TEXT NOT NULL, "
    "kind TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL)",
    "CREATE INDEX IF NOT EXISTS events_run_idx ON events(run_id, created_at)",
    "CREATE TABLE IF NOT EXISTS operations (key TEXT PRIMARY KEY, run_id TEXT NOT NULL, "
    "kind TEXT NOT NULL, input_hash TEXT NOT NULL, status TEXT NOT NULL, doc TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS topics (key TEXT PRIMARY KEY, channel TEXT NOT NULL, run_id TEXT NOT NULL, doc TEXT NOT NULL)",
)


class Transaction:
    def __init__(self, connection, postgres=False):
        self.connection, self.postgres = connection, postgres

    def execute(self, sql, params=()):
        return self.connection.execute(sql.replace("?", "%s") if self.postgres else sql, params)

    def get_run(self, run_id, *, lock=True):
        suffix = " FOR UPDATE" if lock and self.postgres else ""
        row = self.execute("SELECT version, doc FROM runs WHERE id=?" + suffix, (run_id,)).fetchone()
        if row is None:
            raise WorkflowError(f"run {run_id!r} does not exist; use create for a new episode")
        doc = json.loads(row[1])
        doc["version"] = row[0]
        return doc

    def save(self, run):
        previous = run["version"]
        run["version"] += 1
        cursor = self.execute("UPDATE runs SET version=?,doc=? WHERE id=? AND version=?",
                              (run["version"], canonical(run), run["id"], previous))
        if cursor.rowcount != 1:
            raise Conflict("run changed concurrently; reload before continuing")

    def event(self, event_id, run_id, kind, payload):
        serialized = canonical(payload)
        inserted = self.execute("INSERT INTO events VALUES (?,?,?,?,?) ON CONFLICT(id) DO NOTHING",
                                (event_id, run_id, kind, serialized, utc_now()))
        if inserted.rowcount == 1:
            return True
        # Unique insertion serializes concurrent delivery even across run locks.
        # READ COMMITTED sees the winner after ON CONFLICT has waited for it.
        old = self.execute("SELECT run_id,kind,payload FROM events WHERE id=?", (event_id,)).fetchone()
        if old is None or tuple(old) != (run_id, kind, serialized):
            raise Conflict("event ID was already used with different content")
        return False

    def operation(self, key):
        row = self.execute("SELECT doc FROM operations WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def put_operation(self, operation):
        values = (operation["key"], operation["run_id"], operation["kind"], operation["input_hash"],
                  operation["status"], canonical(operation))
        self.execute("INSERT INTO operations VALUES (?,?,?,?,?,?) ON CONFLICT(key) DO UPDATE SET "
                     "status=excluded.status,doc=excluded.doc", values)

    def create_operation(self, operation):
        values = (operation["key"], operation["run_id"], operation["kind"], operation["input_hash"],
                  operation["status"], canonical(operation))
        cursor = self.execute("INSERT INTO operations VALUES (?,?,?,?,?,?) ON CONFLICT(key) DO NOTHING", values)
        if cursor.rowcount != 1:
            raise Conflict("operation was concurrently reserved; reconcile its outcome")


class Store:
    def __init__(self, location):
        self.location = str(location)
        self.postgres = self.location.startswith(("postgres://", "postgresql://"))
        if not self.postgres:
            Path(self.location).parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def transaction(self):
        if self.postgres:
            try:
                import psycopg
            except ImportError as exc:
                raise WorkflowError("PostgreSQL requires: uv sync --extra postgres") from exc
            conn = psycopg.connect(self.location)
        else:
            conn = sqlite3.connect(self.location, timeout=30, isolation_level=None)
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute("PRAGMA busy_timeout=30000")
            conn.execute("BEGIN IMMEDIATE")
        try:
            yield Transaction(conn, self.postgres)
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self):
        with self.transaction() as tx:
            for statement in SCHEMA:
                tx.execute(statement)
            versions = [row[0] for row in tx.execute("SELECT version FROM schema_version").fetchall()]
            if versions and versions != [1]:
                raise WorkflowError("unsupported database schema; migrate with the owning code version")
            tx.execute("INSERT INTO schema_version VALUES (1) ON CONFLICT DO NOTHING")

    def get(self, run_id):
        with self.transaction() as tx:
            return tx.get_run(run_id, lock=False)

    def list(self):
        with self.transaction() as tx:
            return [json.loads(row[0]) for row in tx.execute("SELECT doc FROM runs ORDER BY id").fetchall()]

    def mutate(self, run_id, action, expected_version=None):
        with self.transaction() as tx:
            run = tx.get_run(run_id)
            if expected_version is not None and run["version"] != expected_version:
                raise Conflict("stale state version; reload status")
            result = action(tx, run)
            tx.save(run)
            return result

    def events(self, run_id):
        with self.transaction() as tx:
            return [{"id": r[0], "kind": r[1], "payload": json.loads(r[2]), "created_at": r[3]}
                    for r in tx.execute("SELECT id,kind,payload,created_at FROM events WHERE run_id=? "
                                        "ORDER BY created_at,id", (run_id,)).fetchall()]

    def health(self):
        with self.transaction() as tx:
            version = tx.execute("SELECT version FROM schema_version").fetchone()[0]
        return {"backend": "postgresql" if self.postgres else "sqlite", "schema": version}
