from pymongo import MongoClient
from config import config
from bson import ObjectId

from pprint import pprint

cfg = config.load_config()

class Database:
  """Class for connecting to the database."""
  
  def __init__(self):
    self.config = cfg[__name__.split(".")[-1]]  # retrieve module name, find config entry
    self.uri = self.config['uri']

  def set_queue_limit(self, guild_id, limit=25):
    """Set queue limit for given guild."""
    try:
      client = MongoClient(self.uri)
      key = {'guild_id':guild_id}
      data = {'guild_id':guild_id,'playall_limit':limit}
      guild = client.qbot.guilds.update(key,data,upsert=True)
      return guild
    except Exception:
      return None
  
  def get_queue_limit(self, guild_id):
    """Get queue limit for given guild."""
    try:
      client = MongoClient(self.uri)
      guild = client.qbot.guilds.find({'guild_id':guild_id})
      guild = {'guild_id':guild[0]['guild_id'],'playall_limit':guild[0]['playall_limit']}

      if guild['guild_id'] == guild_id:
        return guild['playall_limit']
      return 0
    except Exception:
      return 0

  def set_default_role(self, guild_id, default=None):
    """Set default role for new users"""
    try:
      client = MongoClient(self.uri)
      key = {'guild_id':guild_id}
      data = {'guild_id':guild_id,'default_role':default}
      guild = client.qbot.guilds.update(key,data,upsert=True)
      return guild
    except Exception:
      return None

  def get_default_role(self, guild_id):
    """Get default role if one exists"""
    try:
      client = MongoClient(self.uri)
      guild = client.qbot.guilds.find({'guild_id':guild_id})
      guild = {'guild_id':guild[0]['guild_id'],'default_role':guild[0]['default_role']}

      if guild['guild_id'] == guild_id:
        return guild['default_role']
      return None
    except Exception:
      return None
