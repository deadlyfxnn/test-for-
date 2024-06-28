from os import name
import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class setActivity(commands.Cog): #setze deinen filenamen
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Wähle eine Option aus")
    async def set_activity(
      self, ctx,
      status: Option(str, "Wähle eine option", choices=["online", "idle", "dnd", "invisible"]),
      activity: Option(str, "Wähle eine weiter option", choices=["Game", "Watch", "Listening", "Streaming"]),
      name: Option(str),
      url: Option(str, "Ist bei Streaming pflicht", default=None)
    ):
      if status == "online":
        status = discord.Status.online
      elif status == "idle":
        status = discord.Status.idle
      elif status == "dnd":
        status = discord.Status.dnd
      elif status == "invisible":
        status = discord.Status.invisible

      if activity == "Game":
        act = discord.Game(name=name)
      elif activity == "Watch":
        act = discord.Activity(type=discord.ActivityType.watching, name=name)
      elif activity == "Listening":
        act = discord.Activity(type=discord.ActivityType.listening, name=name)
      elif activity == "Streaming":
        act = discord.Streaming(name=name, url=url)

      await self.bot.change_presence(status=status, activity=act)
      await ctx.respond("Status wurde geändert", ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(setActivity(bot)) #setze deinen filenamen