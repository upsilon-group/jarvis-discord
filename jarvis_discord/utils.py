""" Jarvis Discord BOT

AUTHOR : Luoskate
VERSION : 1.0
"""

import asyncio
import datetime
import logging
import os
from typing import Dict, Optional

import discord
from discord.ext import commands
from jarvis_discord import config

LOGGER = logging.getLogger(f"jarvis.{__name__}")

CONFIG = config.Config("jarvis_discord/config.json")
PREFIX = CONFIG.prefix()
BASE_COGS = CONFIG.base_cogs()


async def rainbow(bot) -> None:
    await bot.wait_until_ready()
    guild = CONFIG.guild(bot)
    rainbow_role = discord.utils.get(guild.roles, name="rainbow")
    colors = [
        discord.Colour(int("FF0000", 16)),
        discord.Colour(int("FF003F", 16)),
        discord.Colour(int("FF007F", 16)),
        discord.Colour(int("FF00BF", 16)),
        discord.Colour(int("FF00FF", 16)),
        discord.Colour(int("BF00FF", 16)),
        discord.Colour(int("7F00FF", 16)),
        discord.Colour(int("3F00FF", 16)),
        discord.Colour(int("0000FF", 16)),
        discord.Colour(int("003FFF", 16)),
        discord.Colour(int("007FFF", 16)),
        discord.Colour(int("00BFFF", 16)),
        discord.Colour(int("00FFFF", 16)),
        discord.Colour(int("00FFBF", 16)),
        discord.Colour(int("00FF7F", 16)),
        discord.Colour(int("00FF3F", 16)),
        discord.Colour(int("00FF00", 16)),
        discord.Colour(int("3FFF00", 16)),
        discord.Colour(int("7FFF00", 16)),
        discord.Colour(int("BFFF00", 16)),
        discord.Colour(int("FFFF00", 16)),
        discord.Colour(int("FFBF00", 16)),
        discord.Colour(int("FF7F00", 16)),
        discord.Colour(int("FF3F00", 16)),
    ]
    while not bot.is_closed():
        for color in colors:
            await rainbow_role.edit(color=color)
            await asyncio.sleep(0.3)


async def self_delete(channel: discord.abc.Messageable, *args: str) -> None:
    for arg in args:
        await channel.send(content=arg, delete_after=4)


async def embed_msg(
    channel: discord.abc.Messageable,
    title: str,
    color: int,
    desc: Optional[str],
    timestamp: datetime.datetime,
    img_url: Optional[str],
    thumbnail_url: Optional[str],
    author_name: str,
    author_url: Optional[str],
    author_icon: str,
    footer: str,
    footer_icon: str,
    *args: Dict,
) -> None:

    embed = discord.Embed(
        title=title, colour=discord.Colour(color), description=desc, timestamp=timestamp
    )

    if img_url is not None:
        embed.set_image(url=img_url)
    if thumbnail_url is not None:
        embed.set_thumbnail(url=thumbnail_url)
    embed.set_author(name=author_name, url=author_url, icon_url=author_icon)
    embed.set_footer(text=footer, icon_url=footer_icon)

    for field in args:
        embed.add_field(
            name=field["name"], value=field["value"], inline=field["inline"]
        )

    await channel.send(embed=embed)


def get_prefix(self, message):
    prefix = commands.when_mentioned(self, message)
    for pre in PREFIX:
        prefix.append(pre)
    return prefix


def load_base_cogs(bot) -> None:
    for cog in os.listdir("jarvis_discord/cogs"):
        if cog.endswith(".py") and cog in BASE_COGS:
            try:
                bot.load_extension(f"jarvis_discord.cogs.{cog[:-3]}")
                LOGGER.info(f"Successfully load cog: <{cog[:-3]}>.")
            except Exception as error:
                LOGGER.error(
                    f"Could not load module <{cog}> due to {error.__class__.__name__}: {error}"
                )
