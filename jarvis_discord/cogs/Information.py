import datetime
import logging
from typing import Union

import discord
from discord.ext import commands
from jarvis_discord import config, utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Information:
    """Retrieve infos for a bunch of things."""

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config("jarvis_discord/config.json")
        self.server = self.config.guild(bot)

    @commands.group(aliases=["infos", "information", "informations"])
    async def info(self, ctx) -> None:
        if ctx.invoked_subcommand is None:
            pass

    @info.command(aliases=["usr"])
    async def user(self, ctx, *, user: discord.Member = None) -> None:
        if not user:
            user = self.server.get_member(ctx.author.id)
        await utils.embed_msg(
            ctx.author,
            "Informations :",
            user.color.value,
            f"Joue à __***{user.activity.name}***__" if user.activity else None,
            datetime.datetime.now(),
            None,
            user.avatar_url,
            user.name,
            f"https://discordapp.com/users/{user.id}/",
            user.avatar_url,
            f"Use {ctx.prefix} help to get info ",
            self.bot.user.avatar_url,
            {"name": "ID :", "value": user.id, "inline": True},
            {"name": "Statut :", "value": f"*{user.status}*", "inline": True},
            {"name": "Server :", "value": f"*{self.server}*", "inline": True},
            {
                "name": "Surnom :",
                "value": user.nick if not None else "*Aucun*",
                "inline": True,
            },
            {
                "name": "À créer son compte le :",
                "value": user.created_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": False,
            },
            {
                "name": "A rejoint le serveur le :",
                "value": user.joined_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": False,
            },
            {
                "name": f"Rôles ( __**{len(user.roles[1:])}**__ ):",
                "value": " | ".join(["`" + role.name + "`" for role in user.roles[1:]]),
                "inline": False,
            },
        )

    @user.error
    async def info_user_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print("bad arg")
            await utils.self_delete(ctx, f"{' '.join(str(ctx.args))} est introuvable.")

    @info.group(aliases=["chn", "channels"])
    async def channel(self, ctx) -> None:
        if ctx.invoked_subcommand is None:
            pass

    @channel.command(aliases=["txt"])
    async def text(self, ctx, *, channel: discord.TextChannel) -> None:
        invites = await channel.invites()
        invites_str = " | ".join([f"`{invite.code}`" for invite in invites])
        await utils.embed_msg(
            ctx.author,
            "Informations :",
            int("421D7A", 16),
            "Type : __*Texte*__",
            datetime.datetime.now(),
            None,
            None,
            channel.name,
            f"https://discordapp.com/channels/{channel.guild.id}/{channel.id}",
            self.bot.user.avatar_url,
            f"Use {ctx.prefix} help to get info ",
            self.bot.user.avatar_url,
            {"name": "ID :", "value": channel.id, "inline": True},
            {
                "name": f"Invitations ( __**{len(invites)}**__ ):",
                "value": invites_str if invites else "*Aucune*",
                "inline": True,
            },
            {"name": "Server :", "value": f"*{channel.guild}*", "inline": True},
            {
                "name": "Sujet :",
                "value": channel.topic if channel.topic else "*Aucun*",
                "inline": True,
            },
            {
                "name": "Créer le :",
                "value": channel.created_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": False,
            },
            {
                "name": "Catégorie :",
                "value": str(channel.category) if not None else "*Aucune*",
                "inline": True,
            },
            {
                "name": "NSFW :",
                "value": ":underage: __***Oui***__"
                if channel.is_nsfw()
                else ":white_check_mark: __***Non***__",
                "inline": True,
            },
        )

    @channel.command(aliases=["voc"])
    async def voice(self, ctx, *, channel: discord.VoiceChannel) -> None:
        invites = await channel.invites()
        invites_str = " | ".join([f"`{invite.code}`" for invite in invites])
        await utils.embed_msg(
            ctx.author,
            "Informations :",
            int("421D7A", 16),
            "Type : __*Vocale*__",
            datetime.datetime.now(),
            None,
            None,
            channel.name,
            f"https://discordapp.com/channels/{channel.guild.id}/{channel.id}",
            self.bot.user.avatar_url,
            f"Use {ctx.prefix} help to get info ",
            self.bot.user.avatar_url,
            {"name": "ID :", "value": channel.id, "inline": True},
            {
                "name": f"Invitations ( __**{len(invites)}**__ ):",
                "value": invites_str if invites else "*Aucune*",
                "inline": True,
            },
            {"name": "Server :", "value": f"*{channel.guild}*", "inline": True},
            {
                "name": "Limite d'utilisateur :",
                "value": f"**{len(channel.members)}** / __**{channel.user_limit if channel.user_limit != 0 else '∞'}**__",
                "inline": True,
            },
            {
                "name": "Créer le :",
                "value": channel.created_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": False,
            },
            {
                "name": "Catégorie :",
                "value": str(channel.category) if not None else "*Aucune*",
                "inline": True,
            },
            {"name": "Bitrate :", "value": f"*{channel.bitrate}/s*", "inline": True},
        )

    @text.error
    async def info_text_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print("bad arg")
            await utils.self_delete(ctx, f"{' '.join(str(ctx.args))} est introuvable.")
        elif isinstance(error, commands.CheckFailure):
            await utils.self_delete(ctx, f"Les channel privés ne fonctionnent pas.")


def setup(bot):
    bot.add_cog(Information(bot))
