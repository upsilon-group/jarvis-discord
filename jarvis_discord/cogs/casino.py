"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""
import logging
import random
from typing import List

from discord.ext import commands

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Casino(commands.Cog):
    # TODO: Add doc
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def transform_type(choices: List) -> List:
        # TODO: Add doc
        choices_trans = []
        for value in choices:
            try:
                value = float(value)
                value = int(value) if value.is_integer() else value
            except ValueError:
                pass
            choices_trans.append(value)
        return choices_trans

    @commands.command(aliases=["random"])
    async def casino(self, ctx, *, choices: str) -> None:
        # TODO: Add doc
        _choices = self.transform_type(choices.split())
        if any(isinstance(value, str) for value in _choices):
            response = random.choice(_choices)
        elif any(isinstance(value, float) for value in _choices):
            result = random.uniform(_choices[0], _choices[1])
            nb_decimals = max(
                [str(_choices[0])[::-1].find("."), str(_choices[1])[::-1].find(".")]
            )
            response = round(result, nb_decimals)
        else:
            response = random.randint(_choices[0], _choices[1])
        await ctx.channel.send(f':game_die: **`"{response}"`**')


def setup(bot):
    # TODO: Add doc
    bot.add_cog(Casino(bot))
