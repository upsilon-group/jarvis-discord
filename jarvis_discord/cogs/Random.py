import datetime
import logging
import random
from typing import Union

import discord
from discord.ext import commands
from jarvis_discord import config, utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Random:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rnd"])
    async def random(self, ctx, *, msg_values: str) -> None:
        values = []
        for value in msg_values.split():
            try:
                value = float(value)
                value = int(value) if value.is_integer() else value
            except ValueError:
                pass
            finally:
                values.append(value)
        if any(isinstance(value, str) for value in values):
            response = random.choice(values)
        elif any(isinstance(value, float) for value in values):
            result = random.uniform(values[0], values[1])
            nb_decimals = max(
                [str(values[0])[::-1].find("."), str(values[1])[::-1].find(".")]
            )
            response = round(result, nb_decimals)
        else:
            response = random.randint(values[0], values[1])
        await ctx.channel.send(f':game_die: **`"{response}"`**')


def setup(bot):
    bot.add_cog(Random(bot))
