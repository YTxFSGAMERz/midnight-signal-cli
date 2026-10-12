# Midnight Signal — Terminal Cybersecurity Adventure

A small, choice-driven **command-line adventure game** made with Python's standard library. Take the night shift in a fictional security operations center, investigate an alert, make response decisions, and discover one of several endings.

## Features

- Branching story scenes with multiple paths and endings
- Numeric choices with input validation and a quit option
- Live score and team-trust tracking
- Evidence inventory and incident-status indicators
- Outcomes that reflect the decisions you made
- Replay support
- Persistent career record with completed missions and best score
- No third-party dependencies and no network access

## Requirements

- Python 3.10 or newer

## Run the game

```bash
python main.py
```

On some systems, use `python3 main.py` instead.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Project files

- `main.py` — game scenes, player state, career record, input loop, and ending logic
- `career_record.json` — automatically created persistent career record (not required in a fresh checkout)
- `tests/test_game.py` — unit tests for state changes, ending selection, and career records
- `COPILOT_PROMPT.md` — a prompt for extending the project with GitHub Copilot

## GitHub Copilot challenge

Open this folder in VS Code, open `COPILOT_PROMPT.md`, and ask GitHub Copilot Chat to implement the enhancement described there. Review the proposed changes, run the game and tests, and only then update the project description to reflect what you actually kept. The core game is a starter implementation; the Copilot extension is a separate step.

## Safety note

All incidents, devices, alerts, and response actions are fictional and occur within the story. This project is a learning game, not a real incident-response tool.

## License

MIT — see `LICENSE`.
