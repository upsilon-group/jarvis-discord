""" Jarvis Discord BOT

AUTHOR : Luoskate
VERSION : 1.0
"""
import asyncio
import locale
import logging
import os

from typing import Dict
from typing import Optional

import discord

from discord.ext import commands

import requests

from jarvis_discord import config
from jarvis_discord import utils

locale.setlocale(locale.LC_TIME, "")

DISCORD_LOGGER = logging.getLogger("discord")
DISCORD_LOGGER.setLevel(logging.INFO)
DISCORD_HANDLER = logging.FileHandler(
    filename="logs/discord.log", encoding="utf-8", mode="w+"
)
DISCORD_HANDLER.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] <%(name)s> - [%(funcName)s] - %(message)s", "%x %X")
)
DISCORD_LOGGER.addHandler(DISCORD_HANDLER)

LOGGER = logging.getLogger("jarvis")
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.FileHandler(filename="logs/jarvis.log", encoding="utf-8", mode="w+")
HANDLER.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(levelname)s] <%(name)s> - [%(funcName)s] - %(message)s", "%x %X"
    )
)

LOGGER.addHandler(HANDLER)

CONFIG = config.Config("jarvis_discord/config.json")
TOKEN = CONFIG.token()

BOT = commands.Bot(
    command_prefix=utils.get_prefix,
    pm_help=True,
    command_not_found="La commande {} est introuvable.",
    command_has_no_subcommands="La commande {0.name} ne prend pas d'arguments.",
)


@BOT.event
async def on_ready() -> None:
    LOGGER.info(f"Logged in as : {str(BOT.user)}, ID: {BOT.user.id}")
    utils.load_base_cogs(BOT)


@BOT.event
async def on_member_join(member: discord.Member) -> None:
    default_role = CONFIG.default_role()
    LOGGER.info(f"New Member ! : {str(member)}")
    if default_role is not None:
        guild = CONFIG.guild(BOT)
        try:
            await member.add_roles(default_role, reason="New member default role.")
            LOGGER.info(f"Added {default_role.name} to {str(member)}")
        except discord.HTTPException:
            LOGGER.info(f"{default_role.name} doesn't exist in server : {guild.name}")


@BOT.event
async def on_message_delete(message: discord.Message) -> None:
    LOGGER.info(f"↪ message: {str(message.author)}: {message.content}")


@BOT.event
async def on_raw_message_delete(
    message_id: int, channel_id: int, guild_id: Optional[int] = None
) -> None:
    channel = BOT.get_channel(channel_id)
    if guild_id:
        guild = BOT.get_guild(guild_id)
        LOGGER.info(
            f"message ID: {message_id} in {str(channel.recipient) if isinstance(channel, discord.abc.PrivateChannel) else channel.name} -> {guild.name}."
        )
    else:
        LOGGER.info(
            f"message ID: {message_id} in {str(channel.recipient) if isinstance(channel, discord.abc.PrivateChannel) else channel.name}."
        )


@BOT.event
async def on_message_edit(
    message_before: discord.Message, message_after: discord.Message
) -> None:
    LOGGER.info(
        f"↪ message: {str(message_before.author)}: {message_before.content} ⟾ {str(message_after.author)}: {message_after.content}"
    )


@BOT.event
async def on_raw_message_edit(message_id: int, datas: Optional[Dict] = None) -> None:
    try:
        datas["content"]
    except (KeyError, TypeError):
        return
    channel = BOT.get_channel(datas["channel_id"])
    message = channel.get_message(message_id)
    LOGGER.info(
        f"{message_id} : in {str(channel.recipient) if isinstance(channel, discord.abc.PrivateChannel) else channel.name}"
    )
    await on_message(message)


@BOT.event
async def on_message(message: discord.Message) -> None:
    LOGGER.info(
        f"{message.id} : in {str(message.channel.recipient) if isinstance(message.channel, discord.abc.PrivateChannel) else message.channel.name}"
    )
    LOGGER.info(f"↪ message: {str(message.author)}: {message.content}")
    await BOT.process_commands(message)


LOOP = asyncio.get_event_loop()
LOOP.create_task(utils.rainbow(BOT))

try:
    try:
        LOOP.run_until_complete(BOT.start(TOKEN))
    except discord.LoginFailure:
        LOGGER.critical(f"Incorrect token: '{TOKEN}'.")
except KeyboardInterrupt:
    for task in asyncio.Task.all_tasks():
        task.cancel()
    LOOP.run_until_complete(BOT.logout())
    LOGGER.info("Exit : Keyboard Interrupt")
finally:
    BOT.close()
    LOOP.close()
