# Squishy - A general purpose Discord bot
# Created by Enhanced Rock - (@enhancedrock, https://erock.carrd.co)
# Licensed under AGPL-3.0. Additional attribution requirements apply — see the NOTICE file for details.

import requests

version = "v1.0.0" # do NOT touch this.
modified = False # if you're using your own/a modified version of Squishy, set this to True to disable auto-updates

print(f"\n\033[1mHaiii!!\033[0m\n\033[3mSquishy {version}\033[0m\nMade by \033[31;1mEnhanced Rock\033[0m\n") # as per the NOTICE, you may not remove this attribution

if not modified:
    print("Checking for updates...")
    response = requests.get("https://api.github.com/repos/enhancedrock/squishy/releases/latest", timeout=5)
    if response.status_code == 200:
        data = response.json()
        latest_version = data.get("tag_name", "v0.0.0")
        if latest_version > version:
            print(f"Update available: {latest_version}. You are using {version}.")
        elif latest_version < version:
            print(f"You are using a newer version ({version}) than the latest release ({latest_version}). Wait, what? Don't tell me you touched the variable that says \033[1mdo NOT touch\033[0m..")
        else:
            print("You are using the latest version.")
        
    else:
        print(f"Failed to fetch release info: {response.status_code}")

else:
    print("This version of Squishy is marked as modified. Skipping update check.")