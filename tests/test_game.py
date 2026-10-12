import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from main import (
    GameState,
    apply_effects,
    choose_ending,
    load_career_record,
    save_career_record,
    update_career_record,
)


class CareerRecordTests(unittest.TestCase):
    def test_missing_file_uses_safe_default(self):
        with TemporaryDirectory() as directory:
            record = load_career_record(Path(directory) / "career_record.json")
        self.assertEqual(record, {"best_score": 0, "completed_missions": 0})

    def test_valid_record_is_loaded(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "career_record.json"
            path.write_text('{"best_score": 12, "completed_missions": 3}', encoding="utf-8")
            self.assertEqual(
                load_career_record(path),
                {"best_score": 12, "completed_missions": 3},
            )

    def test_malformed_json_uses_safe_default(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "career_record.json"
            path.write_text("{not valid json", encoding="utf-8")
            self.assertEqual(
                load_career_record(path),
                {"best_score": 0, "completed_missions": 0},
            )

    def test_update_keeps_best_score_and_counts_mission(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "career_record.json"
            record = {"best_score": 10, "completed_missions": 2}
            update_career_record(record, 8)
            save_career_record(path, record)
            self.assertEqual(
                load_career_record(path),
                {"best_score": 10, "completed_missions": 3},
            )
            update_career_record(record, 14)
            self.assertEqual(record, {"best_score": 14, "completed_missions": 4})


class ApplyEffectsTests(unittest.TestCase):
    def test_numeric_effects_accumulate(self):
        state = GameState(score=2, team_trust=1)
        apply_effects(state, {"score": 3, "team_trust": -1})
        self.assertEqual(state.score, 5)
        self.assertEqual(state.team_trust, 0)

    def test_boolean_flags_are_set(self):
        state = GameState()
        apply_effects(state, {"evidence_preserved": True, "host_isolated": True})
        self.assertTrue(state.evidence_preserved)
        self.assertTrue(state.host_isolated)

    def test_inventory_items_are_not_duplicated(self):
        state = GameState()
        apply_effects(state, {"item": "Event timeline"})
        apply_effects(state, {"item": "Event timeline"})
        self.assertEqual(state.inventory, ["Event timeline"])

    def test_unknown_effect_raises(self):
        with self.assertRaises(KeyError):
            apply_effects(GameState(), {"unknown_property": 1})


class EndingTests(unittest.TestCase):
    def test_best_ending_requires_complete_strong_response(self):
        state = GameState(
            score=8,
            team_trust=1,
            evidence_preserved=True,
            host_isolated=True,
            incident_resolved=True,
        )
        self.assertEqual(choose_ending(state), "ending_best")

    def test_evidence_and_isolation_allow_solid_ending(self):
        state = GameState(score=3, evidence_preserved=True, host_isolated=True)
        self.assertEqual(choose_ending(state), "ending_good")

    def test_incomplete_response_ends_cautiously(self):
        self.assertEqual(choose_ending(GameState()), "ending_cautious")


if __name__ == "__main__":
    unittest.main()
