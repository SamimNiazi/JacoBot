import asyncio
import discord
from datetime import datetime

from Functionnalities.Profiles.profileCreation import Profile
from Interfaces import ButtonView
from discord.ui import Button


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
        delta_time_days = (date[0] - datetime.now()).days
        events += f'-** {date[0].strftime("%a %b %d %Y")} :**  {date[1]} \n => *({abs(delta_time_days)} days {'left' if delta_time_days >= 0 else 'ago'})*\n'
    em.description = events
    em.set_thumbnail(url=message.author.avatar)
    return em

def create_button_view() :
    buttons = ButtonView.EventButtons()
    buttons.add_item(Button(label="Remove a Single Date", style=discord.ButtonStyle.primary))
    buttons.add_item(Button(label="Remove All Dates", style=discord.ButtonStyle.secondary))
    buttons.add_item(Button(label="Remove Expired Dates", style=discord.ButtonStyle.secondary))
    return buttons

class Calendar(Profile):

    def __init__(self):
        super().__init__()

    async def calendar(self, message):
        query = {"discord_id":message.author.id }

        await self.check_if_user_is_in_db(message, query)

        user_calendar = self.collection.find_one(query, projection={'_id': 0, "calendar": 1, "is_calendar_ordered" : 1})


        if not user_calendar["is_calendar_ordered"] and len(user_calendar["calendar"]) > 0:
            user_calendar = self.order_calendar_dates(message, query)

        embed = create_calendar_embed(user_calendar['calendar'], message)
        button_view = create_button_view()
        await message.channel.send(embed=embed, view=button_view)



    async def add_date_to_calendar(self, message, client):
        query = {"discord_id": message.author.id}
        await self.check_if_user_is_in_db(message, query)

        date_format = "%d/%m/%Y"
        await message.channel.send("Please send the date as \n(Enter date as \"DD/MM/YYYY\")\n")
        reply_event_date = await wait_for_reply(message, client)

        try:
            date_input = datetime.strptime(reply_event_date.content, date_format)
        except ValueError:
            await message.channel.send("You did not respect the format \"DD/MM/YYYY\"")
            return

        if not reply_event_date: return
        await message.channel.send("What is this date for?")
        reply_event_name = await wait_for_reply(message, client)
        if not reply_event_name: return

        self.collection.update_one(query, {"$set":{"is_calendar_ordered" : False}, "$addToSet": { "calendar": [ date_input, reply_event_name.content ] } })
        await message.channel.send("Your date has been added to the calendar")

    def order_calendar_dates(self, message, query):
        collection_to_order = self.collection.find_one(query)
        sorted_calendar = sorted(collection_to_order['calendar'], key=lambda x: x[0])
        self.collection.update_one(query,{'$set': {'calendar': sorted_calendar, 'is_calendar_ordered': True}})
        return self.collection.find_one(query)

    async def check_if_user_is_in_db (self, message, query) :
        if not self.collection.find_one(query):
            await super().create(message)
