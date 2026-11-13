"""Cross-promotion never treats suggestions or stale provider data as a write."""
from datetime import datetime, timedelta, timezone
import unittest

from ytvideos.cross_promotion import PromotionError, build_plan
from ytvideos.release import ReleaseSpec

CHANNEL = "UC" + "x" * 22
SHORT = "SHORT000001"
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
        self.assertEqual(result["actions"][0]["payload"]["long_id"], LONG)
        for patch in ({"channel_id": "UC" + "y" * 22}, {"privacy": "private"},
                      {"format": "short"}):
            snapshot = inventory()
            snapshot["videos"][1].update(patch)
            self.assertEqual(build_plan(release, video_id=SHORT, inventory=snapshot)["actions"][0]["status"], "blocked")

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

    def test_empty_optional_actions_do_not_invent_targets(self):
        result = build_plan(spec(), video_id=SHORT, inventory=inventory())
        self.assertEqual(result["actions"], [])
        self.assertEqual(result["blockers"], [])


if __name__ == "__main__":
    unittest.main()
