import discord
from discord import app_commands
from morse_code_game.word_generator import generate_letter, generate_word, generate_sentence
from morse_code_game.helpers import DIFFICULTIES, SCORES_TO_WIN



async def difficulty_autocomplete(interaction: discord.Interaction, curr: str) -> list[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name = difficulty, value= difficulty)
        for difficulty in DIFFICULTIES if curr.lower() in difficulty.lower()
    ] 

async def score_to_win_autocomplete(interaction: discord.Interaction, curr: str) -> list[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name = score_to_win, value= score_to_win)
        for score_to_win in SCORES_TO_WIN if str(curr) in str(score_to_win)
    ] 