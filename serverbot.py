import discord
import sys
import subprocess
import asyncio
import time 
import os
import socket

# Pipes data from a socket on localhost to the discord server
# Gets data from discord server and publishes it to the socket
# Set the discord token in the env variable DISCORD_TOKEN
# Make sure you give appropriate permissions to the bot

class MyClient(discord.Client):
    def __init__(self, port, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.start_server())
        self.name = name
        self.server = None
        self.port = port
        self.writers = set([])

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('$health'):
            # Health checkup
            await message.channel.send('[{}] I am awake and running!'.format(self.name))
        else:
            # Remove the ID from the data

            data = " ".join(message.content.split(" ")[1:])

            # Iterate over the list of sockets and send to each
            for writer in self.writers:
                writer.write(bytes(data, "utf-8"))
                await writer.drain()

    async def handle_client(self, reader, writer):
        """Read from client and write data to the channel"""

        self.writers.add(writer)

        while True:
            buf = await reader.read(4096)

            if len(buf) == 0:
                print(">> (BOT) Connection to localhost broken")
                break

            # Publish message to all channels
            for guild in self.guilds:
                for channel in guild.text_channels:
                    await channel.send("[{}] {}".format(self.name, buf.decode("utf-8")))

        self.writers.remove(writer)

    async def start_server(self):
        """Start a server running on port self.port"""

        print(">> (BOT) Starting server...")
        self.server = await asyncio.start_server(self.handle_client, host="localhost", port=self.port)
        
        
if (len(sys.argv) != 3):
    print("python iobot.py <port> <id>")
    exit(1)

port = int(sys.argv[1])
name = sys.argv[2]

client = MyClient(port, name)
client.run(os.environ["DISCORD_TOKEN"])
