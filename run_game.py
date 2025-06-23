import os
import sys
import subprocess
import venv
import platform
from pathlib import Path

# Paths
venv_dir = Path("venv")
game_script = Path("src/game.py")

# 1. Create virtual environment if it doesn't exist
if not venv_dir.exists():
    print("🔧 Creating virtual environment...")
    venv.create(venv_dir, with_pip=True)

# 2. Determine platform-specific activate script and python binary
if platform.system() == "Windows":
    python_bin = venv_dir / "Scripts" / "python.exe"
    pip_bin = venv_dir / "Scripts" / "pip.exe"
else:
    python_bin = venv_dir / "bin" / "python"
    pip_bin = venv_dir / "bin" / "pip"

# 3. Install pygame
print("📦 Installing pygame...")
subprocess.check_call([str(pip_bin), "install", "--upgrade", "pip"])
subprocess.check_call([str(pip_bin), "install", "pygame"])

# 4. Run the game
print("🎮 Launching the game...")
subprocess.run([str(python_bin), str(game_script)])
