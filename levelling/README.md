## levelling
A way to keep members engaged by rewarding them with XP and thus levels for engagement

## Config
- `xp` Configure the ways to earn XP
- - `formula` The formula for level XP requirements to be calculated
- - - `type` The formula type:
- - - - 1 = Linear ((level*100) + 75)
- - - - 2 = Exponential (5 * (level^2) + (level*50) + 75)
- - - - 3 = Flat (1000)
- - - `multiplier` What to * the formula by ((formula) * multiplier)
- - - `max-level` The maximum achievable level 
- - `message` Configure earning XP from messages
- - - `enabled` If members should earn XP from sending messages
- - - `min` The minimum amount of XP earned
- - - `max` The maximum amount of XP earned
- - - `cooldown` The cooldown from earning message XP
- - `voice` Configure earning XP from being in VC
- - - `enabled` If members should earn XP from being in VC
- - - `min` The minimum amount of XP earned
- - - `max` The maximum amount of XP earned
- - - `cooldown` The cooldown from earning VC XP
- - - `minimum-members` The minimum amount of members needed in a VC to earn XP
- - - `anti-afk` If a member has been muted and hasn't spoken in the VCs chat since the last cooldown, don't give them XP
- - `reaction` Configure earning XP from reaction to messages
- - - `enabled` If members should earn XP from adding reactions
- - - `min` The minimum amount of XP earned
- - - `max` The maximum amount of XP earned
- - - `cooldown` The cooldown from earning reaction XP
- `message` The message sent when a user levels up
- - `channel` Whether or not to post the welcome message to a channel
- - `channel-id` The ID of the channel to post the welcome message to
- - `dm` What to DM the member on join
- - - `enabled` If the member should be DM'd
- - - `content` The plaintext message to be sent
- - - `embeds` The list of embeds to be sent 
- - `content` The plaintext message to be sent
- - `embeds` The list of embeds to be sent (Supports [Discohook embeds](https://discohook.app/?data=eyJ2ZXJzaW9uIjoiZDIiLCJtZXNzYWdlcyI6W3siX2lkIjoiMzBrTDJtSVBuZSIsImRhdGEiOnsiZW1iZWRzIjpbeyJhdXRob3IiOnsibmFtZSI6IlNxdWlzaHkiLCJpY29uX3VybCI6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9lbmhhbmNlZHJvY2svZW5oYW5jZWRyb2NrL3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJ0aXRsZSI6IldlbGNvbWUhIiwiY29sb3IiOjM0NDcwMDMsImRlc2NyaXB0aW9uIjoiV2VsY29tZSB0byB0aGUgc2VydmVyLCB7dXNlci5tZW50aW9ufSEgV2UncmUgaGFwcHkgdG8gaGF2ZSB5b3UgaGVyZSEgOjMiLCJmaWVsZHMiOlt7Im5hbWUiOiJIZXkhISIsInZhbHVlIjoiSGVyZSBhcmUgc29tZSB0aGluZ3MgdG8gZG8uLiJ9LHsibmFtZSI6IlJlYWQgdGhlIHJ1bGVzISIsInZhbHVlIjoiVGhleSdsbCBjb21lIGluIGhhbmR5LiIsImlubGluZSI6dHJ1ZX0seyJuYW1lIjoiQ2hlY2sgdGhlIEZBUSEiLCJ2YWx1ZSI6IkFueSBpc3N1ZXMgb3IgcXVlc3Rpb25zIHlvdSBoYXZlIG1pZ2h0IGJlIHRoZXJlLiIsImlubGluZSI6dHJ1ZX0seyJuYW1lIjoiSW50cm9kdWNlIHlvdXJzZWxmISIsInZhbHVlIjoiSXQnbGwgaGVscCBwZW9wbGUgc3RyaWtlIHVwIGEgY29udmVyc2F0aW9uIHdpdGggeW91LiIsImlubGluZSI6dHJ1ZX1dLCJpbWFnZSI6eyJ1cmwiOiJodHRwczovL2dpdGh1Yi5jb20vZW5oYW5jZWRyb2NrL2VuaGFuY2Vkcm9jay9yYXcvcmVmcy9oZWFkcy9tYWluL3NxdWlzaHlwZnAucG5nIn0sInRodW1ibmFpbCI6eyJ1cmwiOiJodHRwczovL2dpdGh1Yi5jb20vZW5oYW5jZWRyb2NrL2VuaGFuY2Vkcm9jay9yYXcvcmVmcy9oZWFkcy9tYWluL3NxdWlzaHlwZnAucG5nIn0sImZvb3RlciI6eyJ0ZXh0IjoiWW91IGFyZSBvdXIge21lbWJlcmNvdW50LmZvcm1hdH0gbWVtYmVyISIsImljb25fdXJsIjoiaHR0cHM6Ly9naXRodWIuY29tL2VuaGFuY2Vkcm9jay9lbmhhbmNlZHJvY2svcmF3L3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJ0aW1lc3RhbXAiOiIyMDI1LTA3LTE3VDEwOjQ5OjMzLjkwOVoifV19fV19) - but not multiple images/galleries)
- `leaderboard` Leaderboard configuration
- - `enabled` If the leaderboard is enabled
- - `entires` The top x members to show
- `rewards` Level up rewards
- - `currency` If currency should be rewarded on level up (requires economy)
- - - `every-x-level` Grant the currency reward every x levels
- - - `min` The minimum amount of currency earned
- - - `max` The maximum amount of currency earned
- - Define any level rewards here by adding `"LEVEL": [LISTOFROLEIDS]` (It MUST be a list of Role IDs, even if there's only one role)
- `boosters` Boosts to XP earning
- - `effort` If members should earn more xp for message 'effort'
- - - `enabled` If the effort booster is on
- - - `words` Every x words, boost XP earnings by `percent`
- - - `percent` Every x words, boost XP earnings by `percent`
- - `roles` Roles that should be granted an XP booster
- - - Define roles here as `"ROLEID": BOOST%"`
- - `channel` Channels that should be granted an XP booster
- - - Define channels here as `"CHANNELID": BOOST%`
- `restrictions` Restrictions on who can earn XP/when XP can be earned
- - `blacklist` Blacklist these channels/roles
- - - `enabled` Enables the blacklist
- - - `channels` A list of channels that XP cannot be earned in
- - - `roles` A list of roles that XP cannot be earned in

## Variables
You can insert these into any text field, and Squishy will replace them with its corresponding value.
| Variable             | Explanation                                       | Sample value             |
|----------------------|---------------------------------------------------|--------------------------|
| {user.xp}            | The users XP                                      | 300                      |
| {user.lvl}           | The users level                                   | 3                        |
| {user.at}            | The users @                                       | enhancedrock             |
| {user.id}            | The users ID                                      | 1230142509947293809      |
| {user.display}       | The users display name                            | Ruby                     |
| {user.mention}       | Mentions the user                                 | @Ruby                    |
| {user.avatar}        | The user's avatar URL                             | cdn.discordapp.com/...   |
| {server.name}        | The server's name                                 | rockbox                  |
| {server.id}          | The server's ID                                   | 1396790366409326602      |
| {server.icon}        | The server's icon URL                             | cdn.discordapp.com/...   |
| {membercount}        | The server's member count after the event         | 500                      |
| {membercount.format} | The server's member count formatted as an ordinal | 500th                    |
| {time}               | The current time                                  | 1753456831               |
| {time.iso}           | The time in ISO, for a footer                     | 2025-06-19T23:00:00.000Z |