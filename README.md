# Squishy
A general-purpose utility & entertainment Discord bot initially intended for my private Discord servers.

## Running Squishy

1. Grab the latest source code zip from Releases, extract it somewhere and rename it to 'squishy' (all lowercase)
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
8. Rename config.json.template -> config.json in the squishy project folder we cloned earlier. Read the Config section of this README.
9. Enable the 3 intents (Presence, Server Members, Message Content) and Press 'Reset Token'. Copy the bot token you're given, and set "bot-token" to the token in config.json.
> [!CAUTION]
> This token is how programs access your bot. **Keep it safe, and do not share it with ANYONE**, or else they can log in as the bot and **do whatever they want to your server.**
10. Now, you can open a terminal/command prompt/shell in the directory that the 'squishy' folder is in, and run `python squishy`! Required dependencies should be installed automatically.

## Why FOSS?

I believe it presents new opportunities for me, Squishy, and the servers I/others use her in. I hate freemium Discord bots that charge you for features that you would just expect to come normally, so I decided to write my own bot and self-host her.

## Why not host her, and allow people to add her to their server?

I can't afford to host a bot for however many servers to use. And this way, people can customise her code to add their own features or things they would like for their server (although under the AGPL-3.0 license, the modified source code must be made public to users of your version of the bot).

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
- - `custom` Your custom status
- `modules` What modules you'd like enabled
- - `quotes` See quotes README
- - `economy` See economy README
- - `stars` See stars README
- - `moderation` See moderation README
- - `levelling` See levelling README
- - `fun` See fun README
- - `welcomer` See welcomer README
- - `customs` Your custom modules - See customs README
- `analytics` Opt-in analytics of the bot. See the Analytics section of this README. (would appreciate it if you left this, and its options, on :3)

## Analytics

Analytics are opt-in, and are disabled by default, but help me to get an idea of how many people use the bot. I like Squishy, and she's a personal passion project of mine. I'll always continue maintaining her for myself, but seeing that people are actually *using* my bot is a massive boost to my self-esteem and helps motivate me to keep working on her. These analytics are **publicly viewable** as they're just sent to an https://ntfy.sh channel. I don't have the place to host nor the capacity to write my own analytics server. The data that analytics transmits are: your server ID, how many members it has, your instances user ID, and its username. The server ID and members are just for me to get a general idea of how many people are using squishy, and and your instances user ID and username is for me to see how Squishy is being used/branded. Again, this is opt-in, and publicly viewable, but a massive help and motivation boost for me.

## License

This project is licensed under the AGPL-3.0.
Additional attribution requirements apply — see the `NOTICE` file for details.