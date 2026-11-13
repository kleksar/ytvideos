"""Thumbnail acceptance needs more than a decoded image and a texture note."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

from PIL import Image, ImageDraw

import test_pool_service as fixtures
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.image_review import PREVIEW_HELPER, RESULT_SCHEMA, SCHEMA, validate_observation
from ytvideos.util import file_digest
from ytvideos.workflow import REQUIRED_CHECKS, required_checks


ROOT = Path(__file__).resolve().parents[1]


class ThumbnailReviewTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.PoolServiceTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.production = self.fixture.production
        self.root = self.fixture.root
        helper = self.production.project / PREVIEW_HELPER
        helper.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / PREVIEW_HELPER, helper)
        profile_path = self.production.project / "channels/test_channel/channel.json"
        profile = json.loads(profile_path.read_text())
        profile["production"] = json.loads((ROOT / "channels/paper_detour/channel.json").read_text())["production"]
        profile_path.write_text(json.dumps(profile))
        run = self.production.create("test_channel", "Synthetic thumbnail review regression", capabilities={
            "sessions.independent": {"available": True, "evidence": "Synthetic independent session fixture",
                                     "runtime_key": "fixture-runtime", "max_sessions": 1},
            "image.generate": {"available": True, "evidence": "Synthetic native image fixture", "billing": "included"},
        })
        self.run_id = run["id"]
        script = self.root / "script.txt"
        script.write_text("Synthetic accepted narration for this test, not a real episode. " * 6)
        packaging = self.root / "packaging.json"
        packaging.write_text(json.dumps({"title": "Synthetic test title"}))
        script_artifact = self.production.artifacts.put(script, "script")
        package_artifact = self.production.artifacts.put(packaging, "release_spec")

        def prepared(tx, state):
            for key, artifact in [("script", script_artifact), ("packaging", package_artifact)]:
                state["artifacts"][artifact["id"]] = artifact
                state["tasks"][key].update(status="complete", outputs=[artifact["id"]])
            state["approvals"]["script"] = {"artifact_id": script_artifact["id"], "revision": state["revision"]}

        self.fixture.store.mutate(self.run_id, prepared)
        self.image = self.root / "artwork.png"
        image = Image.new("RGB", (480, 854), "#243040")
        ImageDraw.Draw(image).rectangle((170, 260, 310, 590), fill="#f1cf65")
        image.save(self.image)
        self.fixture.image = self.image
        reference_path = self.root / "reference.png"
        Image.new("RGB", (320, 180), "#64744c").save(reference_path)
        self.reference = self.production.attach(self.run_id, reference_path, kind="image", source="Synthetic visual fixture")
        self.reference = self.fixture.store.get(self.run_id)["artifacts"][self.reference["id"]]
        self.brief = {"id": "main", "title": "Synthetic test title", "prompt": "Synthetic composition for an isolated test",
                      "visual_intent": "Test a large clear center", "references": [self.reference["id"]]}
        from thumbnail_fixtures import seed_packaging
        seed_packaging(self.production, self.run_id, self.root,
                       title=self.brief["title"], ids=["main", "no-reference"])
        self.task = self.production.add_thumbnail_task(self.run_id, self.brief)
        self.fixture.pools.operate(self.run_id, "initialize", {
            "runtime_key": "fixture-runtime", "max_sessions": 1, "review_capacity": 2,
            "evidence": "Synthetic native session fixture",
        })
        self.fixture.pools.operate(self.run_id, "enqueue")
        self.pending = self.fixture.pools.operate(self.run_id, "tick")["pending"][0]
        self.granted = self.fixture.claim(self.run_id, self.pending)
        self.claim = self.granted["task_claim"]
        self.fixture.native_complete(self.run_id, self.granted)
        self.preview_dir = self.root / "previews"
        self.card = self.root / "card.json"
        self.card.write_text(json.dumps({"title": self.brief["title"], "channel": "Test channel"}))
        self.build_previews()
        note = self.root / "review-evidence.txt"
        note.write_text("Synthetic test observations only; no person viewed these fixtures and no CTR is claimed.")
        manifest = json.loads((self.preview_dir / "manifest.json").read_text())
        self.observed = {
            "schema": SCHEMA, "artifact_sha256": file_digest(self.image), "reviewer": "independent-test-reviewer",
            "concept_id": "main", "artwork_text": "FIXTURE",
            "title": self.brief["title"], "preview_manifest": self.record(self.preview_dir / "manifest.json"),
            "phone_preview": self.record(Path(manifest["previews"][0]["path"])),
            "crop_preview": self.record(Path(manifest["previews"][1]["path"])),
            "observations": {
                "focal_point": "Synthetic fixture: yellow center rectangle.",
                "story_relation": "Synthetic geometry represents only the regression, no real story claim.",
                "title_pair": "Synthetic test title is the exact brief text.",
                "phone_size": "Synthetic 320px derivative retains the center rectangle.",
                "crop": "Synthetic center rectangle stays inside the central 2:3 crop.",
            },
            "references": [{"artifact_id": self.reference["id"], "sha256": self.reference["sha256"],
                            "comparison": "Synthetic artwork has a yellow center; reference fixture is a green plane."}],
            "evidence": self.record(note),
        }
        self.write_review_result()

    def write_review_result(self, **changes):
        result = {key: value for key, value in self.observed.items() if key != "evidence"}
        result.update(schema=RESULT_SCHEMA, decision="pass",
                      source={"tool": "synthetic-fixture", "session_id": "independent-test-reviewer"})
        result.update(changes)
        path = Path(self.observed["evidence"]["path"])
        path.write_text(json.dumps(result))
        self.observed["evidence"] = self.record(path)

    @staticmethod
    def record(path):
        return {"path": str(path), "sha256": file_digest(path)}

    def build_previews(self, *, width=320, crop="2:3"):
        args = [sys.executable, str(self.production.project / PREVIEW_HELPER), str(self.image),
                "--out", str(self.preview_dir), "--widths", str(width), "--card-json", str(self.card), "--crops"]
        if crop:
            args.append(crop)
        subprocess.run(args, check=True, capture_output=True, text=True)

    def receipt(self, observed=None):
        checks = [{"name": name, "status": "pass", "method": "synthetic test fixture",
                   "observed": {"fixture": True}} for name in REQUIRED_CHECKS["scene_image"]]
        if observed is not False:
            checks.append({"name": "thumbnail_review", "status": "pass", "method": "synthetic independent review fixture",
                           "observed": self.observed if observed is None else observed})
        path = self.root / "receipt.json"
        path.write_text(json.dumps({"run_id": self.run_id, "task_id": self.task["id"],
                                   "input_hash": self.claim["input_hash"], "worker": self.claim["worker"],
                                   "output_sha256": file_digest(self.image), "checks": checks}))
        return path

    def complete(self, observed=None):
        return self.production.complete(self.run_id, self.task["id"], self.claim["token"],
                                        self.image, self.receipt(observed), actual_units=0)

    def test_texture_only_receipt_cannot_complete_or_be_accepted_by_pool(self):
        with self.assertRaisesRegex(WorkflowError, "missing checks: thumbnail_review"):
            self.complete(False)
        with self.assertRaisesRegex(Conflict, "complete the claimed image task"):
            self.fixture.pools.operate(self.run_id, "accept", {
                "job_id": self.pending["packet"]["job_id"], "review_id": "texture-only", "service_seconds": 1,
            })

    def test_exact_composition_review_preserves_evidence_and_accepts_the_native_result(self):
        task = self.complete()
        self.assertEqual(task["status"], "complete")
        records = task["media_validation"]["evidence_artifacts"]
        self.assertGreaterEqual(len(records), 6)
        self.assertIn(self.reference["id"], task["media_validation"]["checked_artifact_ids"])
        shutil.rmtree(self.preview_dir)
        for record in records:
            self.assertTrue(self.production.artifacts.resolve(record).is_file())
        # Lost completion acknowledgement does not depend on disposable previews.
        self.assertEqual(self.complete()["status"], "complete")
        result = self.fixture.pools.operate(self.run_id, "accept", {
            "job_id": self.pending["packet"]["job_id"], "review_id": "exact-synthetic-review", "service_seconds": 4,
        })
        self.assertEqual(result["status"], "accepted")

    def test_unrelated_or_unreadable_file_is_not_independent_review_evidence(self):
        path = Path(self.observed["evidence"]["path"])
        for content in ("No review was performed.", "{broken", "{}", "[]"):
            path.write_text(content)
            self.observed["evidence"] = self.record(path)
            with self.subTest(content=content), self.assertRaisesRegex(WorkflowError, "review result"):
                self.complete()
        self.assertNotEqual(self.fixture.store.get(self.run_id)["tasks"][self.task["id"]]["status"], "complete")

    def test_failed_review_or_receipt_rewriting_cannot_be_promoted_to_pass(self):
        for changes in ({"decision": "fail"}, {"decision": "unverified"},
                        {"reviewer": "some-other-reviewer"}, {"observations": {}},
                        {"artifact_sha256": "0" * 64}, {"source": {}}):
            self.write_review_result(**changes)
            with self.subTest(changes=changes), self.assertRaises(WorkflowError):
                self.complete()

    def test_wrong_image_title_self_review_or_omitted_reference_is_rejected(self):
        for field, value in [("artifact_sha256", "0" * 64), ("title", "Another title"),
                             ("reviewer", self.claim["worker"]), ("references", []),
                             ("artwork_text", ""), ("concept_id", "another")]:
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                self.complete({**self.observed, field: value})
        bad = copy.deepcopy(self.observed)
        bad["observations"].pop("phone_size")
        with self.assertRaisesRegex(WorkflowError, "separate composition"):
            self.complete(bad)

    def test_rehashed_unrelated_preview_cannot_masquerade_as_the_actual_artwork(self):
        path = Path(self.observed["phone_preview"]["path"])
        Image.new("RGB", (320, 569), "red").save(path)
        manifest_path = self.preview_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["previews"][0]["sha256"] = file_digest(path)
        manifest_path.write_text(json.dumps(manifest))
        bad = {**self.observed, "phone_preview": self.record(path), "preview_manifest": self.record(manifest_path)}
        with self.assertRaisesRegex(WorkflowError, "canonical derivative"):
            self.complete(bad)

    def test_uncropped_master_and_wrong_card_title_do_not_replace_crop_and_pair_checks(self):
        with self.assertRaisesRegex(WorkflowError, "required displayed crop"):
            self.complete({**self.observed, "crop_preview": self.observed["phone_preview"]})
        self.card.write_text(json.dumps({"title": "A different title", "channel": "Test channel"}))
        self.build_previews()
        with self.assertRaisesRegex(WorkflowError, "card title/channel"):
            self.complete({**self.observed, "preview_manifest": self.record(self.preview_dir / "manifest.json")})

    def test_full_resolution_or_single_pixel_is_not_a_phone_size_inspection(self):
        for width in (1, 1024):
            self.build_previews(width=width)
            manifest_path = self.preview_dir / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            observed = {**self.observed, "preview_manifest": self.record(manifest_path),
                        "phone_preview": self.record(Path(manifest["previews"][0]["path"])),
                        "crop_preview": self.record(Path(manifest["previews"][1]["path"]))}
            with self.subTest(width=width), self.assertRaisesRegex(WorkflowError, "phone-size"):
                self.complete(observed)

    def test_dynamic_check_and_exact_references_are_visible_in_context_plan_and_pool(self):
        expected = sorted(required_checks("scene_image", purpose="thumbnail"))
        packet = self.production.context(self.run_id, self.task["id"])
        self.assertEqual(packet["required_checks"], expected)
        self.assertEqual(packet["task_guide"]["required_checks"], expected)
        self.assertEqual(packet["visual_references"], [self.reference])
        plan = self.production.plan(self.run_id)
        self.assertEqual(next(step for step in plan["steps"] if step["id"] == self.task["id"])["required_checks"], expected)
        self.assertEqual(self.pending["packet"]["context"]["required_checks"], expected)
        self.assertEqual(self.pending["packet"]["context"]["visual_references"], [self.reference])
        self.assertNotIn("thumbnail_review", required_checks("scene_image"))

    def test_title_and_registered_reference_are_checked_before_a_task_is_added(self):
        for change in [{"title": ""}, {"references": ["unknown"]}, {"references": []}]:
            with self.subTest(change=change), self.assertRaises(WorkflowError):
                self.production.add_thumbnail_task(self.run_id, {**self.brief, "id": "invalid", **change})
        self.assertNotIn("thumbnail:invalid", self.fixture.store.get(self.run_id)["tasks"])

    def test_reference_not_applicable_is_explicit_without_inventing_an_art_reference(self):
        brief = {**self.brief, "id": "no-reference", "references": [],
                 "reference_na_reason": "Synthetic geometry regression has no artistic reference requirement."}
        self.production.add_thumbnail_task(self.run_id, brief)
        observed = {**self.observed, "references": [], "reference_na_reason": brief["reference_na_reason"]}
        self.assertIs(validate_observation(observed, artifact_sha256=file_digest(self.image),
                                          worker=self.claim["worker"], brief=brief,
                                          artifacts=self.fixture.store.get(self.run_id)["artifacts"]), observed)


if __name__ == "__main__":
    unittest.main()
