import discord
import sys
import subprocess
import asyncio
import time 
import os
import socket
import select

# Pipes data from STDOUT to server and from server to STDIN
# Intended to be run as a child process inside a parent process

class MyClient(discord.Client):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.io_loop())
        self.name = name
        self.server = None
        self.writers = set([])

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('$health'):
            # Health checkup
            await message.channel.send('[{}] I am awake and running!'.format(self.name))
        else:
            # Remove the ID from the data

            data = " ".join(message.content.split(" ")[1:])

            # Write to stdout
            print(data)

    async def io_loop(self):
        """Read from client and write data to the channel"""

        await self.wait_until_ready()

        while True:
            if select.select([sys.stdin], [], [], 0.0)[0]:
                buf = sys.stdin.readline()

                # Publish message to all channels
                for guild in self.guilds:
                    for channel in guild.text_channels:
                        await channel.send("[{}] {}".format(self.name, buf))
            else:
                # Check again after some time
                await asyncio.sleep(0.1)
        
        
if (len(sys.argv) != 2):
    print("python stdbot.py <name>")
    exit(1)

name = sys.argv[1]

client = MyClient(name)
client.run(os.environ["DISCORD_TOKEN"])
