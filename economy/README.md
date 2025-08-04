# welcome
Module to allow members to own & manage a virtual a currency

## Config
- `max-bal` The maximum amount of currency members can have (0 = off)
- `payments` If members can send money to eachother
- `max-payment-amount` How much money can be sent in a payment
- `currency-symbol` The symbol for your server's currency
- `currency-placement` If the symbol comes before or after the number (1 = before, 2 = after)
- `currency-name` The name of your currency (E.g. "You recieved 1 point")
- `currency-name-plural` The plural name of your currency  (E.g. "You recieved 2 points)
- `shop` The shop where members can spend their currency
- - `enabled` If the shop is enabled
- - `items` Dictionary of items, must follow this format:
```
"itemnumber": {
    "name": "Double XP Potion (5m)",
    "cost": 100,
    "description": "Grants you Double XP for 5 minutes!",
    "rewards": [
        {
            "type": "temprole",
            "value1": "1401602493581885612",
            "value2": 300
        }
    ]
}
```

## Rewards
There are 3 reward types, `role`, `temprole` and `script`. `role` grants the user a role, with the role ID being specified in `value1`. `temprole` grants the user a role for a temporary period of time, with the role ID being specified in `value1` and the duration (in seconds) being specified in `value2`. `script` attemps to execute a script from the customs/scripts folder as though it was part of the bot, meaning you can take actions like remove roles or send messages. With `script`, it automatically tries executing a function named `main()`, and passes 2 arguments: the purchaser/gift recipient's user ID, and the ID of the channel it was bought in. If it can't find a main function, it'll just try to run the Python file.