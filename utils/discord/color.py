import random

COLORS = {
    "pink": {
        "start": "```ansi\n[2;35m",
        "end": "[0m\n```"
    },
    "red": {
        "start": "```ansi\n[2;35m[2;31m",
        "end": "[0m[2;35m[0m\n```"
    },
    "yellowish": {
        "start": "```ansi\n[2;35m[2;31m[2;32m",
        "end": "[0m[2;31m[0m[2;35m[0m\n```"
    },
    "blue": {
        "start": "```ansi\n[2;34m",
        "end": "[0m\n```"
    },
    "teal": {
        "start": "```ansi\n[2;34m[2;32m[2;32m[2;32m[2;36m",
        "end": "[0m[2;32m[0m[2;32m[0m[2;32m[0m[2;34m[0m\n```"
    },
    "white": {
        "start": "```ansi\n[2;37m",
        "end": "[0m[2;37m[0m\n```"
    }
}

def colorize_message(message: str) -> str:
    """ Wrap the message in color """

    color = random.choice(list(COLORS.values()))
    return f'{color["start"]}{message}{color["end"]}'


if __name__ == "__main__":
    pass
