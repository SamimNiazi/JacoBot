from random import randint, choice
from Constants import automatedResponses

def dice() -> str:
    return f'You rolled a {randint(1, 6)}'

def eightball() -> str:
    return choice(automatedResponses.EIGHTBALLRESPONSES)