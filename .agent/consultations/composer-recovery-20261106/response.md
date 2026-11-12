# Consultation: composer recovery

URL: https://chatgpt.com/c/6aedd63a-13e4-83eb-8623-f6bc954066d0
Task: composer-recovery-design-20261106. Model: GPT-6; effort: Extra High. Exact prompt: `prompt.txt`, SHA-256 fe84382c704abe49bcef09fdae7f32f978f909d8e326db29b93cf54d9cbd34cd. The composer was empty before input and after the exact posted message was verified; PENDING and VERIFIED were recorded, and the lock was released before waiting. The finished response initially showed a loading error; the visible reload response control restored it without resending. Full response below, transcribed from the displayed page; formatting normalized.

Recommendation: Use a durable send journal, short-lived ownership leases, composer-content verification, and chat-history reconciliation. Never treat a planned Send as proof that nothing was submitted earlier.

## 1. Minimal persistent state

| Field | Purpose |
|---|---|
| conversation_id | Prevent actions in the wrong chat |
| owner_id, lease_epoch, expires_at | Coordinate cooperating sessions and reject stale owners |
| initial_composer | Record whether the composer was empty or contained an existing draft |
| operation_id, payload, payload_hash | Identify the exact intended message |
| phase | Track prepared → inserted → send_attempted → confirmed |
| history_anchor, sent_message_id | Detect submissions, including unexpected partial ones |

Store the journal durably before touching the composer. If an existing user draft must be displaced, preserve its exact contents securely; a hash alone cannot restore it.

## 2. Required recovery checks

1. Before editing: Verify conversation identity, lease ownership, and composer contents. Never overwrite an unrecognized draft.
2. Before clearing stale text: Confirm it exactly matches the previously recorded agent-owned insertion and that no intervening user edit is evident. Otherwise stop.
3. Before Send: Revalidate ownership, full composer contents, and outgoing chat history since history_anchor.
4. After Send: Confirm the outgoing message in chat history, preferably using a stable message ID. Do not infer success from an empty composer.
5. After a crash: Reconcile outgoing messages before restoring, clearing, or retrying anything. Ambiguous results enter uncertain rather than triggering an automatic resend.

Prefer atomic paste over simulated character-by-character typing. Use an explicit Send control rather than Enter when possible.

## 3. Accidental partial submission

Example: Intended: A + B + C. Composer temporarily contains A. An accidental Enter submits A. The session crashes before the planned Send.

On recovery, checking only for the full intended message would incorrectly conclude that nothing was sent. The protocol must instead inspect all outgoing messages since the history anchor. If A is found, record the partial submission, mark the operation partial_sent, and block automatic submission of A + B + C. Recovery requires an explicit decision to continue, correct, or replace the partial message. The journal cannot undo what was already delivered.

## 4. Guarantees versus limitations

| Property | Assessment |
|---|---|
| Prevent cooperative sessions from deliberately sharing ownership | Achievable with leases and fencing checks |
| Avoid overwriting recognized user drafts | Achievable under cooperative ownership rules |
| Detect a visible partial submission | Achievable through history reconciliation |
| Avoid duplicate sends after uncertain outcomes | Achievable by blocking ambiguous retries |
| Guarantee exactly-once delivery | Not achievable through UI alone |
| Guarantee no draft loss during arbitrary concurrent UI edits | Not achievable through UI alone |
| Prevent stale browser actions already in flight | Not guaranteed by a lease alone |

The critical race is between checking the composer and editing or submitting it. A human or stale session can change the UI during that interval. UI-level leases are advisory unless all actors honor them and stale actions are actually fenced.

For stronger guarantees, move message submission behind a server API supporting idempotency keys and atomic ownership checks.

## 5. Recommended minimal policy

Use fail-closed sending, non-destructive recovery, and permissive reclaiming of verified stale agent text.

An expired session should not block another session indefinitely. However, expiration alone must never authorize deleting composer contents. Reclaim only when conversation, ownership journal, and exact content checks agree; otherwise leave the draft untouched.

This prevents most cooperative-session failures without introducing a permanent global composer lock. It deliberately prioritizes avoiding duplicate or destructive actions over guaranteeing automatic progress.

Decision: apply ownership records before input, account for unplanned partial sends, require exact matching and explicit browser evidence, leave personal or unclear drafts untouched. Do not displace a user draft even though the consultation mentions preserving one.
