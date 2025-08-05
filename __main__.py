# Squishy - A general purpose Discord bot
# Created by Enhanced Rock - (@enhancedrock, https://erock.carrd.co)
# Licensed under AGPL-3.0. Additional attribution requirements apply
# See the NOTICE file for details.

import os
import subprocess
import json
import zipfile
import tempfile
import sys
import shutil

# venv check
if 'VIRTUAL_ENV' not in os.environ:
    print("Squishy doesn't appear to be running inside a virtual enviornment, or the VIRTUAL_ENV enviornment variable is unset. Please follow the README's setup tutorial!")
    exit()

# Install pip requirements
requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
if os.path.isfile(requirements_path):
    print("Checking for/installing dependencies from requirements.txt...")
    try:
        subprocess.check_call(["pip", "install", "-r", requirements_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Done!")
    except subprocess.CalledProcessError as e:
        print(f"\nFailed to install dependencies: {e}")
        exit()
    import requests
else:
    print("\033[31;1mA requirements.txt was not found!!\033[0m Please ensure you didn't delete or rename the file, you can grab it off of the Github repository if it's missing.\nThe program will now exit.")
    exit()

VERSION = "v2.0.1" # do NOT touch this.
MODIFIED = False # if you're using your own/a modified version of Squishy, set this to True

print(f"\n\033[1mHaiii!!\033[0m\n\033[3mSquishy {VERSION}\033[0m\nMade by \033[31;1mEnhanced Rock\033[0m\n") # as per the NOTICE, you may not remove this attribution

# Check if config.json exists
if not os.path.isfile(os.path.join(os.path.dirname(__file__), "config.json")):
    print("\033[31;1mA config.json was not found!!\033[0m Please read the README for setup instructions.\nThe program will now exit.")
    exit()

# Load the config.json
with open(os.path.join(os.path.dirname(__file__), "config.json"), "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Extract an update over the bot's code
def extract_and_replace(zip_path, target_folder):
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        # Locate the top-level extracted folder
        extracted_root = next(
            (os.path.join(tmpdir, d) for d in os.listdir(tmpdir)
             if os.path.isdir(os.path.join(tmpdir, d))),
            None
        )

        if not extracted_root:
            raise RuntimeError("Could not find the extracted root folder")

        # Copy contents over existing code
        for item in os.listdir(extracted_root):
            s = os.path.join(extracted_root, item)
            d = os.path.join(target_folder, item)

            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

# Check for updates, and update if one exists
if config.get("update-checker", True):
    print("Checking for updates...")
    response = requests.get("https://api.github.com/repos/enhancedrock/squishy/releases/latest", timeout=5)
    if response.status_code == 200:
        data = response.json()
        latest_version = data.get("tag_name", "v0.0.0")
        if latest_version > VERSION:
            print(f"Update available! {VERSION} -> {latest_version}")
            if not MODIFIED and config.get("auto-updater", True):
                zip_url = data.get("zipball_url")
                if zip_url:
                    print("Downloading the latest version...")
                    try:
                        zip_response = requests.get(zip_url, timeout=10)
                        zip_response.raise_for_status()

                        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
                            tmp_zip.write(zip_response.content)
                            tmp_zip_path = tmp_zip.name

                        # Replace the contents of the current directory
                        current_dir = os.path.dirname(__file__)
                        extract_and_replace(tmp_zip_path, current_dir)                    

                        # Run cleanup script (if exists)
                        if os.path.isfile(os.path.join(os.path.dirname(__file__), "CLEANUP.py")):
                            print("CLEANUP.py was included with this release, skipping cleanup.")
                            subprocess.run([sys.executable, "CLEANUP.py"] + sys.argv[1:], cwd=os.path.dirname(__file__), check=True)
                        else:
                            print("CLEANUP.py not found, skipping cleanup.")

                        print("Update complete! Restarting now...\n")

                        # Restart the script in-place
                        python_executable = sys.executable
                        script_path = os.path.abspath(sys.argv[0])
                        os.execv(python_executable, [python_executable, script_path] + sys.argv[1:])
                    except Exception as e:
                        print(f"Failed to download or extract update: {e}")
                else:
                    print("Failed to find the download URL for the latest version.")
            else:
                print("Auto-updater is disabled or you are using a modified version of Squishy. Please update manually by downloading the latest release from Github.")
        elif latest_version < VERSION:
            print(f"You are using a newer version ({VERSION}) than the latest release ({latest_version}). Wait, what? Don't tell me you touched the variable that says \033[1mdo NOT touch\033[0m..")
        else:
            print("You are using the latest version.")
    else:
        print(f"Failed to fetch release info: {response.status_code}")
else:
    print("Update checking is disabled in the config.json. If you want to enable it, set 'update-checker' to true in the config.json file.")

# Time to start!
print("\n\033[1mStarting Squishy...\033[0m\n")
subprocess.run([sys.executable, "squishy.py"] + sys.argv[1:], cwd=os.path.dirname(__file__), check=True)