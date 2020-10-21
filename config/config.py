import json
import logging
import os

EXAMPLE_CONFIG = """{
  "token": "",
  "youtube_key": "",
  "database": "",
  "prefix": "?",
  "music": {
    "max_volume": 150,
    "vote_skip": true,
    "vote_skip_ratio": 0.5,
    "storage": ""
  },
  "tips": {
    "repository_url": "https://gitlab.com/indecent/pyqbot"
  }
}
"""


def load_config(path="config.json"):
  """Loads the config from `path`"""
  HERE = os.path.dirname(os.path.realpath(__file__))
  CONFIG_LOC = os.path.join(HERE,path)
  if os.path.exists(CONFIG_LOC) and os.path.isfile(CONFIG_LOC):
    with open(CONFIG_LOC, 'r') as config:
        return json.load(config)
  else:
    print(CONFIG_LOC)
    with open(CONFIG_LOC, 'w+') as config:
      config.write(EXAMPLE_CONFIG)
      logging.warn(
        f"No config file found. Creating a default config file at {path}"
      )
    return load_config(path=path)