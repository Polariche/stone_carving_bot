class Game():

    def __init__(self, guild, user):
        #self.id =  #snowflake, maybe?

        self.guild_id = guild.id
        self.user_id = user.id

        self.display_id = -1
        self.option_emojis = {}

    def generate_display_text(self):
        return "This is a sample display for a game"

    def play_option(self, option):
        return

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
        self.play_option(self.option_emojis[str(reaction.emoji)])

        await reaction.message.edit(content=self.generate_display_text())
        await reaction.remove(user)