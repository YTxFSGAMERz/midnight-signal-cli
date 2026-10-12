# GitHub Copilot Enhancement Prompt

Paste the prompt below into GitHub Copilot Chat after opening this repository in VS Code.

---

I am extending **Midnight Signal**, a Python command-line choose-your-own-adventure game. Please inspect `main.py` and `tests/test_game.py` before making changes.

Implement a small persistent **career record** feature using only Python's standard library:

1. Save the player's best score and number of completed missions to a JSON file named `career_record.json` in the project directory.
2. Load that record when the game starts. If the file does not exist, is invalid JSON, or contains invalid data, start with a safe default and do not crash.
3. Update the record only when a mission reaches an ending, not when the player quits midway.
4. Keep the feature command-line based and integrate it with the existing replay flow.
5. Add unit tests covering a missing file, valid record, malformed JSON, and updating a best score.
6. Keep functions small and testable. Use `pathlib` and `json`; don't install dependencies, add network access, or rewrite the game architecture.
7. Tell me which files you changed and how to run the tests. Do not claim the changes are complete until you have actually implemented them.

First propose a brief plan, then implement the feature and run the tests if your environment supports it.

---

After Copilot makes changes, inspect the diff and run the game. Only keep the changes if they work.
