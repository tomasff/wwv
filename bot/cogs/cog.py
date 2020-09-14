import discord
from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot, members, guilds):
        self.bot = bot
        self._members = members
        self._guilds = guilds