"""Regression cases for missing channel recipes and isolated worker requirements."""

import json
from pathlib import Path
import unittest

import test_pool_service as fixtures
from ytvideos.context import TASK_EXECUTION_REFERENCE, snapshot_references, validate_documents
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.service import Production
from ytvideos.store import Store
from ytvideos.util import digest


class ConfiguredRecipeTests(unittest.TestCase):
    def test_scenes_profile_selects_bryan_and_final_narration_speed(self):
        from ytvideos.profiles import load_profile
        root = Path(__file__).resolve().parents[1]
        profile = load_profile(root / "channels", "scenes_on_repeat")
        self.assertEqual(profile["voice"], {"provider": "elevenlabs", "id": "K60rGfHNsqGiO3nscQV3", "speed": 1.1})

    def test_future_you_but_weird_export_rule_is_pinned_without_changing_legacy_recipes(self):
        from ytvideos.profiles import load_profile
        root = Path(__file__).resolve().parents[1]
        profile = load_profile(root / "channels", "scenes_on_repeat")
        snapshot = snapshot_references(root, profile, "long")
        path = "channels/scenes_on_repeat/PROFILE.md"
        self.assertIn(path, snapshot["routes"]["render"])
        self.assertIn(path, snapshot["routes"]["review"])
        text = snapshot["documents"][path]["text"]
        self.assertIn("**1080p, 30 fps**", text)
        self.assertIn("1920×1080", text)
        formats = profile["production"]["formats"]
        self.assertEqual(formats["long"]["video"], {"canvas": None, "fps": None})
        self.assertEqual(formats["short"]["variants"]["scene"]["video"]["fps"], "24/1")
        self.assertEqual(formats["short"]["variants"]["meme_time_machine"]["video"]["fps"], "48/1")

    def test_clip_procedure_is_pinned_across_channels_without_thumbnail_leakage(self):
        root = Path(__file__).resolve().parents[1]
        path = ".agents/skills/ytv-produce-video/references/video-clips.md"
        profiles = [{"id": "generic_unconfigured"}]
        for channel_file in sorted((root / "channels").glob("*/channel.json")):
            profiles.append(json.loads(channel_file.read_text()))
        for profile in profiles:
            for form in ("short", "long"):
                snapshot = snapshot_references(root, profile, form)
                with self.subTest(channel=profile["id"], format=form):
                    for stage in ("storyboard", "scene_image", "render", "review"):
                        self.assertIn(path, snapshot["routes"][stage])
                    for stage in ("thumbnail", "audio", "research", "packaging"):
                        self.assertNotIn(path, snapshot["routes"][stage])
                    self.assertEqual(snapshot["documents"][path]["text"], (root / path).read_text())

    def test_history_packets_include_the_visual_identity_and_caption_rules(self):
        root = Path(__file__).resolve().parents[1]
        profile = json.loads((root / "channels/nuviko_history/channel.json").read_text())
        identity = "channels/nuviko_history/brand/VISUAL_PROFILE.md"
        visual_tasks = {"storyboard", "scene_image", "thumbnail", "subtitles", "render", "review", "packaging"}
        for format in ("short", "long"):
            snapshot = snapshot_references(root, profile, format)
            for task, paths in snapshot["routes"].items():
                with self.subTest(format=format, task=task):
                    self.assertIn("channels/nuviko_history/PROFILE.md", paths)
                    if task in visual_tasks:
                        self.assertIn(identity, paths)
                    else:
                        self.assertNotIn(identity, paths)

    def test_history_audio_uses_the_shared_music_preferences(self):
        root = Path(__file__).resolve().parents[1]
        profile = json.loads((root / "channels/nuviko_history/channel.json").read_text())
        catalog = "channels/paper_detour/docs/MUSIC_CATALOG.md"
        for format in ("short", "long"):
            snapshot = snapshot_references(root, profile, format)
            for task, paths in snapshot["routes"].items():
                with self.subTest(format=format, task=task):
                    if task == "audio":
                        self.assertIn(catalog, paths)
                    else:
                        self.assertNotIn(catalog, paths)

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

    def test_scenes_short_source_selection_gets_edit_rules_before_assembly(self):
        root = Path(__file__).resolve().parents[1]
        profile = json.loads((root / "channels/scenes_on_repeat/channel.json").read_text())
        recipe = "channels/scenes_on_repeat/docs/EDIT_NOTES.md"
        short = snapshot_references(root, profile, "short")
        for stage in ("research", "script", "scene_image"):
            with self.subTest(format="short", stage=stage):
                self.assertIn(recipe, short["routes"][stage])
        self.assertNotIn(recipe, short["routes"]["thumbnail"])
        long = snapshot_references(root, profile, "long")
        for stage in ("research", "script", "scene_image", "thumbnail"):
            with self.subTest(format="long", stage=stage):
                self.assertNotIn(recipe, long["routes"][stage])


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

    def test_skill_examples_are_scoped_and_keep_their_saved_text(self):
        examples = {
            ".agents/skills/ytv-write-script/references/hook-patterns.md": {"research", "script"},
            ".agents/skills/ytv-produce-video/references/production-examples.md": {
                "storyboard", "scene_image", "thumbnail", "audio", "render"},
        }
        for path in examples:
            self.document(path, f"Accepted examples: {path}\n")
        run = self.production.create("test_channel", "use the task's examples")
        before = {}
        for route in run["reference_snapshot"]["routes"]:
            task = ({"stage": "scene_image", "payload": {"purpose": "thumbnail"}}
                    if route == "thumbnail" else {"stage": route})
            context = self.production._reference_context(run, task)
            before[route] = (task, context)
            documents = {item["path"]: item["text"] for item in context["reference_documents"]}
            for path, stages in examples.items():
                with self.subTest(route=route, path=path):
                    if route in stages:
                        self.assertEqual(documents[path], f"Accepted examples: {path}\n")
                    else:
                        self.assertNotIn(path, documents)
        for path in examples:
            self.document(path, "Changed examples for future runs.\n")
        for task, context in before.values():
            self.assertEqual(context, self.production._reference_context(run, task))
        new_run = self.production.create("test_channel", "use the revised examples")
        self.assertNotEqual(run["pins"]["references"], new_run["pins"]["references"])

    def test_every_task_route_receives_the_pinned_execution_procedure(self):
        self.document(TASK_EXECUTION_REFERENCE, "Read the exact instructions before acting.\n")
        for format in ("short", "long"):
            run = self.production.create("test_channel", "documented execution", format=format)
            for route, paths in run["reference_snapshot"]["routes"].items():
                with self.subTest(format=format, route=route):
                    self.assertIn(TASK_EXECUTION_REFERENCE, paths)
                    task = ({"stage": "scene_image", "payload": {"purpose": "thumbnail"}}
                            if route == "thumbnail" else {"stage": route})
                    documents = self.production._reference_context(run, task)["reference_documents"]
                    self.assertEqual(next(item["text"] for item in documents
                                          if item["path"] == TASK_EXECUTION_REFERENCE),
                                     "Read the exact instructions before acting.\n")

    def test_missing_or_blank_execution_procedure_cannot_create_a_run(self):
        path = self.document(TASK_EXECUTION_REFERENCE)
        path.unlink()
        with self.assertRaisesRegex(WorkflowError, "missing.*task-execution"):
            self.production.create("test_channel", "missing execution instructions")
        self.document(TASK_EXECUTION_REFERENCE, " \n\t")
        with self.assertRaisesRegex(WorkflowError, "empty.*task-execution"):
            self.production.create("test_channel", "empty execution instructions")
        self.assertEqual(self.fixture.store.list(), [])

    def test_execution_procedure_stays_pinned_after_checkout_edit_or_removal(self):
        path = self.document(TASK_EXECUTION_REFERENCE, "Accepted execution procedure.\n")
        run = self.production.create("test_channel", "keep execution instructions")
        before = self.production.context(run["id"], "research")
        path.write_text("Changed execution procedure.\n")
        self.assertEqual(before, self.production.context(run["id"], "research"))
        new_run = self.production.create("test_channel", "new execution instructions")
        self.assertNotEqual(run["pins"]["references"], new_run["pins"]["references"])
        path.unlink()
        self.assertEqual(before, self.production.context(run["id"], "research"))

    def test_blank_pinned_instruction_is_rejected_even_with_its_matching_hash(self):
        import hashlib
        text = " \n\t"
        document = {"path": TASK_EXECUTION_REFERENCE, "text": text,
                    "sha256": hashlib.sha256(text.encode()).hexdigest()}
        with self.assertRaisesRegex(WorkflowError, "empty.*task-execution"):
            validate_documents([TASK_EXECUTION_REFERENCE], [document])

    def test_blank_required_skill_cannot_create_a_run(self):
        (self.root / "skills/ytv-produce-video/SKILL.md").write_text(" \n\t")
        with self.assertRaisesRegex(WorkflowError, "required skill ytv-produce-video.*non-empty"):
            self.production.create("test_channel", "missing skill procedure")
        self.assertEqual(self.fixture.store.list(), [])

    def test_blank_saved_skill_cannot_be_used_even_with_its_matching_pin(self):
        run = self.production.create("test_channel", "saved skill procedure")
        def blank(tx, state):
            state["skills"]["ytv-write-script"]["text"] = " \n\t"
            state["pins"]["skills"] = digest(state["skills"])
        self.fixture.store.mutate(run["id"], blank)
        with self.assertRaisesRegex(WorkflowError, "required skill ytv-write-script.*non-empty"):
            self.production.context(run["id"], "research")

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
