from Functionnalities.apiCalls import dog
from Functionnalities.miscellaneous import dice, eightball
from Functionnalities.Profiles.profileCreation import Profile
from Functionnalities.Profiles.Calendar import Calendar


async def commands_match_case(command_after_prefix, message, client=None):
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
    match interaction.data.get("custom_id"):
        case "remove_a_date" | "remove_all_dates":
            await Calendar(client).remove_dates(interaction)

