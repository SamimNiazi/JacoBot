async def create(message, mongoClient):
    collection = mongoClient.users['UserProfiles']
    if collection.find_one({"discord_id":message.author.id }) :
        await message.channel.send("You already have a profile")
        return

    collection.insert_one(
        {
            "discord_id": message.author.id,
            "discord_name": message.author.name,
            "calendar": []
        }
    )
    await message.channel.send("You have been added to the database")

