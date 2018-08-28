import datetime
import discord
import logging

from discord.ext import commands
from jarvis_discord import config
from jarvis_discord import utils
from typing import Union

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Say:
    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config("jarvis_discord/config.json")
        self.server = self.config.guild(bot)
    
    @commands.command()
    async def say(self, ctx, channel: discord.TextChannel, *, message: str) -> None:
        LOGGER.info(message)
        LOGGER.info(channel.name)
        await channel.send(content=message)

    @say.error
    async def say_error(self, ctx, error):
        LOGGER.error(error)
        if isinstance(error, commands.BadArgument):
            await utils.self_delete(ctx, f"{' '.join(ctx.args)} est introuvable.")

def setup(bot):
    bot.add_cog(Say(bot))
