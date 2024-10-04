"""Module that contains the base logic to make a button

More or less of an interface, because the customization of the button is done elsewhere.
To avoid making an EventButtons class in every other file, I placed it here so it could
be called and constructed at will.
"""

from discord.ui import View

class EventButtons(View):
    """Inherits from Discord View to be able to create Buttons
    """
    def __init__(self):
        super().__init__()
