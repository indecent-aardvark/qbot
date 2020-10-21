from discord.ext import commands
import discord
import asyncio
import youtube_dl
import logging
import math
from video import Video, Videos
from database import Database
from cogs import meta, guildstate

from pprint import pprint


class Access(commands.Cog):
  """Get access to the server"""

  def __init__(self, bot, config):
    self.bot = bot
    self.config = config[__name__.split(".")[-1]]  # retrieve module name, find config entry
    self.states = {}
    self._original_help_command = bot.help_command
    bot.help_command = meta.HelpCommand()
    bot.help_command.cog = self

  def cog_unload(self):
    self.bot.help_command = self._original_help_command

  def get_state(self, guild):
    """Gets the state for `guild`, creating it if it does not exist."""
    if guild.id in self.states:
      return self.states[guild.id]
    else:
      self.states[guild.id] = guildstate.GuildState()
      return self.states[guild.id]

  @commands.command(brief="Grants role of member.")
  @commands.guild_only()
  async def playlimit(self, ctx):
    """Grants role of member"""