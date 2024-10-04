from Common.constants import Constants
class Profile:

    def __init__(self):
        self.mongo_client = Constants().mongo_client
        self.collection = self.mongo_client.users['UserProfiles']

    async def create(self, message):
        if self.collection.find_one({"discord_id":message.author.id }) :
            await message.channel.send("You already have a profile")
            return

        self.collection.insert_one(
            {
                "discord_id": message.author.id,
                "discord_name": message.author.name,
                "calendar": [],
                "is_calendar_ordered": False
            }
        )
        await message.channel.send("You have been added to the database")

