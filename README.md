# Squishy
A general-purpose utility & entertainment Discord bot initially intended for my private Discord servers.

## Running Squishy

1. Clone Squishy by running `git clone https://github.com/enhancedrock/squishy.git squishy`.
2. Make an 'New Application' in the [Discord Developer Portal](https://discord.com/developers/applications).
3. Optionally, give it a Profile Picture and Description, before heading to 'Installation'.
> [!NOTE]
> Squishy's normal profile picture is available in the root of the squishy project folder we cloned earlier. Credit for this goes to Chewy/chewyffon/@chewyffon.
4. Scroll to 'Guild Install', and add the 'bot' scope, then add the 'Administrator' permission.
> [!NOTE]
> Aside from the *(togglable)* auto-updater, which only talks to Github, Squishy never communicates with anything outside of Discord or makes dangerous actions without confirmation, and therefore poses no risk to your Discord server. You may read and self-assess the code if you want.
5. Now, copy the 'Discord Provided Link', open it and add it to your server.
6. Return to the Developer Portal at the Installation tab, and change it 'Discord Provided Link' to 'None'.
7. Now go to the 'Bot' section, and disable 'Public Bot'.
> [!NOTE]
> These 2 steps will prevent people who aren't you from using your instance of Squishy, as she's only designed to work in 1 server at a time.
8. Rename config.json.template -> config.json in the squishy project folder we cloned earlier.
9. Enable the 3 intents (Presence, Server Members, Message Content) and Press 'Reset Token'. Copy the bot token you're given, and set "bot-token" to the token in config.json.
> [!CAUTION]
> This token is how programs access your bot. **Keep it safe, and do not share it with ANYONE**, or else they can log in as the bot and **do whatever they want to your server.**
10. Now, you can open a terminal/command prompt/shell in the directory that the squishy project folder is in, and run `python squishy`! Required dependencies should be installed automatically.

## Why FOSS?

I believe it presents new opportunities for me, Squishy, and the servers I/others use her in. I hate freemium Discord bots that charge you for features that you would just expect to come normally, so I decided to write my own bot and self-host her.

## Why not host her, and allow people to add her to their server?

I can't afford to host a bot for however many servers to use. And this way, people can customise her code to add their own features or things they would like for their server (although under the AGPL-3.0 license, the modified source code must be made public to users of your version of the bot).

## License

This project is licensed under the AGPL-3.0.
Additional attribution requirements apply — see the `NOTICE` file for details.