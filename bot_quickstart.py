# This example requires the 'message_content' intent.

import discord
from discord import app_commands
from discord.ext import commands

from games.loa_stone import LOA_Stone 
import random

MY_GUILD = discord.Object(id=1005844989076586496)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
        self.games = {}

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

async def create_game_session(interaction):
    #message = ctx.message

    # the pair of (guild_id, user_id) works as a key for the game session
    guild = interaction.guild
    user = interaction.user
    channel = interaction.channel
    
    print (f"Creating a game for ({guild.id}, {user.id})")
    #created_date = ""

    game = LOA_Stone(guild, user)
    client.games[(guild.id, user.id)] = game

    await game.create_new_display(interaction)

    return game

def load_game_session(client, user_id, guild_id):
    pass

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    message = reaction.message
    guild = message.guild
    owner = message.mentions[0]

    # see if the (guild_id, author_id) has a game
    try:
        game = client.games[(guild.id, owner.id)]

    except KeyError:
        return
    
    if reaction.message.id == game.display_id:
        print(f"My display has received an emoji: {reaction.emoji}")

        await game.reaction_input(reaction, user)

@client.tree.command(name='새돌', description="새 돌을 깎아봅시다")
async def cmd_create_new_game(interaction: discord.Interaction):
    await create_game_session(interaction)

@client.tree.command(name='돌', description="돌을 깎아봅시다. 이미 깎고 있다면 이어서 깎습니다")
async def cmd_show_game(interaction: discord.Interaction):
    try:
        game = client.games[(interaction.guild.id, interaction.user.id)]
        await game.create_new_display(interaction)

    except KeyError:
        game = await create_game_session(interaction)


with open(".token", "r") as f:
    token = f.readlines()[0]

client.run(token)