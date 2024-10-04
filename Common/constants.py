"""Module used to obtain all important constants

Imports tokens from .env file

Example:
    Discord token
    MongoDB token
"""
import os
from typing import Final
from dotenv import load_dotenv
from pymongo import MongoClient

class Constants:
    """Constants class so that we can retrieve them from other modules in a singular spot."""

    # pylint: disable=too-few-public-methods
    def __init__(self):
        load_dotenv()
        self.discord_token: Final[str] = os.getenv("DISCORD_TOKEN")
        self.mongo_uri: Final[str] = os.getenv("MONGO_DB")
        self.mongo_client = MongoClient(self.mongo_uri)
