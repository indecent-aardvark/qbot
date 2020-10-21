from discord.ext import commands
import discord
import random
from cogs import meta

class Tips(commands.Cog):
  """Commands for providing tips about using the bot."""

  def __init__(self, bot, config):
    self.bot = bot
    self.config = config[__name__.split(".")[-1]]
    self.tips = ["Only admins and the song requester can immediately skip songs. Everybody else will have to vote!",
                f"You can check out my source code here: {self.config['repository_url']}"]
    self._original_help_command = bot.help_command
    bot.help_command = meta.HelpCommand()
    bot.help_command.cog = self

  def cog_unload(self):
    self.bot.help_command = self._original_help_command

  @commands.command()
  async def tip(self, ctx):
    """Get a random tip about using the bot."""
    index = random.randrange(len(self.tips))
    await ctx.send(f"**Tip #{index+1}:** {self.tips[index]}")

  @commands.command()
  async def issues(self, ctx):
    """Instructions on how to report an issue."""
    await ctx.send("Please visit https://gitlab.com/indecent/pyqbot/issues to report an issue.")