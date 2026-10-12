"""Midnight Signal: a choice-driven cybersecurity adventure for the terminal."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


CAREER_RECORD_PATH = Path(__file__).with_name("career_record.json")
DEFAULT_CAREER_RECORD = {"best_score": 0, "completed_missions": 0}


@dataclass
class GameState:
    """Tracks the player's progress during one mission."""

    score: int = 0
    team_trust: int = 0
    evidence_preserved: bool = False
    host_isolated: bool = False
    incident_resolved: bool = False
    inventory: list[str] = field(default_factory=list)


def load_career_record(path: Path) -> dict[str, int]:
    """Load a validated career record, falling back safely when needed."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return DEFAULT_CAREER_RECORD.copy()

    if not isinstance(data, dict):
        return DEFAULT_CAREER_RECORD.copy()

    best_score = data.get("best_score")
    completed_missions = data.get("completed_missions")
    if (
        not isinstance(best_score, int)
        or isinstance(best_score, bool)
        or best_score < 0
        or not isinstance(completed_missions, int)
        or isinstance(completed_missions, bool)
        or completed_missions < 0
    ):
        return DEFAULT_CAREER_RECORD.copy()
    return {"best_score": best_score, "completed_missions": completed_missions}


def save_career_record(path: Path, record: dict[str, int]) -> None:
    """Persist a career record as readable JSON."""
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def update_career_record(record: dict[str, int], score: int) -> None:
    """Count a completed mission and retain the player's best score."""
    record["completed_missions"] += 1
    record["best_score"] = max(record["best_score"], score)


# Each scene is a short story beat. Choices apply effects, then move to another scene.
SCENES: dict[str, dict[str, Any]] = {
    "briefing": {
        "title": "02:13 — THE ALERT",
        "text": (
            "The SOC dashboard flashes amber. A test workstation has triggered an\n"
            "unfamiliar sign-in alert, and the night shift is nearly over. You are\n"
            "the responder on duty. Every choice is made inside a safe simulation."
        ),
        "choices": [
            {"label": "Inspect the alert metadata before acting", "next": "alert", "effects": {"score": 1}},
            {"label": "Ask analyst Nia to review the alert with you", "next": "teammate", "effects": {"team_trust": 1}},
            {"label": "Isolate the simulated workstation immediately", "next": "containment", "effects": {"score": 1, "host_isolated": True}},
        ],
    },
    "alert": {
        "title": "THE TIMELINE",
        "text": (
            "The alert contains a timestamp, a device ID, and a login from an unusual\n"
            "location. The evidence may disappear when the workstation is restarted."
        ),
        "choices": [
            {"label": "Preserve the event logs and record their hash", "next": "dashboard", "effects": {"score": 2, "evidence_preserved": True, "item": "Preserved event logs"}},
            {"label": "Contain the endpoint first and document the time", "next": "containment", "effects": {"score": 1, "host_isolated": True}},
            {"label": "Dismiss the alert without checking the evidence", "next": "ending_missed", "effects": {"score": -2}},
        ],
    },
    "teammate": {
        "title": "A SECOND PAIR OF EYES",
        "text": (
            "Nia replies: 'I can help. What do we know so far?' A clear handoff could\n"
            "save time, but guessing would only make the investigation noisier."
        ),
        "choices": [
            {"label": "Share the exact timestamp and investigate together", "next": "alert", "effects": {"score": 1, "team_trust": 2}},
            {"label": "Rush ahead alone and leave Nia out of the loop", "next": "dashboard", "effects": {"team_trust": -1}},
            {"label": "Ask Nia to preserve logs while you isolate the host", "next": "containment", "effects": {"score": 1, "team_trust": 2, "evidence_preserved": True, "host_isolated": True, "item": "Preserved event logs"}},
        ],
    },
    "dashboard": {
        "title": "FOLLOW THE SIGNAL",
        "text": (
            "The lab dashboard shows a short sequence of sign-in events. You have\n"
            "enough context to investigate safely, but not enough to declare victory."
        ),
        "choices": [
            {"label": "Search the mock logs and build an event timeline", "next": "timeline", "effects": {"score": 2, "evidence_preserved": True, "item": "Event timeline"}},
            {"label": "Isolate the lab network segment and note the time", "next": "containment", "effects": {"score": 1, "host_isolated": True}},
            {"label": "Restore from a verified snapshot, then validate", "next": "recovery", "effects": {"score": 1, "incident_resolved": True, "item": "Snapshot verification"}},
        ],
    },
    "timeline": {
        "title": "CONNECT THE DOTS",
        "text": (
            "The timeline points to an unexpected sign-in followed by a suspicious\n"
            "process alert. The story is becoming clearer: preserve what you can,\n"
            "contain the simulation, and keep the team informed."
        ),
        "choices": [
            {"label": "Correlate the timestamps and pass findings to the team", "next": "containment", "effects": {"score": 2, "team_trust": 1, "item": "Correlated incident timeline"}},
            {"label": "Skip correlation and close the ticket", "next": "ending_missed", "effects": {"score": -2}},
        ],
    },
    "containment": {
        "title": "CONTAINMENT CHECK",
        "text": (
            "The workstation is part of a fictional lab. Choose a careful response: \n"
            "containment should be documented, and useful evidence should be retained."
        ),
        "choices": [
            {"label": "Confirm isolation and record the action in the case notes", "next": "recovery", "effects": {"score": 2, "host_isolated": True, "item": "Containment note"}},
            {"label": "Restart immediately before checking evidence", "next": "recovery", "effects": {"score": -1}},
            {"label": "Ask Nia to verify isolation and review your notes", "next": "recovery", "effects": {"score": 2, "team_trust": 2, "host_isolated": True}},
        ],
    },
    "recovery": {
        "title": "VERIFY BEFORE YOU CLOSE",
        "text": (
            "The immediate alert is quiet. The final decision matters: validate the\n"
            "system, escalate with evidence, or risk closing the case too early."
        ),
        "choices": [
            {"label": "Check against a clean baseline and write the incident report", "next": "ending_evaluated", "effects": {"score": 2, "incident_resolved": True, "item": "Incident report"}},
            {"label": "Keep the host isolated and escalate with your evidence", "next": "ending_cautious", "effects": {"team_trust": 1}},
            {"label": "Declare success without completing validation", "next": "ending_missed", "effects": {"score": -2}},
        ],
    },
    "ending_best": {
        "title": "ENDING: CLEAN HANDOFF",
        "text": (
            "Excellent response. You preserved evidence, contained the simulated\n"
            "host, validated recovery, and kept the team aligned. Your incident report\n"
            "gives the next shift a clear, defensible account of what happened.\n\n"
            "MISSION RESULT: Strong investigation"
        ),
        "choices": [],
    },
    "ending_good": {
        "title": "ENDING: INCIDENT CONTROLLED",
        "text": (
            "You contained the situation and retained useful evidence. A few details\n"
            "could be stronger, but the case is in a safe state and ready for review.\n\n"
            "MISSION RESULT: Solid response"
        ),
        "choices": [],
    },
    "ending_cautious": {
        "title": "ENDING: ESCALATED SAFELY",
        "text": (
            "You chose caution and escalated the case rather than claiming certainty.\n"
            "The system remains isolated while the team reviews the remaining unknowns.\n\n"
            "MISSION RESULT: Safe escalation"
        ),
        "choices": [],
    },
    "ending_missed": {
        "title": "ENDING: TOO SOON TO CLOSE",
        "text": (
            "The alert was closed before the evidence was fully checked. The team\n"
            "cannot confidently explain what happened, so the case must be reopened.\n"
            "In incident response, a quiet dashboard is not the same as a verified fix.\n\n"
            "MISSION RESULT: Review your choices and try again"
        ),
        "choices": [],
    },
}


def apply_effects(state: GameState, effects: dict[str, Any]) -> None:
    """Apply a choice's state changes, keeping inventory entries unique."""
    for key, value in effects.items():
        if key == "item":
            if value not in state.inventory:
                state.inventory.append(value)
        elif hasattr(state, key):
            current = getattr(state, key)
            if isinstance(current, bool) and isinstance(value, bool):
                setattr(state, key, value)
            elif isinstance(current, (int, float)) and not isinstance(current, bool):
                setattr(state, key, current + value)
            else:
                setattr(state, key, value)
        else:
            raise KeyError(f"Unknown game-state effect: {key}")


def choose_ending(state: GameState) -> str:
    """Select an outcome based on the player's investigation choices."""
    if (
        state.evidence_preserved
        and state.host_isolated
        and state.incident_resolved
        and state.score >= 7
        and state.team_trust >= 1
    ):
        return "ending_best"
    if state.evidence_preserved and state.host_isolated:
        return "ending_good"
    return "ending_cautious"


def show_status(state: GameState) -> None:
    """Print a compact, readable mission HUD."""
    inventory_text = ", ".join(state.inventory) if state.inventory else "empty"
    print("\n" + "─" * 58)
    print(f"  SCORE {state.score:>3}    TEAM TRUST {state.team_trust:>3}")
    print(f"  Evidence: {'preserved' if state.evidence_preserved else 'not yet preserved'}")
    print(f"  Host:    {'isolated' if state.host_isolated else 'not isolated'}")
    print(f"  Toolkit: {inventory_text}")
    print("─" * 58)


def get_choice_count(scene: dict[str, Any]) -> int:
    return len(scene["choices"])


def play_mission(
    career_record: dict[str, int] | None = None,
    record_path: Path = CAREER_RECORD_PATH,
) -> bool:
    """Play one mission and return whether it reached an ending."""
    if career_record is None:
        career_record = load_career_record(record_path)

    state = GameState()
    scene_id = "briefing"

    while True:
        scene = SCENES[scene_id]
        print(f"\n\n╔{'═' * 56}╗")
        print(f"║  {scene['title']:<54}║")
        print(f"╚{'═' * 56}╝")
        print(scene["text"])

        if not scene["choices"]:
            show_status(state)
            update_career_record(career_record, state.score)
            save_career_record(record_path, career_record)
            return True

        show_status(state)
        for index, choice in enumerate(scene["choices"], start=1):
            print(f"  {index}. {choice['label']}")
        print("  Q. Quit to terminal")

        while True:
            try:
                answer = input("\nChoose your next move: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n\nMission ended. Thanks for playing Midnight Signal.")
                raise SystemExit(0)

            if answer == "q":
                print("\nMission ended. Thanks for playing Midnight Signal.")
                return False
            if answer.isdigit() and 1 <= int(answer) <= get_choice_count(scene):
                choice = scene["choices"][int(answer) - 1]
                apply_effects(state, choice["effects"])
                scene_id = choice["next"]
                if scene_id == "ending_evaluated":
                    scene_id = choose_ending(state)
                break
            print(f"Enter a number from 1 to {get_choice_count(scene)}, or Q to quit.")


def main() -> None:
    print(r"""
  __  __ ___ ____  _   _ ___ ____ _   _ ____ _   _ _____   ____ ___ ____ _   _    _    _
 |  \/  |_ _|  _ \| \ | |_ _/ ___| | | / ___| \ | | ____| / ___|_ _/ ___| \ | |  / \  | |
 | |\/| || || | | |  \| || | |  _| | | | |  _|  \| |  _|   \___ \| | |  _|  \| | / _ \ | |
 | |  | || || |_| | |\  || | |_| | |_| | |_| | |\  | |___   ___) | | |_| | |\  |/ ___ \| |___
 |_|  |_|___|____/|_| \_|___\____|\___/ \____|_| \_|_____| |____/___\____|_| \_/_/   \_\_____|
                         A TERMINAL CYBERSECURITY ADVENTURE
""")
    print("A fictional, choice-driven incident-response story. No network access or external packages required.")
    career_record = load_career_record(CAREER_RECORD_PATH)
    print(
        f"Career record: {career_record['completed_missions']} completed mission(s), "
        f"best score {career_record['best_score']}."
    )
    while True:
        play_mission(career_record, CAREER_RECORD_PATH)
        print(
            f"\nCareer record: {career_record['completed_missions']} completed mission(s), "
            f"best score {career_record['best_score']}."
        )
        try:
            answer = input("\nPlay another mission? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nSee you next shift, analyst.")
            return
        if answer not in {"y", "yes"}:
            print("\nSee you next shift, analyst. Stay curious and preserve the evidence.\n")
            return


if __name__ == "__main__":
    main()
