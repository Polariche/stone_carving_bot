class Game():

    def __init__(self, guild, user):
        #self.id =  #snowflake, maybe?

        self.guild_id = guild.id
        self.user_id = user.id

        self.display_messages = set()

    def attach_message_id(self, message_id):
        self.display_messages.add(message_id)

    def remove_message(self, message_id):
        self.display_messages.remove(message_id)