# This example requires the 'message_content' intent.

import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

key_path = os.environ['DISCORD_KEY']
with open(key_path, "r") as f:
    key = f.readlines()[0]

client.run(key)
