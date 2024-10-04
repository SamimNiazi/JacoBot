# -*- coding: utf-8 -*-
"""Module containing all the api calls

This module contains all the functions that require to access an external API endpoint
"""
import requests
import discord
from discord import Embed


async def dog() -> Embed :
    """Call to an API to return a picture of a dog
    Returns:
        Embed: Discord embed that will be used in the message sent to the user
    """
    r = requests.get("https://dog.ceo/api/breeds/image/random", timeout=5)
    response = r.json()
    em = discord.Embed(title = "Heres a dog!")
    em.set_image(url=response['message'])
    return em
