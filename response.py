from random import choice,randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if 'hello' in lowered:
        return "B-B-B-BAKAAAA"
    elif 'how are you' in lowered:
        return "I'm fine"
    elif 'bye' in lowered:
        return "Bye"
    elif 'roll dice' in lowered:
        return f'Your rolled {randint(1,6)}'