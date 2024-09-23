from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from Functionnalities import miscellaneous as misc
from Functionnalities import apiCalls

#LOAD MY TOKEN FROM MY ENV FILE
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

#BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#DIRECTING COMMANDS
async def directCommands(action: str, message: Message) -> None:
    commandWords: list = action.split(' ')
    command_after_prefix: str = commandWords[0]
    match command_after_prefix:
        case "dice":
            await message.channel.send(misc.dice())
        case "8ball":
            await message.channel.send(misc.eightball())
        case "dog":
            embed = await apiCalls.dog()
            await message.channel.send(embed = embed)



#HANDLING STARTUP
PREFIX: Final[str] = "jaco "

@client.event
async def on_ready() -> None:
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    if message.content.startswith(PREFIX):
        action = str(message.content[5:])
        await directCommands(action.lower(), message)

#MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()