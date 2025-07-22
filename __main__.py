# Squishy - A general purpose Discord bot
# Created by Enhanced Rock - (@enhancedrock, https://erock.carrd.co)
# Licensed under AGPL-3.0. Additional attribution requirements apply — see the NOTICE file for details.

import os
import subprocess

requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
if os.path.isfile(requirements_path):
    print("Checking for/installing dependencies from requirements.txt...")
    try:
        subprocess.check_call(["pip", "install", "-r", requirements_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Done!")
    except subprocess.CalledProcessError as e:
        print(f"\nFailed to install dependencies: {e}")
        exit()
else:
    print("\033[31;1mA requirements.txt was not found!!\033[0m Please ensure you didn't delete or rename the file, you can grab it off of the Github repository if it's missing.\nThe program will now exit.")
    exit()

import json
import requests
import zipfile

version = "v1.0.0" # do NOT touch this.
modified = False # if you're using your own/a modified version of Squishy, set this to True to disable auto-updates

print(f"\n\033[1mHaiii!!\033[0m\n\033[3mSquishy {version}\033[0m\nMade by \033[31;1mEnhanced Rock\033[0m\n") # as per the NOTICE, you may not remove this attribution

if not os.path.isfile(os.path.join(os.path.dirname(__file__), "config.json")):
    print("\033[31;1mA config.json was not found!!\033[0m Please read the README for setup instructions.\nThe program will now exit.")
    exit()

with open(os.path.join(os.path.dirname(__file__), "config.json"), "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

if not modified and config.get("auto-update", True):
    print("Checking for updates...")
    response = requests.get("https://api.github.com/repos/enhancedrock/squishy/releases/latest", timeout=5)
    if response.status_code == 200:
        data = response.json()
        latest_version = data.get("tag_name", "v0.0.0")
        if latest_version > version:
            print(f"Update available! {version} -> {latest_version}")
            zip_url = data.get("zipball_url")
            if zip_url:
                print("Downloading the latest version...")
                try:
                    zip_response = requests.get(zip_url, timeout=10)
                    if zip_response.status_code == 200:
                        zip_path = os.path.join(os.path.dirname(__file__), "latest_source.zip")
                        with open(zip_path, "wb") as zip_file:
                            zip_file.write(zip_response.content)
                        print("Download complete. Extracting files...")
                        with zipfile.ZipFile(zip_path, "r") as zip_ref:
                            zip_ref.extractall(os.path.dirname(__file__))
                        os.remove(zip_path)
                        print("Update applied successfully! Please restart the program.")
                        exit()
                    else:
                        print(f"Failed to download the update: {zip_response.status_code}")
                except requests.RequestException as e:
                    print(f"An error occurred while downloading the update: {e}")
            else:
                print("Failed to find the download URL for the latest version.")
        elif latest_version < version:
            print(f"You are using a newer version ({version}) than the latest release ({latest_version}). Wait, what? Don't tell me you touched the variable that says \033[1mdo NOT touch\033[0m..")
        else:
            print("You are using the latest version.")
    else:
        print(f"Failed to fetch release info: {response.status_code}")
else:
    print("This version of Squishy is marked as modified. Skipping update check.")