import os
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Final

class Constants:
    def __init__(self):
        # LOAD MY TOKEN FROM MY ENV FILE
        load_dotenv()
        self.TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
        # LOAD MONGODBURI FROM MY ENV FILE
        self.URI: Final[str] = os.getenv("MONGO_DB")
        self.mongo_client = MongoClient(self.URI)


