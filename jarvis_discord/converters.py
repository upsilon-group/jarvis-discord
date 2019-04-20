"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""

import discord
from discord.ext import commands
from discord.ext.commands.errors import BadArgument


class GuildConverter(commands.Converter):
    async def convert(self, ctx, argument):
        guild = discord.utils.get(ctx.bot.guilds, name=argument)
        if not guild:
            raise BadArgument(f"Guild {argument} not found.")
        return guild
