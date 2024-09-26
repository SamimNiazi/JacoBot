import asyncio
import discord

from Functionnalities.Profiles.profileCreation import create


async def calendar(message, mongoClient):
    collection = mongoClient.users['UserProfiles']
    query = {"discord_id":message.author.id }

    if not collection.find_one(query):
        await create(message, mongoClient)

    userCalendar = collection.find_one(query, projection={'_id': 0, "calendar": 1})
    embed = createCalendarEmbed(userCalendar['calendar'], message)
    await message.channel.send(embed=embed)



async def addDateToCalendar(message, client, mongoClient):
    collection = mongoClient.users['UserProfiles']

    await calendar(message, mongoClient)

    await message.channel.send("Please send the date")
    replyEventDate = await waitForReply(message, client)
    if not replyEventDate: return
    await message.channel.send("What is this date for?")
    replyEventName = await waitForReply(message, client)
    if not replyEventName: return

    collection.update_one({"discord_id":message.author.id }, {"$addToSet": { "calendar": [ replyEventDate.content, replyEventName.content ] } })
    await message.channel.send("Your date has been added to the calendar")


async def waitForReply(message, client):

    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        reply = await client.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        # If the user doesn't reply within the timeout period
        await message.channel.send("You took too long to reply, please try again.")
        return
    return reply

def createCalendarEmbed(dates, message) :

    em = discord.Embed(title = "Here's your upcoming events!" )
    events = ""
    for date in dates:
        events += "- " + "**" + date[0] + ":**   " + date[1] + "\n"
    em.description = events
    em.set_thumbnail(url=message.author.avatar)
    return em


