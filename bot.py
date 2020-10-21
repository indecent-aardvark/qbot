import os
import sys
import discord
import logging
from discord.ext import commands
from cogs import music, error, meta, tips, roles
from pprint import pprint
from config import config

cfg = config.load_config()

bot = commands.Bot(command_prefix=cfg['prefix'])

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='?help'))
  logging.info(f"Logged in as {bot.user.name}")

COGS = [music.Music, error.CommandErrorHandler, meta.Meta, tips.Tips, roles.Roles]

def add_cogs(bot):
  for cog in COGS:
    bot.add_cog(cog(bot, cfg))  # Initialize the cog and add it to the bot

def run():
  add_cogs(bot)
  if cfg["token"] == "":
    raise ValueError(
      "No token has been provided. Please ensure that config.json contains the bot token."
    )
    sys.exit(1)
  bot.run(cfg["token"])