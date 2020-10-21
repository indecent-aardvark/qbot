from discord.ext import commands
import discord
import asyncio
import logging
import pymongo
from pymongo import MongoClient
from database import Database
from cogs import meta, guildstate

from pprint import pprint

class Roles(commands.Cog):
  '''Commands to help with role namagement'''

  def __init__(self, bot, config):
    self.bot = bot
    self.config = config

  @commands.Cog.listener()
  async def on_member_join(self, ctx):
    try:
      db_client = Database()
      default_role = db_client.get_default_role(ctx.guild.id)
      if default_role is not None:
        await ctx.add_roles(discord.utils.get(ctx.guild.roles,name=default_role))
    except:
      pass

  @commands.command(brief="Role management.")
  @commands.guild_only()
  async def role(self, ctx, *, opts):
    try:
      opts = opts.split(' ')
      opts = list(filter(lambda a: a != '', opts))
      if opts[0] == 'default':
        try:
          db_client = Database()
          try:
            default_role = opts[1:]
            default_role = ' '.join(default_role)
            guild_roles = [role.name for role in ctx.guild.roles]
            if default_role in guild_roles:
              db_client.set_default_role(ctx.guild.id,opts[1])
              message = await ctx.send(f"The default role has been set to {opts[1]}!")
            else:
              pprint(default_role)
              pprint(guild_roles)
              message = await ctx.send(f"The role '{default_role}' doesn't exist!")
          except IndexError:
            default_role = db_client.get_default_role(ctx.guild.id)
            if default_role is not None:
              message = await ctx.send(f"The default role is {default_role}.")
            else:
              message = await ctx.send(f"There is no default role set.")
        except pymongo.errors.OperationFailure as e:
          await ctx.send("Sorry, but I had trouble saving that :(")
      elif opts[0] == 'add':
        try:
          user = opts[1]
          new_role = ' '.join(opts[2:])
          member_exists = False
          for member in ctx.guild.members:
            if member.name.lower() == user.lower() or str(member.id) == user.replace('<@','').replace('>',''):
              try:
                member_exists = True
                for role in ctx.guild.roles:
                  if role.name.lower() == new_role.lower():
                    new_role = role.name
                await member.add_roles(discord.utils.get(member.guild.roles,name=new_role))
              except:
                message = await ctx.send(f"The role {new_role} doesn't exist!")
          if not member_exists:
            message = await ctx.send(f"The user {user} doesn't exist!")
        except:
          message = await ctx.send(f"It looks like something didn't go as planned... You'll have to try again.")
      elif opts[0] == 'remove':
        pass
    except IndexError as e:
      await ctx.send("You didn't give me any arguments...")
      
    """
    guild_roles = ctx.guild.roles
    '''
    : role.name
    : role.permissions.manage_roles
    '''
    for role in guild_roles:
      pprint(role.name)
      pprint(role.permissions.manage_roles)
    print('---')
    sender_roles = ctx.author.roles
    '''
    : role.name
    : role.permissions.manage_roles
    '''
    for role in sender_roles:
      pprint(role.name)
      pprint(role.permissions.manage_roles)
    members = ctx.guild.members
    for member in members:
      #pprint(dir(member))
      pprint(member.name)
    #pprint(dir(ctx))
    """
    pprint(opts)