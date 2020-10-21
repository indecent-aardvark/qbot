import youtube_dl as ytdl
import discord
import re
from time import strftime, gmtime
from urllib.parse import urlparse

from pprint import pprint

YTDL_OPTS = {
  'default_search': 'ytsearch',
  'format': 'bestaudio/best',
  'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
  'restrictfilenames': True,
  'socket_timeout': 30,
  'nocheckcertificate': True,
  'ignoreerrors': False,
  'logtostderr': False,
  'quiet': True,
  'no_warnings': True,
  'source_address': '0.0.0.0',
  'usenetrc': True,
  'cachedir': f'',
  'postprocessors': [
    {
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192'
    },
    {
      'key': 'FFmpegMetadata'
    }
  ]
}

# Make additional options for handling playlists
YTDL_LIST_OPTS = {
  'dump_single_json': True,
  'extract_flat' : True,
  'noplaylist': False,
}

YTDL_LIST_OPTS.update(YTDL_OPTS)
YTDL_OPTS.update({'noplaylist':True})

class Video:
  """Class containing information about a particular video."""

  def __init__(self, url_or_search, requested_by, queue_length):
    """Plays audio from (or searches for) a URL."""
    video = self._get_info(url_or_search)
    video_format = video["formats"][0]
    self.stream_url = video_format["url"]
    self.video_url = video["webpage_url"]
    self.title = video["title"]
    self.uploader = video["uploader"] if "uploader" in video else ""
    self.thumbnail = video["thumbnail"] if "thumbnail" in video else None
    self.duration = strftime("%M:%S",gmtime(video["duration"] if "duration" in video else 0))
    if video["duration"] if "duration" in video else 0 > 3600:
      self.duration = strftime("%H:%M:%S",gmtime(video["duration"] if "duration" in video else 0))
    self.requested_by = requested_by
    self.position_in_queue = queue_length+1

  def _get_info(self, video_url):
    with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
      info = ydl.extract_info(video_url, download=False)
      video = None
      if "_type" in info and info["_type"] == "playlist":
        return self._get_info(
          info["entries"][0]["webpage_url"])  # get info for first video
      else:
        video = info
      return video

  def get_embed(self):
    """Makes an embed out of this Video's information."""
    embed = discord.Embed(
        title=self.title, description=f'{self.uploader}', url=self.video_url
      )
    embed.insert_field_at(1,name='__**Length**__',value=self.duration)
    embed.insert_field_at(2,name='__**Position in Queue**__',value=self.position_in_queue)
    embed.set_footer(
      text=f"Requested by {self.requested_by.name}",
      icon_url=self.requested_by.avatar_url)
    if self.thumbnail:
      embed.set_thumbnail(url=self.thumbnail)
    return embed

class Videos:
  """Class containing information about a particular video."""

  def __init__(self, url_or_search, requested_by):
    """Plays audio from (or searches for) a URL."""
    videos = self._get_info(url_or_search)
    parsed_uri = urlparse(url_or_search)
    base_uri = f'{parsed_uri.scheme}://{parsed_uri.netloc}{parsed_uri.path}?v='
    self.stream_urls = []
    try:
      for video in videos['entries']:
        self.stream_urls.append(f'{base_uri}{video["id"]}')
    except Exception:
      self.stream_urls = None

  def _get_info(self, video_url):
    with ytdl.YoutubeDL(YTDL_LIST_OPTS) as ydl:
      info = ydl.extract_info(video_url, download=False)
      if "_type" in info and info["_type"] == "playlist":
        return info