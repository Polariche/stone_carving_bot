# This example requires the 'message_content' intent.

from typing import Literal, Union, Optional

import discord
from discord import app_commands
from discord.ext import commands

from games.loa_stone import LOA_Stone 
import random


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
        self.games = {}
        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

async def create_game_session(interaction, permission, permission_user):
    #message = ctx.message

    # the pair of (guild_id, user_id) works as a key for the game session
    guild = interaction.guild
    user = interaction.user
    channel = interaction.channel
    
    print (f"Creating a game for ({guild.id}, {user.id})")
    #created_date = ""

    game = LOA_Stone(guild, user, permission, permission_user)
    client.games[(guild.id, user.id)] = game

    await game.create_new_display(interaction)

    return game

def load_game_session(client, user_id, guild_id):
    pass

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # This copies the global commands over to your guild.
    for guild in client.guilds:
        client.tree.copy_global_to(guild=guild)
        await client.tree.sync(guild=guild)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    # see if the (guild_id, author_id) has a game
    try:
        message = reaction.message
        guild = message.guild
        owner = message.mentions[0]
        game = client.games[(guild.id, owner.id)]

    except KeyError:
        return
    
    if reaction.message.id == game.display_id:
        print(f"My display has received an emoji: {reaction.emoji}")
        await game.reaction_input(reaction, user)

async def create_or_load(interaction, permission: Optional[Literal["모두", "나만", "이사람만"]], permission_user: Optional[Union[discord.User, discord.Role]] = None):
    try:
        game = client.games[(interaction.guild.id, interaction.user.id)]

        game.modify_permission(permission, permission_user)

        await game.create_new_display(interaction)

    except KeyError:
        game = await create_game_session(interaction, permission, permission_user)

@client.tree.command(name='돌', description="다같이 돌을 깎아봅시다! 이미 깎고 있다면 이어서 깎습니다")
async def cmd_our_game(interaction: discord.Interaction):
    await create_or_load(interaction, "모두")

@client.tree.command(name='내돌', description="나만의 돌을 깎아봅시다. 다른 사람은 노터치!!")
async def cmd_my_game(interaction: discord.Interaction):
    await create_or_load(interaction, "나만")

@client.tree.command(name='해줘', description="대신 깎아달라고 해봅시다. 나와 내가 지정한 사람들만 내 돌을 깎을 수 있게 됩니다")
async def cmd_your_game(interaction: discord.Interaction, user: Union[discord.User]):
    await create_or_load(interaction, "이사람만", user)


with open("discord.token", "r") as f:
    token = f.readlines()[0]

with open("smilegate.token", "r") as f:
    smg_api_key = f.readlines()[0]

client.run(token)