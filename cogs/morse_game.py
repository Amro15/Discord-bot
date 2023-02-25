import discord
import asyncio
from discord.ext import commands
from discord import app_commands, Embed
from bot import bot, GUILD_ID
from morse_code import encrypt
from morse_code_game.helpers import get_difficulty, DIFFICULTIES, SCORES_TO_WIN, DIFFICULTIES_DICT, wait
from autocomplete import difficulty_autocomplete, score_to_win_autocomplete


class Play_morse_game(commands.Cog):
    def __init__(self, bot, ongoing_game : bool = False, stop_morse_game_bool : bool = False,
                 generated_guess : bool = None, scoreboard : dict = "", str_scoreboard : str = "", user_with_correct_guess :str = ""):
      self.bot = bot
      self.ongoing_game = ongoing_game
      self.stop_morse_game_bool = stop_morse_game_bool
      self.generated_guess = generated_guess
      self.scoreboard = scoreboard
      self.str_scoreboard = str_scoreboard
      self.user_with_correct_guess = user_with_correct_guess

    @commands.Cog.listener()
    async def on_ready(self):
      print('Play morse game cog loaded')


    @app_commands.command(name="playmorseguessinggame", description="Plays a morse code guessing game")
    @app_commands.autocomplete(difficulty = difficulty_autocomplete, score_to_win = score_to_win_autocomplete)
    async def play_morse_game(self, interaction: discord.Interaction, difficulty : str, score_to_win : int):
        """Starts a morse code guessing game"""
        if self.ongoing_game == False:
          self.ongoing_game = True
          if self.stop_morse_game_bool == True:
            self.stop_morse_game_bool = False
          if difficulty not in DIFFICULTIES or score_to_win not in SCORES_TO_WIN:
              await interaction.response.send_message(embed = Embed(title=":warning:", description="Please select the difficulty and score to win from the available options and try again"))
          else:
              self.scoreboard = {}
              difficulty = get_difficulty(difficulty)
              await interaction.response.defer()
              current_high_score : int= 0
              while current_high_score != score_to_win and self.stop_morse_game_bool != True:
                  print("looping")
                  self.generated_guess = DIFFICULTIES_DICT[difficulty]["func"]()
                  await interaction.followup.send(embed= Embed(title="Encrypt the following:", description = self.generated_guess))
                  global time_to_guess
                  time_to_guess = asyncio.create_task(wait(DIFFICULTIES_DICT[difficulty]["time_to_guess"])) 
                  try:
                      await time_to_guess
                  except asyncio.CancelledError:
                      if self.stop_morse_game_bool == True:
                        break
                      else:
                        current_high_score = self.user_with_correct_guess["score"] if self.user_with_correct_guess["score"] > current_high_score else current_high_score
                        if current_high_score == score_to_win:
                            success_msg : str = f"{self.user_with_correct_guess['name']} wins!" 
                        else:
                            success_msg : str = f"{self.str_scoreboard}\n\nNext guess coming in ~5 seconds"
                        await interaction.followup.send(embed= Embed(title=f"{self.user_with_correct_guess['name']} scored a point!" ,description= success_msg))
                  else:
                      await interaction.followup.send(embed= Embed(title="Time is up!", description=f"The answer was {encrypt(self.generated_guess)[0]}\n Next guess coming in ~5 seconds"))
                  await asyncio.sleep(5)
              self.ongoing_game = False
        else:
          await interaction.response.send_message(embed=Embed(title="Cannot start game", description="Cannot start game when there is an ongoing game please use /stopmorsegame to stop current game to start a new one"))
    
    @app_commands.command(name="stopmorseguessinggame", description="Stops a morse code game if one is in progress")
    async def stop_morse_guessing_game(self, interaction : discord.Interaction):
      """Stops a morse code guessing game if any are in progress"""
      if self.stop_morse_game_bool == False:
        self.stop_morse_game_bool = True
        self.ongoing_game = False
        time_to_guess.cancel()
        await interaction.response.send_message(embed=Embed(title="Game successfully ended", description=self.str_scoreboard if self.str_scoreboard != "" else "No one scored"))
      else:
        await interaction.response.send_message(embed=Embed(title="There is no ongoing game", description="Please use /playmorseguessinggame to start a morse code guessing game"))


    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author == bot.user:
          return
      
      if self.generated_guess is not None and message.content == encrypt(self.generated_guess)[0]:
          time_to_guess.cancel()
          if message.author not in self.scoreboard:
              print("not in sc")
              self.scoreboard[message.author] = 1
          else:
              print("in sc")
              self.scoreboard[message.author] = self.scoreboard[message.author] + 1
          self.user_with_correct_guess = {"name": message.author, "score": self.scoreboard[message.author]} 
          for person, score in self.scoreboard.items():
              str_scoreboard = str_scoreboard + f"{person} has {str(score)} point(s)\n"
        
    @commands.command() 
    async def ping(self, ctx):
      await ctx.send("Pong!")

async def setup(bot : commands.Bot) -> None:
  await bot.add_cog(Play_morse_game(bot), guild=discord.Object(id=GUILD_ID))