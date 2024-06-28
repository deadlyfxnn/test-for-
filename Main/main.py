import discord
import os

from discord import activity

intents = discord.Intents.all()


bot = discord.Bot(
  intents = intents,
  debug_guilds = [1256173132834668634]
)

if __name__ == "__main__": 
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(os.environ['TOKEN'])
