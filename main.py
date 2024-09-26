from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from pymongo import MongoClient

from Functionnalities import miscellaneous, apiCalls
from Functionnalities.Profiles import profileCreation, Calendar

#LOAD MY TOKEN FROM MY ENV FILE
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
#LOAD MONGODBURI FROM MY ENV FILE
URI: Final[str] = os.getenv("MONGO_DB")
mongoClient = MongoClient(URI)

#BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#DIRECTING COMMANDS
async def direct_commands(action: str, message: Message) -> None:
    command_words: list = action.split(' ')
    command_after_prefix: str = command_words[0]

    match command_after_prefix:
        case "dice":
            await message.channel.send(miscellaneous.dice())
        case "8ball":
            await message.channel.send(miscellaneous.eightball())
        case "dog":
            embed = await apiCalls.dog()
            await message.channel.send(embed = embed)
        case "createprofile":
            await profileCreation.create(message,mongoClient)
        case "adddate":
            await Calendar.add_date_to_calendar(message, client, mongoClient)
        case "calendar":
            await Calendar.calendar(message, mongoClient)




#HANDLING STARTUP
PREFIX: Final[str] = "jaco "

@client.event
async def on_ready() -> None:
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    if message.author.id == 1287856434217750590:
        return
    if message.content.startswith(PREFIX):
        action = str(message.content[5:])
        await direct_commands(action.lower(), message)

#MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()