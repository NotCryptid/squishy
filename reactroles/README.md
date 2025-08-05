# reactroles
Assign roles to members based on message reactions.

## Config
Each message where you want reactroles is defined as a key. Like so:
```
"1402010066776756344": {
    [...]
}
```
Within that, an emoji (not the name of an emoji), followed by the ID of the role that emoji should give when reacted to. Like so:
```
"1402010066776756344": {
    "1️⃣": 1396790366933483599
}
```
If you would like for Squishy to react to your messages with the emojis, and retroactively apply roles to anyone who reacted while the bot was offline, you must add a "channel" key to the dictionary. Like so:
```
"1402010066776756344": {
    "channel": 1402009175118319668,
    "1️⃣": 1396790366933483599
}
```