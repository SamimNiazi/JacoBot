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
            await Calendar().add_date_to_calendar(message, client)
        case "calendar":
            await Calendar().calendar(message)