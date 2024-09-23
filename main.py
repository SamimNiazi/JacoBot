from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from Functionnalities import miscellaneous as misc

#LOAD MY TOKEN FROM MY ENV FILE
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

#BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#MESSAGE FUNCTIONALITY
# async def send_message(message: Message, user_message: str) -> None:
#     if not user_message:
#         print('Message was empty because intents were not enabled')
#         return
#
#     try:
#         response: str = get_response(user_message)
#         await message.channel.send(response)
#     except Exception as e:
#         print(e)


#DIRECTING COMMANDS
async def directCommands(action: str, message: Message) -> None:
    commandWords: list = action.split(' ')
    command_after_prefix: str = commandWords[0]
    match command_after_prefix:
        case "dice":
            await message.channel.send(misc.dice())
        case"8ball":
            await message.channel.send(misc.eightball())



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