from discord.ui import View

class EventButtons(View):
    def __init__(self, author_id):
        super().__init__()
        self.author_id = author_id
