import discord
import sys
import subprocess
import asyncio
import time 
import os

# Echo output of a script to a discord server with a new channel
# Set the discord token in the env variable DISCORD_TOKEN
# Make sure you give appropriate permissions to the bot

class MyClient(discord.Client):
    def __init__(self, cmd, channel_name, desc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = channel_name + time.strftime("%Y%m%d-%H%M%S")
        self.cmd = cmd
        self.desc = desc
        self.channel = None
        self.bg_task = self.loop.create_task(self.background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author == client.user:
            return

        # Health checkup
        if message.content.startswith('$health'):
            await message.channel.send('{} - I am awake and running!'.format(channel_name))

    async def background_task(self):
        print(">> (BOT) Running process...")
        await self.wait_until_ready()

        # Create a new channel 
        for guild in self.guilds:
            print(">> (BOT) Creating channel...{}".format(guild))
            self.channel = await guild.create_text_channel(self.channel_name)
            await self.channel.send("Hello I am running the command '{}'".format(self.cmd))
            await self.channel.send("This command does the following - {}".format(self.desc))
            print(">> (BOT) Done...")
            break 
    
        print(">> (BOT) Starting the process...")
        proc = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            output = proc.stdout.readline().decode('utf-8')

            if output == '' and proc.poll() is not None:
                break
            if output:
                await self.channel.send(output)
                sys.stdout.write(output)
        
        output = proc.stderr.read().decode('utf-8')

        if output != '':
            await self.channel.send("STDERR: " + output)
            sys.stdout.write(output)
        
        if proc.returncode == 0:
            print("Process exited normally")
            await self.channel.send("Process exited normally. I'm leaving :)")
        else:
            print("Process exited with code {}".format(proc.returncode))
            await self.channel.send("Process exited with code {}. I'm leaving :(".format(proc.returncode))
        
        print(">> (BOT) Finished program")
        exit(0)

if (len(sys.argv) != 4):
    print("python iobot.py <cmd> <channel name> <desc>")
    exit(1)

cmd = sys.argv[1]
channel_name = sys.argv[2]
desc = sys.argv[3]

client = MyClient(cmd, channel_name, desc)
client.run(os.environ["DISCORD_TOKEN"])
