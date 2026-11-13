"""Cross-promotion never treats suggestions or stale provider data as a write."""
from datetime import datetime, timedelta, timezone
import unittest

from ytvideos.cross_promotion import PromotionError, build_plan
from ytvideos.release import ReleaseSpec

CHANNEL = "UC" + "x" * 22
SHORT = "SHORT000001"
RELATED_SHORT = "SHORT000002"
LONG = "LONG0000001"
SECOND = "LONG0000002"
PLAYLIST = "PL01234567890"


def spec(format="short", **options):
    doc = {
        "run_id": "cross-promotion-test", "revision": 1, "channel_id": CHANNEL,
        "format": format, "has_speech": False,
        "metadata": {
            "title": "An episode", "description": "Relevant episode.",
            "tags": ["history"], "category_id": "27", "language": "en",
            "audio_language": "en", "made_for_kids": False,
            "contains_synthetic_media": False, "license": "youtube",
            "age_restricted": False, "paid_promotion": False,
        },
        "publish_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        **options,
    }
    return ReleaseSpec.from_dict(doc)


def inventory():
    return {
        "channel_id": CHANNEL, "source": "api_readback",
        "observed_at": "2026-11-13T10:00:00Z",
        "videos": [
            {"id": SHORT, "channel_id": CHANNEL, "privacy": "public", "format": "short"},
            {"id": LONG, "channel_id": CHANNEL, "privacy": "public", "format": "long"},
            {"id": SECOND, "channel_id": CHANNEL, "privacy": "unlisted", "format": "long"},
            {"id": RELATED_SHORT, "channel_id": CHANNEL, "privacy": "public", "format": "short"},
        ],
        "playlists": [{"id": PLAYLIST, "channel_id": CHANNEL, "privacy": "public",
                       "members_complete": True, "video_ids": [LONG]}],
    }


class CrossPromotionTests(unittest.TestCase):
    def test_shorts_to_long_requires_same_channel_and_public_or_unlisted(self):
        release = spec(related_video_id=LONG)
        result = build_plan(release, video_id=SHORT, inventory=inventory())
        self.assertEqual(result["blockers"], [])
        self.assertEqual(result["actions"][0]["status"], "ready_for_host")
        self.assertEqual(result["schema"], "ytv-cross-promotion-plan-v1")
        self.assertEqual(result["actions"][0]["kind"], "shorts_to_long")
        self.assertEqual(result["actions"][0]["payload"], {"short_id": SHORT, "long_id": LONG})
        for patch in ({"channel_id": "UC" + "y" * 22}, {"privacy": "private"}):
            snapshot = inventory()
            snapshot["videos"][1].update(patch)
            self.assertEqual(build_plan(release, video_id=SHORT, inventory=snapshot)["actions"][0]["status"], "blocked")

    def test_related_short_accepts_public_or_unlisted(self):
        release = spec(related_video_id=RELATED_SHORT)
        for privacy in ("public", "unlisted"):
            with self.subTest(privacy=privacy):
                snapshot = inventory()
                snapshot["videos"][3]["privacy"] = privacy
                result = build_plan(release, video_id=SHORT, inventory=snapshot)
                self.assertEqual(result["schema"], "ytv-cross-promotion-plan-v1")
                self.assertEqual(result["blockers"], [])
                action = result["actions"][0]
                self.assertEqual(action["status"], "ready_for_host")
                self.assertEqual(action["kind"], "shorts_to_short")
                self.assertEqual(action["payload"], {"short_id": SHORT, "target_short_id": RELATED_SHORT})
                self.assertEqual(action["provider"], "studio")
                self.assertIn("verified result", action["requires"])
                self.assertEqual(result["execution"], "read_only_plan; no YouTube mutation or Studio result")

    def test_related_short_rejects_other_channel_private_or_missing_target(self):
        release = spec(related_video_id=RELATED_SHORT)
        for patch, expected in (
            ({"channel_id": "UC" + "y" * 22}, "target video belongs to another channel"),
            ({"privacy": "private"}, "target video is neither Public nor Unlisted"),
        ):
            with self.subTest(patch=patch):
                snapshot = inventory()
                snapshot["videos"][3].update(patch)
                result = build_plan(release, video_id=SHORT, inventory=snapshot)
                self.assertEqual(result["actions"][0]["status"], "blocked")
                self.assertIn(expected, result["blockers"])
        snapshot = inventory()
        snapshot["videos"].pop(3)
        result = build_plan(release, video_id=SHORT, inventory=snapshot)
        self.assertIn("target video is missing from the observed inventory", result["blockers"])

    def test_related_video_requires_observed_short_or_long_format(self):
        release = spec(related_video_id=RELATED_SHORT)
        for format in (None, "", "unknown", "live", [], {}):
            with self.subTest(format=format):
                snapshot = inventory()
                if format is None:
                    del snapshot["videos"][3]["format"]
                else:
                    snapshot["videos"][3]["format"] = format
                result = build_plan(release, video_id=SHORT, inventory=snapshot)
                self.assertEqual(result["actions"][0]["status"], "blocked")
                self.assertNotEqual(result["actions"][0]["kind"], "shorts_to_short")
                self.assertIn("target must be verified as a Short or long-form video", result["blockers"])

    def test_related_short_requires_verified_public_source(self):
        release = spec(related_video_id=RELATED_SHORT)
        for patch in ({"privacy": "private"}, {"format": "long"},
                      {"channel_id": "UC" + "y" * 22}):
            with self.subTest(patch=patch):
                snapshot = inventory()
                snapshot["videos"][0].update(patch)
                result = build_plan(release, video_id=SHORT, inventory=snapshot)
                self.assertEqual(result["actions"][0]["status"], "blocked")
        snapshot = inventory()
        snapshot["videos"].pop(0)
        result = build_plan(release, video_id=SHORT, inventory=snapshot)
        self.assertIn("published video is missing from the observed inventory", result["blockers"])

    def test_cannot_link_video_to_itself(self):
        result = build_plan(spec(related_video_id=SHORT), video_id=SHORT, inventory=inventory())
        self.assertIn("target cannot be the same video", result["blockers"])

    def test_end_screen_validates_targets_and_own_subscription(self):
        end = {"start_seconds": 80, "end_seconds": 90,
               "elements": [{"type": "video", "target_id": SECOND},
                            {"type": "subscribe", "target_id": CHANNEL}]}
        release = spec("long", duration_seconds=90, end_screen=end)
        result = build_plan(release, video_id=LONG, inventory=inventory())
        self.assertEqual(result["actions"][0]["status"], "ready_for_host")
        snapshot = inventory()
        snapshot["videos"][2]["privacy"] = "private"
        self.assertIn("target video is neither Public nor Unlisted",
                      build_plan(release, video_id=LONG, inventory=snapshot)["blockers"])

    def test_playlist_verified_membership_is_noop_or_ready(self):
        release = spec("long", playlist_id=PLAYLIST)
        result = build_plan(release, video_id=LONG, inventory=inventory())
        self.assertEqual(result["actions"][0]["status"], "already_present")
        snapshot = inventory()
        snapshot["playlists"][0]["video_ids"] = []
        self.assertEqual(build_plan(release, video_id=LONG, inventory=snapshot)["actions"][0]["status"],
                         "ready_for_host")
        del snapshot["playlists"][0]["members_complete"]
        self.assertEqual(build_plan(release, video_id=LONG, inventory=snapshot)["actions"][0]["status"], "blocked")

    def test_community_post_waits_for_verified_public_and_is_not_sent(self):
        release = spec("long", community_post={"text": "A different angle on this story."})
        snapshot = inventory()
        result = build_plan(release, video_id=LONG, inventory=snapshot)
        self.assertEqual(result["actions"][0]["payload"]["linked_video_id"], LONG)
        self.assertEqual(result["execution"], "read_only_plan; no YouTube mutation or Studio result")
        snapshot["videos"][1]["privacy"] = "private"
        self.assertEqual(build_plan(release, video_id=LONG, inventory=snapshot)["actions"][0]["status"], "blocked")

    def test_inventory_ownership_provenance_and_duplicates(self):
        release = spec(related_video_id=LONG)
        cases = [
            {"channel_id": "UC" + "y" * 22},
            {"source": "llm_assumption"},
            {"observed_at": "2026-11-13T10:00:00"},
            {"videos": [{"id": SHORT}, {"id": SHORT}]},
        ]
        for patch in cases:
            snapshot = inventory()
            snapshot.update(patch)
            with self.subTest(patch=patch), self.assertRaises(PromotionError):
                build_plan(release, video_id=SHORT, inventory=snapshot)

    def test_read_only_cli_does_not_open_database(self):
        from contextlib import redirect_stdout
        from io import StringIO
        import json
        from pathlib import Path
        import tempfile
        from ytvideos.cli import main

        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            (root / 'release.json').write_text(json.dumps(spec(related_video_id=LONG).to_dict()))
            (root / 'inventory.json').write_text(json.dumps(inventory()))
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main(['--db', str(root / 'missing' / 'state.sqlite3'),
                             'cross-promotion-plan', '--release-spec', str(root / 'release.json'),
                             '--inventory', str(root / 'inventory.json'), '--video-id', SHORT])
            self.assertEqual(code, 0)
            self.assertFalse((root / 'missing').exists())
            self.assertEqual(json.loads(stdout.getvalue())['actions'][0]['status'], 'ready_for_host')

    def test_empty_optional_actions_do_not_invent_targets(self):
        result = build_plan(spec(), video_id=SHORT, inventory=inventory())
        self.assertEqual(result["actions"], [])
        self.assertEqual(result["blockers"], [])


if __name__ == "__main__":
    unittest.main()
