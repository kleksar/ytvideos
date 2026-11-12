"""Regression cases for missing channel recipes and isolated worker requirements."""

import json
from pathlib import Path
import unittest

import test_pool_service as fixtures
from ytvideos.context import snapshot_references
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.service import Production
from ytvideos.store import Store


class ConfiguredRecipeTests(unittest.TestCase):
    def test_scenes_packets_include_each_supported_recipe_and_its_required_captions(self):
        root = Path(__file__).resolve().parents[1]
        profile = json.loads((root / "channels/scenes_on_repeat/channel.json").read_text())
        prefix = "channels/scenes_on_repeat/docs/"
        short = snapshot_references(root, profile, "short")
        for stage in ("research", "script", "storyboard", "audio", "subtitles", "render", "review", "packaging"):
            with self.subTest(format="short", stage=stage):
                self.assertIn(prefix + "MEME_SHORTS.md", short["routes"][stage])
                self.assertNotIn(prefix + "LONG_CAPTIONS.md", short["routes"][stage])
        self.assertIn(prefix + "EDIT_NOTES.md", short["routes"]["render"])
        long = snapshot_references(root, profile, "long")
        for stage in ("subtitles", "render", "review"):
            with self.subTest(format="long", stage=stage):
                for name in ("LONG_COMPILATIONS.md", "LONG_CAPTIONS.md", "EDIT_NOTES.md"):
                    self.assertIn(prefix + name, long["routes"][stage])
                    self.assertTrue(long["documents"][prefix + name]["text"])
                self.assertNotIn(prefix + "MEME_SHORTS.md", long["routes"][stage])


class TaskContextTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.PoolServiceTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.production = self.fixture.production
        self.root = self.production.project
        self.profile_path = self.root / "channels/test_channel/channel.json"

    def configure(self, references):
        profile = json.loads(self.profile_path.read_text())
        profile["context_references"] = references
        self.profile_path.write_text(json.dumps(profile))

    def document(self, path, text="Exact accepted channel recipe."):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        return target

    def test_context_delivers_the_recipe_for_the_requested_stage_and_format(self):
        short = "channels/test_channel/docs/short.md"
        long = "channels/test_channel/docs/long.md"
        cover = "channels/test_channel/docs/cover.md"
        profile = "channels/test_channel/PROFILE.md"
        for path in (short, long, cover, profile):
            self.document(path)
        self.configure([
            {"path": short, "stages": ["storyboard", "render"], "formats": ["short"]},
            {"path": long, "stages": ["storyboard", "render"], "formats": ["long"]},
            {"path": cover, "stages": ["scene_image"], "purposes": ["thumbnail"]},
        ])
        run = self.production.create("test_channel", "new short")
        context = self.production.context(run["id"], "render")
        self.assertIn(short, context["references"])
        self.assertIn(profile, context["references"])
        self.assertNotIn(long, context["references"])
        self.assertNotIn(short, self.production.context(run["id"], "research")["references"])
        self.assertIn("docs/standards/editorial.md", context["references"])
        self.assertEqual(next(doc["text"] for doc in context["reference_documents"] if doc["path"] == short),
                         "Exact accepted channel recipe.")
        image = {"stage": "scene_image"}
        thumbnail = {"stage": "scene_image", "payload": {"purpose": "thumbnail"}}
        self.assertNotIn(cover, self.production._reference_context(run, image)["references"])
        self.assertIn(cover, self.production._reference_context(run, thumbnail)["references"])
        second = self.production.create("test_channel", "new long", format="long")
        self.assertIn(long, self.production.context(second["id"], "render")["references"])
        self.assertNotIn(short, self.production.context(second["id"], "render")["references"])

    def test_resumed_run_keeps_saved_recipe_and_new_run_gets_the_new_version(self):
        path = "channels/test_channel/docs/recipe.md"
        recipe = self.document(path, "Accepted recipe version one.")
        self.configure([{"path": path, "stages": ["render"]}])
        run = self.production.create("test_channel", "original request")
        before = self.production.context(run["id"], "render")
        recipe.write_text("Changed recipe version two.")
        resumed = Production(Store(self.fixture.db), self.production.workspace, self.root)
        after = resumed.context(run["id"], "render")
        self.assertEqual(before, after)
        new_run = resumed.create("test_channel", "new request")
        self.assertNotEqual(run["pins"]["references"], new_run["pins"]["references"])
        recipe.unlink()
        self.assertEqual(before, resumed.context(run["id"], "render"))
        with self.assertRaisesRegex(WorkflowError, "missing"):
            resumed.create("test_channel", "cannot start without required recipe")

    def test_experiment_operations_are_loaded_only_at_the_release_steps_that_need_them(self):
        run = self.production.create("test_channel", "keep creative tasks scoped")
        experiments = "docs/operations/thumbnail-experiments.md"
        for stage in ("configure_release", "verify_publication"):
            self.assertIn(experiments, self.production.context(run["id"], stage)["references"])
        for stage in ("research", "script", "packaging", "schedule"):
            self.assertNotIn(experiments, self.production.context(run["id"], stage)["references"])
        thumbnail = {"stage": "scene_image", "payload": {"purpose": "thumbnail"}}
        self.assertNotIn(experiments, self.production._reference_context(run, thumbnail)["references"])
        self.assertNotIn("docs/standards/thumbnails.md",
                         self.production.context(run["id"], "verify_publication")["references"])

    def test_missing_or_escaping_explicit_recipe_is_rejected_before_run_creation(self):
        outside = self.fixture.root / "outside.md"
        outside.write_text("Outside the repository.")
        link = self.root / "escape.md"
        link.symlink_to(outside)
        for path in ("../outside.md", str(outside), "escape.md", "missing.md",
                     "C:/outside.md", "C:outside.md", "https://example.com/file.md", "file:outside.md"):
            with self.subTest(path=path):
                self.configure([{"path": path, "stages": ["render"]}])
                with self.assertRaises(WorkflowError):
                    self.production.create("test_channel", "invalid reference")
        self.assertEqual(self.fixture.store.list(), [])

    def test_legacy_run_labels_unsnapshotted_texts_and_checks_its_original_code_pin(self):
        run = self.production.create("test_channel", "legacy fixture")
        def legacy(tx, state):
            del state["reference_snapshot"]
            del state["pins"]["references"]
        self.fixture.store.mutate(run["id"], legacy)
        self.assertEqual(self.production.context(run["id"], "research")["reference_source"], "legacy_checkout")
        (self.root / "docs/standards/editorial.md").write_text("New editorial standard.")
        with self.assertRaisesRegex(Conflict, "pin"):
            self.production.context(run["id"], "research")

    def test_modified_snapshot_is_not_used_even_when_the_paths_still_match(self):
        run = self.production.create("test_channel", "snapshot integrity")
        def corrupt(tx, state):
            state["reference_snapshot"]["documents"]["docs/standards/editorial.md"]["text"] = "Changed silently"
        self.fixture.store.mutate(run["id"], corrupt)
        with self.assertRaisesRegex(WorkflowError, "snapshot"):
            self.production.context(run["id"], "research")

    def test_changed_skill_cannot_be_returned_under_the_original_skills_pin(self):
        run = self.production.create("test_channel", "pinned skill integrity")
        def corrupt(tx, state):
            state["skills"]["ytv-write-script"]["text"] = "Substituted skill text"
        self.fixture.store.mutate(run["id"], corrupt)
        with self.assertRaisesRegex(Conflict, "skills.*pin"):
            self.production.context(run["id"], "research")


if __name__ == "__main__":
    unittest.main()
