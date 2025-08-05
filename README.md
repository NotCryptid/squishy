<h1 align="center">
<img width="75" src="https://raw.githubusercontent.com/enhancedrock/enhancedrock/refs/heads/main/squishypfp.png" alt="Squishy, a blue slime girl character by @enhancedrock">

squishy
</h1>
<p align="center">
The cutest<sup>*</sup> free, open source, fully expandable, and self-hostable Discord bot. Designed to provide all the features you could ever need such as an economy, minigames, levelling, and more.
</p>
<sup>*In my subjective opinion</sup>

## Why FOSS?

I believe it presents new opportunities for me, Squishy, and the servers I/others use her in. I hate freemium Discord bots that charge you for features that you would just expect to come normally, so I decided to write my own bot and self-host her.

## Why not host her, and allow people to add her to their server?

I can't afford to host a bot for however many servers to use. And this way, people can customise her code to add their own features or things they would like for their server (although under the AGPL-3.0 license, the modified source code must be made public to users of your version of the bot).

## Hey, you said this could do everything I need, but there's no moderation!

Use Wick. It's the perfect moderation bot. If you really want it to be a part of Squishy, feel free to write an addon! Upload it to github/make a PR to add it to the bot if you want, too.

## Setup

1. Make an 'New Application' in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Optionally, give it a Profile Picture and Description, before heading to 'Installation'.
> [!NOTE]
> Squishy's normal profile picture is available in the root of the `squishy` folder as `squishypfp.png`, downloaded in step 8. Credit for this goes to Chewy/chewyffon/@chewyffon.
3. Scroll to 'Guild Install', and add the 'bot' scope, then add the 'Administrator' permission.
> [!NOTE]
> Aside from the *(togglable)* auto-updater, which only talks to Github, Squishy never communicates with anything outside of Discord or makes dangerous actions without confirmation, and therefore poses no risk to your Discord server. You may read and self-assess the code if you want.
4. Now, copy the 'Discord Provided Link', open it and add it to your server.
5. Return to the Developer Portal at the Installation tab, and change 'Discord Provided Link' to 'None'.
6. Now go to the 'Bot' section, and disable 'Public Bot'.
> [!NOTE]
> Steps 5-6 will prevent people who aren't you from using your instance of Squishy, as she's only designed to work in 1 server at a time.
7. Enable the 3 intents (Presence, Server Members, Message Content) and press 'Reset Token'. Copy your bot token you're given.
> [!CAUTION]
> This token is how programs access your bot. **Keep it safe, and do not share it with ANYONE**, or else they can log in as the bot and **do whatever they want to your server.**
8. Download the latest source code zip from the [releases](https://github.com/enhancedrock/squishy/releases), and extract it somewhere, renaming the folder to `squishy`
9. Duplicate `config.json.template`, changing the duplicates name to `config.json`
10. In your new `config.json`, set `bot-token` to the toke we got in step 7, and `server-id` to the server you plan on using Squishy in.
11. Now, configure any settings you'd like (See the Config section of the README), enable any modules, and configure them (See their individual READMEs)
12. Open a terminal in the the `squishy` folder and run `python3 -m venv .`

## Running Squishy
That's it! CD into her directory, activate the virtual enviornment and run `python3 .` to start her.

## Config

- `bot-token` The token for your bot
- `server-id` The ID of your server that you plan to add Squishy to
- `update-checker` Whether or not Squishy shoudl check for updates on start
- `auto-updater` Whether or not Squishy should update on start
- `status-interval` How often Squishy should rotate through her statuses (in seconds)
- `statuses` The enabled statuses for Squishy to rotate through
- - `member-count` "Watching {members} members"
- - `role-count` "Watching {roles} roles"
- - `channel-count` "Watching {channels} channels"
- - `github` "Watching github.com/enhancedrock/squishy" (would appreciate it if you left this on :3)
- - `custom-enabled` If your custom status should be included in the rotation
- - `custom-type` If your custom status should use 1 for playing, 2 for watching, 3 for listening, and 4 for a standard status
- - `custom` Your custom status
- `online` Whether Squishy should be: 1 for Online, 2 for Idle, 3 for Do not Disturb, 4 for Invisible
- `modules` What modules you'd like enabled
- - `quotes` See quotes README
- - `economy` See economy README
- - `stars` See stars README
- - `moderation` See moderation README
- - `levelling` See levelling README
- - `fun` See fun README
- - `welcomer` See welcomer README
- - `autoroles` See autoroles README
- - `reactroles` See reactroles README
- - `messagebuilder` See messagebuilder README
- - `customs` Your custom modules - See customs README

## License

This project is licensed under the AGPL-3.0.
Additional attribution requirements apply — see the `NOTICE` file for details.