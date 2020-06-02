# Discord-Logger 

## A variety of discord bots which log script output to a discord server

Sometimes when running long scripts on multiple servers it is useful to log the output in a single place. These Discord bots do just that. Currently there are only two, more ideas are highly appreciated

## Usage

To run these bots, you must install the [discordpy library](https://discordpy.readthedocs.io/en/latest/). Additionally, note that these bots only work on Python3. Further, before running you must set a environment variable `DISCORD_TOKEN` containing the token of your server. There's a guide [here] on how to create a bot and obtain a token. Note that you need to give your bot permission to read/write messages and manage channels. 

### iobot

This bot can be used to invoke a script as a subprocess and log STDOUT and STDERR to discord. Usage

```
python3 iobot.py <cmd> <channel name> <description>
```

where `<cmd>` is the shell command you want to execute, `<channel name>` denotes the name of the new channel the bot will create (it appends the current time to the channel name to avoid name collisions), and `<description>` is a small description of what the script does. The bot logs this description when it creates the channel. `test.sh` is a script which prints random english words every second. You can test this bot as follows

```
export DISCORD_TOKEN=<your token>
python3 iobot.py "bash test.sh" "wordy-process" "This process generates random words"
```

### serverbot

This bot enables two-way communication between many bots on a single channel. Essentially, it opens a server on a specified local port. Whenever a message arrives on the discord server it is forward to all connections on the local machine. Conversely, any data sent on a socket to the local server is copied to the discord server. 

Usage

```
export DISCORD_TOKEN=<your token>
python3 serverbot.py <port> <name>
```

where `<name>` is the ID of the bot, which is prefixed before each message and `<port>` is the local port number where the bot is going to run. 

Example

On one terminal, start the bot

```
python3 serverbot.py 1337 logomaniac
```

On the other open a connection to port 1337 and pipe the output of `test.sh`

```
bash test.sh | nc localhost 1337
```

Your discord server should now have periodic messages containing obscure words. If you type any message in the channel, the bot will split on whitespace, remove the first word and print the message on the terminal running `test.sh`. Eg. if you type `hello world`, you should get `world` printed on the second terminal. 
