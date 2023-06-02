# This example requires the 'message_content' intent.

import discord
from games.loa_stone import LOA_Stone 
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
client.option_emojis = {"1️⃣":0, "2️⃣":1, "3️⃣":2}


def generate_display_text(stonegame):
    emojis = [":black_medium_small_square:",
                   ":small_blue_diamond:",
                   ":small_orange_diamond:",
                   "◇"]

    result = stonegame.result()

    stones = stonegame.stones.copy()
    stones[2][stones[2] > 0] = 2
    stones[stones < 0] = 3

    display = '\n'.join([' '.join([emojis[c] for c in s]) for i,s in enumerate(stones)])

    result_display = f"{result[0]}/{result[1]}/{result[2]} 돌을 깎으셨습니다."
    display += "\n" + result_display

    print(stonegame.prob)

    if (stonegame.tries_total() < stonegame.max_tries()):
        prob_display = f"현재 확률: {stonegame.prob}%"
        display += " " + prob_display

    return display


async def create_game_session(client, message):
    stonegame = LOA_Stone()

    display = generate_display_text(stonegame)
    display_message = await message.channel.send(display)

    client.game = stonegame
    client.game_message = display_message

    for emoji in client.option_emojis.keys():
        await display_message.add_reaction(emoji)   


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    print (f"I have received a message: \"{message.content}\"")
    if message.author == client.user:
        return

    if message.content.startswith('돌깎') or message.content.startswith('야 돌') or message.content.startswith('야돌') or message.content.startswith('야돌'):
        await create_game_session(client, message)

        """while (stonegame.tries_total() < 20):
            
            choice = random.choice(options) # replace with user input
            stonegame.try_option(choice)
        """


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if reaction.message == client.game_message:
        print(f"My display has received an emoji: {reaction.emoji}")

        client.game.try_option(client.option_emojis[str(reaction.emoji)])

        await client.game_message.edit(content=generate_display_text(client.game))

        await reaction.remove(user)



with open(".token", "r") as f:
    token = f.readlines()[0]

client.run(token)
