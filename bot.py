import discord
from discord import app_commands, Embed
from discord.ext import commands
from discord.ext.commands import Context
from morse_code import decode, encrypt


intents = discord.Intents.all()
description = '''Morse code decoder and encrypter with a morse code guessing game'''
GUILD_ID = "1071476862917804053"

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.command()
async def sync(ctx: Context):
    """sync bot commands tree"""
    synced = await ctx.bot.tree.sync(guild = discord.Object(id=GUILD_ID))
    await bot.load_extension(f"cogs.morse_game")
    await ctx.send(f"Synced {len(synced)} commands")
    return

def add_commands(*funcs):
    """add multiple commands to tree"""
    for func in funcs:
        bot.tree.add_command(func)

@app_commands.command(name="decodemorse", description="Spaces must separate letters and words must be separated by /. Example:..-. --- --- / -... .- .-.")
async def decode_morse(interaction: discord.Interaction, sentence_in_morse: str):
    """Decodes a string of morse code"""
    decoded_sentence, fully_translated = decode(sentence_in_morse.split(" "))
    embedded_response : Embed = Embed(title="Your decoded message is:", description=decoded_sentence)
    failing_to_decode_msg : str = "\n\n:warning: Highlited morse code does not represent any letter or character please check your spelling"
    failed_embedded_response : Embed= Embed(title="Your decoded message is:", description=decoded_sentence + failing_to_decode_msg)
    if fully_translated:
        await interaction.response.send_message(embed=embedded_response)
    else:
        await interaction.response.send_message(embed=failed_embedded_response)


@app_commands.command(name="encryptmorse", description="Encrypts a word or sentence in morse. Words must be seperated by spaces. Example: Encrypt me")
async def encrypt_morse(interaction: discord.Interaction, sentence : str):
    """Encrypts a string into morse code"""
    encrypted_sentence , fully_translated = encrypt(sentence.split(" "))
    embedded_response : Embed = Embed(title="Your encrypted message is:", description=encrypted_sentence)
    failing_to_encrypt_msg : str = "\n\n:warning: Highlited characters do not have a morse code representation"
    fail_embedded_response : Embed = Embed(title="Your encrypted message is:", description=encrypted_sentence + failing_to_encrypt_msg)
    if fully_translated:
        await interaction.response.send_message(embed=embedded_response)
    else:
        await interaction.response.send_message(embed=fail_embedded_response)

add_commands(decode_morse, encrypt_morse)
