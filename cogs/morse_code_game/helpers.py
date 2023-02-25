import asyncio
from morse_code_game.word_generator import generate_letter, generate_sentence, generate_word

DIFFICULTIES_DICT : dict = {"easy" : {"func" : generate_letter, "time_to_guess" : 8 }, "normal": {"func": generate_word, "time_to_guess": 35}, "hard": {"func": generate_sentence, "time_to_guess": 120 }}
"""Stores the function used  to generate the guess and the time to guess the answer for every difficulty"""
DIFFICULTIES : list = [f"Easy (Letters only. Time to guess {DIFFICULTIES_DICT['easy']['time_to_guess']} secs)",
                       f"Normal (Words only. Time to guess {DIFFICULTIES_DICT['normal']['time_to_guess']} secs)",
                       f"Hard (Sentences only. Time to guess {DIFFICULTIES_DICT['hard']['time_to_guess']} secs)"]
"""Stores the options displayed when calling the command"""

SCORES_TO_WIN : list = [3, 5, 10]


async def wait(delay: int ) -> None:
    """Waits the passed amount in seconds"""
    await asyncio.sleep(delay)
def get_difficulty(s: str) -> str:
    """Takes the difficulty and generates a guess accordingly"""
    if "Easy" in s:
        return "easy"
    elif "Normal" in s:
        return "normal"
    elif "Hard" in s:
        return "hard"
    return None