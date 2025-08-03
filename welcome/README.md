# welcome
Module to welcome, say goodbye to, and roast banned members.

## Config
- `welcome` Whether or not to enable the welcome message
- - `channel` Whether or not to post the welcome message to a channel
- - `channel-id` The ID of the channel to post the welcome message to
- - `dm` What to DM the member on join
- - - `enabled` If the member should be DM'd
- - - `content` The plaintext message to be sent
- - - `embeds` The list of embeds to be sent 
- - `content` The plaintext message to be sent
- - `embeds` The list of embeds to be sent (Supports [Discohook embeds](https://discohook.app/?data=eyJ2ZXJzaW9uIjoiZDIiLCJtZXNzYWdlcyI6W3siX2lkIjoiMzBrTDJtSVBuZSIsImRhdGEiOnsiZW1iZWRzIjpbeyJhdXRob3IiOnsibmFtZSI6IlNxdWlzaHkiLCJpY29uX3VybCI6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9lbmhhbmNlZHJvY2svZW5oYW5jZWRyb2NrL3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJ0aXRsZSI6IldlbGNvbWUhIiwiY29sb3IiOjM0NDcwMDMsImRlc2NyaXB0aW9uIjoiV2VsY29tZSB0byB0aGUgc2VydmVyLCB7dXNlci5tZW50aW9ufSEgV2UncmUgaGFwcHkgdG8gaGF2ZSB5b3UgaGVyZSEgOjMiLCJmaWVsZHMiOlt7Im5hbWUiOiJIZXkhISIsInZhbHVlIjoiSGVyZSBhcmUgc29tZSB0aGluZ3MgdG8gZG8uLiJ9LHsibmFtZSI6IlJlYWQgdGhlIHJ1bGVzISIsInZhbHVlIjoiVGhleSdsbCBjb21lIGluIGhhbmR5LiIsImlubGluZSI6dHJ1ZX0seyJuYW1lIjoiQ2hlY2sgdGhlIEZBUSEiLCJ2YWx1ZSI6IkFueSBpc3N1ZXMgb3IgcXVlc3Rpb25zIHlvdSBoYXZlIG1pZ2h0IGJlIHRoZXJlLiIsImlubGluZSI6dHJ1ZX0seyJuYW1lIjoiSW50cm9kdWNlIHlvdXJzZWxmISIsInZhbHVlIjoiSXQnbGwgaGVscCBwZW9wbGUgc3RyaWtlIHVwIGEgY29udmVyc2F0aW9uIHdpdGggeW91LiIsImlubGluZSI6dHJ1ZX1dLCJpbWFnZSI6eyJ1cmwiOiJodHRwczovL2dpdGh1Yi5jb20vZW5oYW5jZWRyb2NrL2VuaGFuY2Vkcm9jay9yYXcvcmVmcy9oZWFkcy9tYWluL3NxdWlzaHlwZnAucG5nIn0sInRodW1ibmFpbCI6eyJ1cmwiOiJodHRwczovL2dpdGh1Yi5jb20vZW5oYW5jZWRyb2NrL2VuaGFuY2Vkcm9jay9yYXcvcmVmcy9oZWFkcy9tYWluL3NxdWlzaHlwZnAucG5nIn0sImZvb3RlciI6eyJ0ZXh0IjoiWW91IGFyZSBvdXIge21lbWJlcmNvdW50LmZvcm1hdH0gbWVtYmVyISIsImljb25fdXJsIjoiaHR0cHM6Ly9naXRodWIuY29tL2VuaGFuY2Vkcm9jay9lbmhhbmNlZHJvY2svcmF3L3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJ0aW1lc3RhbXAiOiIyMDI1LTA3LTE3VDEwOjQ5OjMzLjkwOVoifV19fV19) - but not multiple images/galleries)
- `goodbye` Whether or not to enable the goodbye message
- - `channel` Whether or not to post the welcome message to a channel
- - `channel-id` The ID of the channel to post the welcome message to
- - `content` The plaintext message to be sent
- - `embeds` The list of embeds to be sent (Supports [Discohook embeds](https://discohook.app/?data=eyJ2ZXJzaW9uIjoiZDIiLCJtZXNzYWdlcyI6W3siX2lkIjoiZXIxTzh1QzkweiIsImRhdGEiOnsiZW1iZWRzIjpbeyJhdXRob3IiOnsibmFtZSI6IlNxdWlzaHkiLCJpY29uX3VybCI6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9lbmhhbmNlZHJvY2svZW5oYW5jZWRyb2NrL3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJ0aXRsZSI6IkZhcmV3ZWxsISIsImNvbG9yIjozNDQ3MDAzLCJkZXNjcmlwdGlvbiI6IlNlZW1zIGxpa2Uge3VzZXIubWVudGlvbn0gbGVmdC4gSXQgd2FzIG5pY2Uga25vd2luZyB5b3UhIiwiZmllbGRzIjpbXSwiaW1hZ2UiOnsidXJsIjoiaHR0cHM6Ly9naXRodWIuY29tL2VuaGFuY2Vkcm9jay9lbmhhbmNlZHJvY2svcmF3L3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJ0aHVtYm5haWwiOnsidXJsIjoiaHR0cHM6Ly9naXRodWIuY29tL2VuaGFuY2Vkcm9jay9lbmhhbmNlZHJvY2svcmF3L3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJmb290ZXIiOnsidGV4dCI6IldlIG5vdyBoYXZlIHttZW1iZXJjb3VudH0gbWVtYmVycy4iLCJpY29uX3VybCI6Imh0dHBzOi8vZ2l0aHViLmNvbS9lbmhhbmNlZHJvY2svZW5oYW5jZWRyb2NrL3Jhdy9yZWZzL2hlYWRzL21haW4vc3F1aXNoeXBmcC5wbmcifSwidGltZXN0YW1wIjoiMjAyNS0wNy0xN1QxMDo0OTozMy45MDlaIn1dfX1dfQ) - but not multiple images/galleries)
- `banned` Whether or not to enable the banned message
- - `channel` Whether or not to post the welcome message to a channel
- - `channel-id` The ID of the channel to post the welcome message to
- - `content` The plaintext message to be sent
- - `embeds` The list of embeds to be sent (Supports [Discohook embeds](https://discohook.app/?data=eyJ2ZXJzaW9uIjoiZDIiLCJtZXNzYWdlcyI6W3siX2lkIjoiZXIxTzh1QzkweiIsImRhdGEiOnsiZW1iZWRzIjpbeyJhdXRob3IiOnsibmFtZSI6IlNxdWlzaHkiLCJpY29uX3VybCI6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9lbmhhbmNlZHJvY2svZW5oYW5jZWRyb2NrL3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJ0aXRsZSI6IkZhcmV3ZWxsISIsImNvbG9yIjozNDQ3MDAzLCJkZXNjcmlwdGlvbiI6IlNlZW1zIGxpa2Uge3VzZXIubWVudGlvbn0gZ290IGJhbm5lZC4gSXQgcHJvYmFibHkgd2Fzbid0IG5pY2Uga25vd2luZyB5b3UuIiwiZmllbGRzIjpbXSwiaW1hZ2UiOnsidXJsIjoiaHR0cHM6Ly9naXRodWIuY29tL2VuaGFuY2Vkcm9jay9lbmhhbmNlZHJvY2svcmF3L3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJ0aHVtYm5haWwiOnsidXJsIjoiaHR0cHM6Ly9naXRodWIuY29tL2VuaGFuY2Vkcm9jay9lbmhhbmNlZHJvY2svcmF3L3JlZnMvaGVhZHMvbWFpbi9zcXVpc2h5cGZwLnBuZyJ9LCJmb290ZXIiOnsidGV4dCI6IldlIG5vdyBoYXZlIHttZW1iZXJjb3VudH0gbWVtYmVycy4iLCJpY29uX3VybCI6Imh0dHBzOi8vZ2l0aHViLmNvbS9lbmhhbmNlZHJvY2svZW5oYW5jZWRyb2NrL3Jhdy9yZWZzL2hlYWRzL21haW4vc3F1aXNoeXBmcC5wbmcifSwidGltZXN0YW1wIjoie3RpbWV9In1dfX1dfQ) - but not multiple images/galleries)

## Variables
You can insert these into any text field, and Squishy will replace them with its corresponding value.
| Variable             | Explanation                                       | Sample value             |
|----------------------|---------------------------------------------------|--------------------------|
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