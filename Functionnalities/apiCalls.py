import requests
import discord
from discord import Embed


async def dog() -> Embed :
    r = requests.get("https://dog.ceo/api/breeds/image/random")
    response = r.json()
    em = discord.Embed(title = "Heres a dog!")
    em.set_image(url=response['message'])
    return em