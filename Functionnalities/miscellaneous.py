"""Module containing small functionalities

This module contains all the functions that do not require complex logic
"""

from random import randint, choice
from Common import automated_responses

def dice() -> str:
    """
    Rolls a die and returns the result
    Returns:
        Int: Random number between 1 and 6
    """
    return f'You rolled a {randint(1, 6)}'

def eightball() -> str:
    """
    Function that returns a random response from eightball.
    Returns:
        Str: Eightball response
    """
    return choice(automated_responses.EIGHTBALLRESPONSES)
