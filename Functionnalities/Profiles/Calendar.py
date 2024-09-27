import asyncio
import discord

from Functionnalities.Profiles.profileCreation import Profile


async def wait_for_reply(message, client):

    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        reply = await client.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
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


class Calendar(Profile):

    def __init__(self):
        super().__init__()

    async def calendar(self, message):
        query = {"discord_id":message.author.id }

        if not self.collection.find_one(query):
            await super().create (message)

        user_calendar = self.collection.find_one(query, projection={'_id': 0, "calendar": 1})
        embed = create_calendar_embed(user_calendar['calendar'], message)
        await message.channel.send(embed=embed)



    async def add_date_to_calendar(self, message, client):
        await self.calendar(message)

        await message.channel.send("Please send the date")
        reply_event_date = await wait_for_reply(message, client)
        if not reply_event_date: return
        await message.channel.send("What is this date for?")
        reply_event_name = await wait_for_reply(message, client)
        if not reply_event_name: return

        self.collection.update_one({"discord_id":message.author.id }, {"$addToSet": { "calendar": [ reply_event_date.content, reply_event_name.content ] } })
        await message.channel.send("Your date has been added to the calendar")


