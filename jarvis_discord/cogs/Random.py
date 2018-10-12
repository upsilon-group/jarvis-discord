import logging
import random
from typing import Union

from discord.ext import commands
from jarvis_discord import utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Random:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["rnd"])
    async def random(self, ctx) -> None:
        if ctx.invoked_subcommand is None:
            pass

    @random.command(aliases=["str", "list"])
    async def string(self, ctx, *, values_list: str) -> None:
        values = values_list.split()
        result = random.choice(values)
        await ctx.channel.send(f':game_die: **`"{result}"`**')

    @random.command(aliases=["int", "number", "nbr"])
    async def integer(
        self, ctx, num_1: Union[int, float], num_2: Union[int, float]
    ) -> None:
        if isinstance(num_1 + num_2, int):
            response = random.randint(num_1, num_2)
        else:
            result = random.uniform(num_1, num_2)
            nb_decimal = max([str(num_1)[::-1].find("."), str(num_2)[::-1].find(".")])
            response = round(result, nb_decimal)
        await ctx.channel.send(f':game_die: **`"{response}"`**')

    @random.error
    async def random_error(self, ctx, error):
        LOGGER.error(error)
        if isinstance(error, commands.BadArgument):
            await utils.self_delete(ctx, f"{' '.join(ctx.args)} est introuvable.")


def setup(bot):
    bot.add_cog(Random(bot))
