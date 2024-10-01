from typing import Final
from discord import Intents, Client, Message
from Common.constants import Constants
from Common import CommandDirecting

#BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#DIRECTING COMMANDS
async def direct_commands(action: str, message: Message) -> None:
    command_words: list = action.split(' ')
    command_after_prefix: str = command_words[0]
    await CommandDirecting.commands_match_case(command_after_prefix, message, client)

#HANDLING STARTUP
PREFIX: Final[str] = "jaco "
@client.event
async def on_ready() -> None:
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    if message.author.id == 1287856434217750590:   #can be removed if elperro is not in the same server >:c
        return
    if message.content.startswith(PREFIX):
        action = str(message.content[5:])
        await direct_commands(action.lower(), message)

@client.event
async def on_interaction(interaction) -> None:
    await interaction.response.send_message("Not yet implemented", ephemeral=True)

#MAIN ENTRY POINT
def main() -> None:
    client.run(token=Constants().TOKEN)

if __name__ == '__main__':
    main()