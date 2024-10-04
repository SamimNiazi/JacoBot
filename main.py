"""Module that contains the base logic to run the discord bot

Attributes:
    intents (Intents): Wraps up a Discord gateway intent flag.
    client (Client): Represents a client connection that connects to Discord.
"""
from typing import Final
from discord import Intents, Client, Message
from Common.constants import Constants
from Common import command_directing

#BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#DIRECTING COMMANDS
async def direct_commands(action: str, message: Message) -> None:
    """Function used to call the appropriate functions that splits
    and obtains the command from user and then calls command_directing

    Args:
        action (str): command or interaction we need to direct
        message (Message): The Message discord object that we will use to get context information.
    """
    command_words: list = action.split(' ')
    command_after_prefix: str = command_words[0]
    await command_directing.commands_match_case(command_after_prefix, message, client)

#HANDLING STARTUP
PREFIX: Final[str] = "jaco "

@client.event
async def on_ready() -> None:
    """Function called when the bot boots up
    Prints a message when bot is connected/
    """
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: Message) -> None:
    """Function called whenever the bot detects a message
    If the message comes from the bot itself, ignores it
    If the message comes from elperro, ignores it
    If the message starts with the prefix: jaco,
    get the command and call direct_commands

    Args:
        message (Message): The Message discord object that we will use to get context information.
    """
    if message.author == client.user:
        return
    if message.author.id == 1287856434217750590:
        return
    if message.content.startswith(PREFIX):
        action = str(message.content[5:])
        await direct_commands(action.lower(), message)

@client.event
async def on_interaction(interaction) -> None:
    """Function called whenever the bot detects an interaction
    Defers the response, so the bot does not wait for one, and
    then calls command_directing

    Args:
        message (Message): The Message discord object that we will use to get context information.
    """
    await interaction.response.defer()
    await command_directing.buttons_match_case(interaction, client)


#MAIN ENTRY POINT
def main() -> None:
    """Function that starts up the bot"""
    client.run(token=Constants().discord_token)

if __name__ == '__main__':
    main()
