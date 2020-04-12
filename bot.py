import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$channel'):
        channel_name = message.content.split()[1]
        await message.guild.create_text_channel(channel_name)
        await message.channel.send('Created text channel {}!'.format(channel_name))

client.run('Njk4OTEzNzcxNTk4NjQzMjYy.XpMwUg.dDQgXdMbVuBkd6mNvOTUYR3UhPY')

# import subprocess
# import sys

# proc = subprocess.Popen(sys.argv[1].split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# while True:
#     output = proc.stdout.readline().decode('utf-8')
#     if output == '' and proc.poll() is not None:
#         break
#     if output:
#         sys.stdout.write(output)

# output = proc.stderr.read().decode('utf-8')
# sys.stdout.write(output)
# if proc.returncode == 0:
#     print("Process exited normally")
# else:
#     print("Process exited with code {}".format(proc.returncode))
