import os
import sys
import subprocess

# Locate pyinstaller.exe dynamically
scripts_dir = os.path.join(sys.prefix, "Scripts")
user_scripts_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", f"Python{sys.version_info.major}{sys.version_info.minor}", "Scripts")

pyinstaller_path = os.path.join(user_scripts_dir, "pyinstaller.exe")

if not os.path.exists(pyinstaller_path):
    pyinstaller_path = os.path.join(scripts_dir, "pyinstaller.exe")

if not os.path.exists(pyinstaller_path):
    print("Could not find pyinstaller.exe automatically.")
    print("Reinstalling PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "pyinstaller"])

# Execute the build command
cmd = [pyinstaller_path, "--onefile", "--name=tomlifier", "tomlify.py"]
print(f"Running command: {' '.join(cmd)}")
subprocess.run(cmd)