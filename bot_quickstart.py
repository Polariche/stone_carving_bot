# This example requires the 'message_content' intent.

import discord
from games.loa_stone import LOA_Stone 
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

client.games = {}

async def create_game_session(client, message):
    # the pair of (guild_id, user_id) works as a key for the game session
    guild = message.guild   
    user = message.author
    
    print (f"Creating a game for ({guild.id}, {user.id})")
    #created_date = ""

    game = LOA_Stone(guild, user)
    client.games[(guild.id, user.id)] = game

    display = game.generate_display_text()
    display_message = await message.channel.send(display)

    game.attach_message_id(display_message.id)

    for emoji in game.option_emojis.keys():
        await display_message.add_reaction(emoji)   


def load_game_session(client, user_id, guild_id):
    pass


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    print (f"I have received a message: \"{message.content}\"")
    if message.author == client.user:
        return

    if message.content.startswith('테스트'):
        await create_game_session(client, message)


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
    
    if reaction.message.id in game.display_messages:
    
        print(f"My display has received an emoji: {reaction.emoji}")

        game.play_option(game.emoji_to_option(reaction.emoji))
        await message.edit(content=game.generate_display_text())

        await reaction.remove(user)



with open(".token", "r") as f:
    token = f.readlines()[0]

client.run(token)
