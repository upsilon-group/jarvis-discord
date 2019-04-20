"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""
import logging
from typing import Union

import discord
from discord.ext import commands
from tzlocal import get_localzone

import jarvis_discord as jarvis

TZ = get_localzone()

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Information(commands.Cog):
    """Rassemble les différentes commandes d'information."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["informations", "info", "infos"])
    async def information(
        self,
        ctx,
        *,
        converted: Union[
            discord.Member,
            jarvis.GuildConverter,
            discord.User,
            discord.TextChannel,
            discord.VoiceChannel,
            discord.CategoryChannel,
            discord.Role,
        ],
    ) -> None:
        """Donne des informations sur un élément.

        [description]

        Arguments:
            converted {Union[discord.Member,
                             converters.GuildConverter,
                             discord.User,
                             discord.TextChannel,
                             discord.VoiceChannel,
                             discord.CategoryChannel,
                             discord.Role,]} :
                - Élément sur lequel on souhaite obtenir des informations.
        """
        if isinstance(converted, (discord.TextChannel, discord.VoiceChannel)):
            member = converted.guild.get_member(ctx.author.id)
            if member is None:
                raise commands.BadUnionArgument
            invites = await converted.invites()
            perms = converted.permissions_for(member)
            if perms.read_messages and isinstance(converted, discord.TextChannel):
                embed = jarvis.TextInfoEmbed(ctx, converted, invites)
            elif perms.connect:
                embed = jarvis.VoiceInfoEmbed(ctx, converted, invites)
            else:
                raise commands.CheckFailure
        else:
            embed_class_name = getattr(
                jarvis, f"{converted.__class__.__name__}InfoEmbed"
            )
            embed = embed_class_name(ctx, converted)

        await ctx.author.send(embed=embed)

    @information.error
    async def information_error(self, ctx, error):
        # TODO: Add doc
        if isinstance(error, commands.BadUnionArgument):
            await ctx.author.send(
                f"Je suis désolé je n'ai pas trouvé : `{' '.join(ctx.message.content.split()[1:])}`."
            )
        print(error)


def setup(bot):
    # TODO: Add doc
    bot.add_cog(Information(bot))
