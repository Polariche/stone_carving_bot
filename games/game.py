from typing import Literal, Union, Optional
import discord

class Game():

    def __init__(self, guild, user, permission, permission_user):
        #self.id =  #snowflake, maybe?

        self.guild_id = guild.id
        self.user_id = user.id

        self.display_id = -1
        self.option_emojis = {}

        self.modify_permission(permission, permission_user)

    def modify_permission(self, permission: Optional[Literal["모두", "나만", "이사람만"]] = "모두", permission_user: Optional[Union[discord.User, discord.Role]] = None):
        if permission_user is None:
            permission_user = discord.Object(id=self.user_id)

        if permission == "이사람만" and permission_user.id == self.user_id:
            permission = "나만"

        self.permission = permission
        self.permission_user_id = permission_user.id

    def generate_display_text(self):
        return "This is a sample display for a game"

    def play_option(self, option):
        return

    def is_game_over(self):
        return False

    def reset(self):
        self.display_id = -1

    async def create_new_display(self, interaction):
        channel = interaction.channel

        if self.display_id > -1:
            try:
                prev_message = await channel.fetch_message(self.display_id)
                await prev_message.delete()
            except e:
                print(e)

        display = self.generate_display_text()
        await interaction.response.send_message(display)
        display_message = await interaction.original_response()
        
        for emoji in self.option_emojis.keys():
            await display_message.add_reaction(emoji)   

        self.display_id = display_message.id


    async def reaction_input(self, reaction, user):
        if self.check_permission(user):

            self.play_option(self.option_emojis[str(reaction.emoji)])
            await reaction.message.edit(content=self.generate_display_text())

        if self.is_game_over():
            self.reset()
            self.display_id = -1

            for emoji in reversed(self.option_emojis.keys()):
                await reaction.message.clear_reaction(emoji)  

        else:
            await reaction.remove(user)


    def check_permission(self, user):
        if self.permission == "모두":
            return True 

        if self.user_id == user.id:
            return True

        if self.permission == "이사람만" and user.id == self.permission_user_id:
            return True

        return False