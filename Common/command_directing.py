"""Command directing Module

This module is used to call the appropriate functions for specific commands.
The same is done for interactions from buttons
"""
from Functionnalities.api_calls import dog
from Functionnalities.miscellaneous import dice, eightball
from Functionnalities.Profiles.profile_creation import Profile
from Functionnalities.Profiles.calendar import Calendar


async def commands_match_case(command_after_prefix, message, client=None):
    """Method for the commands directing.

    Args:
        command_after_prefix (str): The command we will be using to call the right function.
        message (Message): The Message discord object that we will use to get context information.
        client (Client): The Client discord object that represents a client connection to Discord.
                         Some functions require it.
    """
    match command_after_prefix:
        case "dice":
            await message.channel.send(dice())
        case "8ball":
            await message.channel.send(eightball())
        case "dog":
            embed = await dog()
            await message.channel.send(embed=embed)
        case "createprofile":
            await Profile().create(message)
        case "adddate":
            await Calendar(client).add_date_to_calendar(message)
        case "calendar":
            await Calendar(client).calendar(message)

async def buttons_match_case(interaction, client=None):
    """Method for the interaction directing.

    Args:
        interaction (Interaction): The Interaction discord object that we will use to get
        context information.
        client (Client): The Client discord object that represents a client connection to Discord.
                         Some functions require it.
    """
    match interaction.data.get("custom_id"):
        case "remove_a_date" | "remove_all_dates":
            await Calendar(client).remove_dates(interaction)
