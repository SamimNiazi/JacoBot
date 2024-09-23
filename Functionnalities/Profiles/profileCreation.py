from main import mongoClient

async def create(message):
    collection = mongoClient.users['UserProfiles']

    if collection.find({"discord_id":message.author.id }) :
        await message.channel.send("You already have a profile")
        return

    collection.insert_one(
        {
            "discord_id": message.author.id,
            "discord_name": message.author.name,
        }
    )
    await message.channel.send("You have been added to the database")

