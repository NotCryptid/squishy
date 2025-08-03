# catchphrase
Module to say a random line from a user-defined list when pinged.

## Config
- `quote` The list of line you wish for Squishy to pick from
- `suffix` Something to suffix all lines with
- `prefix` Something to prefix all lines with

## Variables
You can insert these into any text field, and Squishy will replace them with its corresponding value.
| Variable             | Explanation                                       | Sample value             |
|----------------------|---------------------------------------------------|--------------------------|
| {user.mention}       | Mentions the user                                 | @Ruby                    |
| {server.name}        | The server's name                                 | rockbox                  |
| {membercount}        | The server's member count                         | 500                      |