import asyncio
import discord

from Functionnalities.Profiles.profileCreation import create


async def calendar(message, mongo_client):
    collection = mongo_client.users['UserProfiles']
    query = {"discord_id":message.author.id }

    if not collection.find_one(query):
        await create(message, mongo_client)

    user_calendar = collection.find_one(query, projection={'_id': 0, "calendar": 1})
    embed = create_calendar_embed(user_calendar['calendar'], message)
    await message.channel.send(embed=embed)



async def add_date_to_calendar(message, client, mongo_client):
    collection = mongo_client.users['UserProfiles']

    await calendar(message, mongo_client)

    await message.channel.send("Please send the date")
    reply_event_date = await wait_for_reply(message, client)
    if not reply_event_date: return
    await message.channel.send("What is this date for?")
    reply_event_name = await wait_for_reply(message, client)
    if not reply_event_name: return

    collection.update_one({"discord_id":message.author.id }, {"$addToSet": { "calendar": [ reply_event_date.content, reply_event_name.content ] } })
    await message.channel.send("Your date has been added to the calendar")


async def wait_for_reply(message, client):

    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        reply = await client.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        # If the user doesn't reply within the timeout period
        await message.channel.send("You took too long to reply, please try again.")
        return
    return reply

def create_calendar_embed(dates, message) :

    em = discord.Embed(title = "Here's your upcoming events!" )
    events = ""
    for date in dates:
        events += "- " + "**" + date[0] + ":**   " + date[1] + "\n"
    em.description = events
    em.set_thumbnail(url=message.author.avatar)
    return em


