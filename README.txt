Hit or Stand

A Pygame survival game with a safe house, weapon and pet upgrades, and casino minigames.

Setup (Python 3.12)

Use Python 3.12 for the pinned dependencies. From the repository root, using uv:

    uv python install 3.12
    uv venv --python 3.12 .venv312
    uv pip install --python .venv312/bin/python -r requirements.txt
    ./.venv312/bin/python Game/main.py

If Python 3.12 is already installed, the standard-library alternative is:

    python3.12 -m venv .venv312
    .venv312/bin/python -m pip install -r requirements.txt
    .venv312/bin/python Game/main.py

On Windows, use .venv312\Scripts\python.exe instead of .venv312/bin/python.
In VS Code, select the virtual environment's Python interpreter and use Run Python File in Terminal.
Fish activation is optional: source .venv312/bin/activate.fish

Controls

- WASD: move. Space: dash once unlocked. Number keys 1-5: select purchased weapons.
- Weapons and the pet fire automatically in battle.
- Escape: pause. The main menu includes a guided tutorial.
- Drag the visible bottom-right corner handle to resize at 16:9; side resizing is disabled.
- Options > Fullscreen, F11, or Alt+Enter toggles fullscreen.
- Fullscreen preserves the artwork's proportions, adding black bars when needed.
- Music volume, fullscreen and window size are saved automatically and restored at startup.
- Type motherload anywhere (no Enter needed) to add 10,000 coins. The code is repeatable
  and rewards are saved immediately.

Progress

Upgrades and records are stored in ~/.hitorstand/player_progress.json on Linux/macOS,
or %APPDATA%\.hitorstand\player_progress.json on Windows. Options > Reset Progress
resets gameplay progress while keeping your window and audio preferences.
The virtual environment is independent of saved game progress.

Windows builds from Linux

Push your changes, open Actions > Build Windows EXE > Run workflow on GitHub.
GitHub builds the game on a Windows runner using Python 3.12. When the run is
green, open it and download HitOrStand-Windows from Artifacts. Extract the ZIP
and attach HitOrStand.exe to your GitHub Release. Python is not needed to play.

Development

Game/main.spec is the reusable PyInstaller configuration. Run it from Game/.
Build on Windows for HitOrStand.exe, or Linux for a Linux executable.
Distribute compiled downloads through GitHub Releases. Executables, build/,
dist/, virtual environments and caches stay excluded from the repository.

Original project: https://github.com/goncasfausto04/project_comp
