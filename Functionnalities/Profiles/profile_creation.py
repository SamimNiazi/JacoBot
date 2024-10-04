"""Module that contains all the logic for user profiles

This module contains methods related to the creation, to the storage and more of profiles
"""

from Common.constants import Constants
class Profile:
    """Profile class containing all the related methods
    Attributes:
        collection (Collection): pymongo collection that contains all user profiles.
    """
    def __init__(self):
        self.collection = Constants().mongo_client.users['UserProfiles']

    async def create(self, message):
        """Creates the profile and stores it into the collection

        Args:
            message (Message): The Message discord object that we will use to get
            context information.
        """

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

    async def delete(self):
        """Deletes the profile from the collection"""
