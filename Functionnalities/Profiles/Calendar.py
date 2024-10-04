import asyncio
import discord
from datetime import datetime

from Functionnalities.Profiles.profileCreation import Profile
from Interfaces import ButtonView
from discord.ui import Button


async def wait_for_reply(message, author , client):

    def check(m):
        return m.author == author and m.channel == message.channel
    try:
        reply = await client.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await message.channel.send("You took too long to reply, please try again.")
        return
    return reply


def create_calendar_embed(dates, message) :
    em = discord.Embed(title = "Here's your upcoming events!")
    events = ""
    counter = 1
    for date in dates:
        delta_time_days = (date[0] - datetime.now()).days
        events += f'** {counter} -  {date[0].strftime("%a %b %d %Y")} :**  {date[1]} \n => *{abs(delta_time_days)} days {'left' if delta_time_days >= 0 else 'ago'}*\n'
        counter += 1

    em.description = events
    em.set_thumbnail(url=message.author.avatar)
    em.set_footer(text=message.author.id)
    return em

def create_button_view() :
    buttons = ButtonView.EventButtons()
    buttons.add_item(Button(label="Remove a Single Date", style=discord.ButtonStyle.primary,custom_id="remove_a_date"))
    buttons.add_item(Button(label="Remove All Dates", style=discord.ButtonStyle.secondary, custom_id="remove_all_dates"))
    return buttons

class Calendar(Profile):

    def __init__(self, client):
        super().__init__()
        self.client = client

    async def calendar(self, message):
        query = {"discord_id":message.author.id }

        await self.check_if_user_is_in_db(message, query)

        user_calendar = self.collection.find_one(query, projection={'_id': 0, "calendar": 1, "is_calendar_ordered" : 1})


        if not user_calendar["is_calendar_ordered"] and len(user_calendar["calendar"]) > 0:
            user_calendar = self.order_calendar_dates(message, query)

        embed = create_calendar_embed(user_calendar['calendar'], message)
        button_view = create_button_view()
        await message.channel.send(embed=embed, view=button_view)


    async def add_date_to_calendar(self, message):
        query = {"discord_id": message.author.id}
        await self.check_if_user_is_in_db(message, query)

        date_format = "%d/%m/%Y"
        await message.channel.send("Please send the date as \n(Enter date as \"DD/MM/YYYY\")\n")
        reply_event_date = await wait_for_reply(message, message.author, self.client)

        try:
            date_input = datetime.strptime(reply_event_date.content, date_format)
        except ValueError:
            await message.channel.send("You did not respect the format \"DD/MM/YYYY\"")
            return

        if not reply_event_date: return
        await message.channel.send("What is this date for?")
        reply_event_name = await wait_for_reply(message, message.author, self.client)
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

    async def remove_dates(self, interaction):
        if interaction.message.embeds[0].footer.text != str(interaction.user.id):
            return
        query = {"discord_id": interaction.user.id}
        match interaction.data.get("custom_id"):
            case "remove_a_date":

                user_profile = self.collection.find_one(query)
                await interaction.channel.send("Please send the index of the event you want to remove.")
                index = await wait_for_reply(interaction,interaction.user, self.client)
                try:
                    index_as_int = int(index.content)
                except ValueError:
                    await interaction.channel.send("You did not send me a proper index")
                    return
                try:
                    user_profile['calendar'].pop(index_as_int - 1)
                    self.collection.find_one_and_update(query, {'$set': {"calendar": user_profile['calendar']}})
                except IndexError:
                    await interaction.channel.send("This index is not in the calendar")
                    return
            case "remove_all_dates":
                self.collection.find_one_and_update(query, { '$set': { "calendar" : []} })

        await interaction.channel.send("Your calendar has been updated")




