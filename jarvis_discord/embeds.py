"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""
from datetime import datetime, timedelta
from typing import Dict, List

import discord
from discord.ext import commands
from tzlocal import get_localzone

from jarvis_discord import utils

TZ = get_localzone()


class MemberInfoEmbed(discord.Embed):
    """Représente un discord.Embed avec les informations sur un membre.

    TODO : add desc
    """

    def __init__(self, ctx: commands.Context, member: discord.Member):
        self.member = member
        self.prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        self.set_author(
            name=str(member),
            url=f"https://discordapp.com/users/{member.id}",
            icon_url=member.avatar_url,
        )
        self.set_thumbnail(url=member.avatar_url)
        self.set_footer(
            text=f"Utilise {self.prefix}help pour obtenir de l'aide",
            icon_url=ctx.bot.user.avatar_url,
        )
        self.set_fields()
        for field in self.fields_list:
            self.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )
        super().__init__(
            title="Informations :",
            colour=discord.Colour(member.color.value),
            timestamp=TZ.localize(datetime.now()),
        )

    def set_fields(self):
        """Créer les différents "champs" contant les informations."""
        activity = self.member.activity
        if activity:
            activity_prefix = utils.trans_activity(activity)
            hours = divmod(datetime.utcnow() - activity.start, timedelta(hours=1))
            minutes = divmod(hours[1], timedelta(minutes=1))
        self.fields_list = [
            {"name": "ID :", "value": self.member.id, "inline": True},
            {
                "name": f"Guilde :{' '*20}",
                "value": f"*{self.member.guild}*",
                "inline": True,
            },
            {
                "name": "Activité :",
                "value": f"{activity_prefix} {activity.name} depuis {int(hours[0])}h{int(minutes[0])}min."
                if activity
                else "*Aucune*",
                "inline": True,
            },
            {
                "name": "Surnom :",
                "value": self.member.nick if self.member.nick else "*Aucun*",
                "inline": True,
            },
            {
                "name": "Statut :",
                "value": f":desktop: *{utils.trans_status(self.member.desktop_status)}*\n \
                         :globe_with_meridians: *{utils.trans_status(self.member.web_status)}*\n \
                         :iphone: *{utils.trans_status(self.member.mobile_status)}*",
                "inline": True,
            },
            {
                "name": f"Rôles ( **{len(self.member.roles[1:])}** ):",
                "value": "\n".join(
                    [f"⦁`{role.name}`" for role in self.member.roles[1:]]
                ),
                "inline": True,
            },
            {
                "name": "A créé son compte le :",
                "value": self.member.created_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": True,
            },
            {
                "name": "A rejoint le serveur le :",
                "value": self.member.joined_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": True,
            },
        ]


class GuildInfoEmbed(discord.Embed):
    """Représente un discord.Embed avec les informations sur une guilde.

    TODO : add desc
    """

    def __init__(self, ctx: commands.Context, guild: discord.Guild):
        self.guild = guild
        self.prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        self.set_author(
            name=str(guild),
            url=f"https://discordapp.com/{guild.id}",
            icon_url=guild.icon_url,
        )
        self.set_thumbnail(url=guild.icon_url)
        self.set_footer(
            text=f"Utilise {self.prefix}help pour obtenir de l'aide",
            icon_url=ctx.bot.user.avatar_url,
        )
        self.set_fields()
        for field in self.fields_list:
            self.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )
        super().__init__(
            title="Informations :",
            colour=discord.Colour(int("421D7A", 16)),
            timestamp=TZ.localize(datetime.now()),
        )

    def set_fields(self):
        """Créer les différents "champs" contant les informations."""
        self.fields_list = [{"name": "ID :", "value": self.guild.id, "inline": True}]


class UserInfoEmbed(discord.Embed):
    """Représente un discord.Embed avec les informations sur un utilisateur.

    TODO : add desc
    """

    def __init__(self, ctx: commands.Context, user: discord.User):
        self.user = user
        self.prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        self.set_author(
            name=str(user),
            url=f"https://discordapp.com/users/{user.id}",
            icon_url=user.avatar_url,
        )
        self.set_thumbnail(url=user.avatar_url)
        self.set_footer(
            text=f"Utilise {self.prefix}help pour obtenir de l'aide",
            icon_url=ctx.bot.user.avatar_url,
        )
        self.set_fields()
        for field in self.fields_list:
            self.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )
        super().__init__(
            title="Informations :",
            colour=discord.Colour(user.color.value),
            timestamp=TZ.localize(datetime.now()),
        )

    def set_fields(self):
        """Créer les différents "champs" contant les informations."""
        self.fields_list = [
            {"name": "ID :", "value": self.user.id, "inline": True},
            {"name": "Statut :", "value": f"*{self.user.status}*", "inline": True},
            {
                "name": "A créé son compte le :",
                "value": self.user.created_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": False,
            },
        ]


class TextInfoEmbed(discord.Embed):
    """Représente un discord.Embed avec les informations sur un salon textuel.

    TODO : add desc
    """

    def __init__(
        self,
        ctx: commands.Context,
        text: discord.TextChannel,
        invites: List[discord.Invite],
    ):
        self.text = text
        self.prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        self.set_author(
            name=f"Salon textuel : {text.name}",
            url=(f"https://discordapp.com/channels/{text.guild.id}/{text.id}"),
            icon_url="https://image.ibb.co/cCGnyL/notepad.png",
        )
        self.set_thumbnail(url="https://image.ibb.co/cCGnyL/notepad.png")
        self.set_footer(
            text=f"Utilise {self.prefix}help pour obtenir de l'aide",
            icon_url=ctx.bot.user.avatar_url,
        )
        self.set_fields(invites)
        for field in self.fields_list:
            self.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )
        super().__init__(
            title="Informations :",
            colour=discord.Colour(int("421D7A", 16)),
            timestamp=TZ.localize(datetime.now()),
        )

    def set_fields(self, invites):
        """Créer les différents "champs" contant les informations."""
        invites_str = " | ".join([f"`{invite.code}`" for invite in invites])
        self.fields_list = [
            {"name": "ID :", "value": self.text.id, "inline": True},
            {
                "name": f"Invitations ( __**{len(invites)}**__ ):",
                "value": invites_str if invites else "*Aucune*",
                "inline": True,
            },
            {"name": "Guilde :", "value": f"*{self.text.guild}*", "inline": True},
            {
                "name": "Slowmode :",
                "value": f"{self.text.slowmode_delay} secondes",
                "inline": True,
            },
            {
                "name": "Sujet :",
                "value": self.text.topic if self.text.topic else "*Aucun*",
                "inline": True,
            },
            {
                "name": "Créé le :",
                "value": self.text.created_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": False,
            },
            {
                "name": "Catégorie :",
                "value": str(self.text.category) if not None else "*Aucune*",
                "inline": True,
            },
            {
                "name": "NSFW :",
                "value": ":underage: __***Oui***__"
                if self.text.is_nsfw()
                else ":white_check_mark: __***Non***__",
                "inline": True,
            },
        ]


class VoiceInfoEmbed(discord.Embed):
    """Représente un discord.Embed avec les informations sur un salon vocal.

    TODO : add desc
    """

    def __init__(
        self,
        ctx: commands.Context,
        vocal: discord.VoiceChannel,
        invites: List[discord.Invite],
    ):
        self.vocal = vocal
        self.prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        self.set_author(
            name=f"Salon vocal : {vocal.name}",
            url=(f"https://discordapp.com/channels/{vocal.guild.id}/{vocal.id}"),
            icon_url="https://image.ibb.co/gZqEdL/speaker.png",
        )
        self.set_thumbnail(url="https://image.ibb.co/gZqEdL/speaker.png")
        self.set_footer(
            text=f"Utilise {self.prefix}help pour obtenir de l'aide",
            icon_url=ctx.bot.user.avatar_url,
        )
        self.set_fields(invites)
        for field in self.fields_list:
            self.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )
        super().__init__(
            title="Informations :",
            colour=discord.Colour(int("421D7A", 16)),
            timestamp=TZ.localize(datetime.now()),
        )

    def set_fields(self, invites):
        """Créer les différents "champs" contant les informations."""
        invites_str = " | ".join([f"`{invite.code}`" for invite in invites])
        self.fields_list = [
            {"name": "ID :", "value": self.vocal.id, "inline": True},
            {
                "name": f"Invitations ( __**{len(invites)}**__ ):",
                "value": invites_str if invites else "*Aucune*",
                "inline": True,
            },
            {"name": "Guilde :", "value": f"*{self.vocal.guild}*", "inline": True},
            {
                "name": "Limite d'utilisateur :",
                "value": f"**{len(self.vocal.members)}** / __**{self.vocal.user_limit if self.vocal.user_limit != 0 else '∞'}**__",
                "inline": True,
            },
            {
                "name": "Créé le :",
                "value": self.vocal.created_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": False,
            },
            {
                "name": "Catégorie :",
                "value": str(self.vocal.category) if not None else "*Aucune*",
                "inline": True,
            },
            {"name": "Bitrate :", "value": f"*{self.vocal.bitrate}/s*", "inline": True},
        ]


class CategoryChannelInfoEmbed(discord.Embed):
    """Représente un discord.Embed avec les informations sur une catégorie.

    TODO : add desc
    """

    def __init__(self, ctx: commands.Context, category: discord.CategoryChannel):
        self.category = category
        self.ctx = ctx
        self.prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        self.set_author(
            name=f"Catégorie : {category.name}",
            url="",
            icon_url="https://image.ibb.co/gJHN00/category.png",
        )
        self.set_thumbnail(url="https://image.ibb.co/gJHN00/category.png")
        self.set_footer(
            text=f"Utilise {self.prefix}help pour obtenir de l'aide",
            icon_url=ctx.bot.user.avatar_url,
        )
        self.set_fields()
        for field in self.fields_list:
            self.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )
        super().__init__(
            title="Informations :",
            colour=discord.Colour(int("421D7A", 16)),
            timestamp=TZ.localize(datetime.now()),
        )

    def set_fields(self):
        """Créer les différents "champs" contant les informations."""
        member = self.category.guild.get_member(self.ctx.author.id)
        if member is None:
            raise commands.BadUnionArgument
        txt_channels_str = "\n".join(
            [
                f"⦁  **#**   `{channel.name}`"
                for channel in self.category.text_channels
                if channel.permissions_for(member).read_messages
            ]
        )
        voice_channels_str = "\n".join(
            [
                f"⦁:speaker:`{channel.name}`"
                for channel in self.category.voice_channels
                if channel.permissions_for(member).connect
            ]
        )
        channels_str = f"{txt_channels_str}\n{voice_channels_str}"
        self.fields_list = [
            {"name": "ID :", "value": self.category.id, "inline": True},
            {"name": "Guilde :", "value": f"*{self.category.guild}*", "inline": True},
            {
                "name": "Salons :",
                "value": channels_str if self.category.channels else "*Aucun*",
                "inline": True,
            },
        ]


class RoleInfoEmbed(discord.Embed):
    """Représente un discord.Embed avec les informations sur un rôle.

    TODO : add desc
    """

    def __init__(self, ctx: commands.Context, role: discord.Role):
        self.role = role
        self.prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        self.set_author(
            name=f"Rôle : {role.name}",
            url="",
            icon_url="https://image.ibb.co/hEGbcf/role-2-439291.png",
        )
        self.set_thumbnail(url="https://image.ibb.co/hEGbcf/role-2-439291.png")
        self.set_footer(
            text=f"Utilise {self.prefix}help pour obtenir de l'aide",
            icon_url=ctx.bot.user.avatar_url,
        )
        self.set_fields()
        for field in self.fields_list:
            self.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )
        super().__init__(
            title="Informations :",
            colour=role.color,
            timestamp=TZ.localize(datetime.now()),
        )

    def set_fields(self):
        """Créer les différents "champs" contant les informations."""
        self.fields_list = [
            {"name": "ID :", "value": self.role.id, "inline": True},
            {"name": "Guilde :", "value": f"*{self.role.guild}*", "inline": True},
            {
                "name": "Créé le :",
                "value": self.role.created_at.strftime("%A %d/%m/%Y à %H:%M:%S"),
                "inline": False,
            },
            {
                "name": "Visible :",
                "value": ":white_check_mark: __***Oui***__"
                if self.role.hoist
                else ":x: __***Non***__",
                "inline": True,
            },
            {
                "name": "Mentionnable :",
                "value": ":white_check_mark: __***Oui***__"
                if self.role.mentionable
                else ":x: __***Non***__",
                "inline": True,
            },
            {
                "name": "Couleur :",
                "value": f"`{str(self.role.colour)}`",
                "inline": True,
            },
        ]


class ExtentionEmbed(discord.Embed):
    """Représente un discord.Embed avec les informations sur le (dé)chargement des extentions.

    TODO : add desc
    """

    def __init__(self, ctx: commands.Context, result: Dict[str, List[str]], load: bool):
        self.result = result
        self.prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        title = f"__***{len(result['success'])}/{len(result['success']) + len(result['failed'])}***__ extentions {'dé' if not load else ''}chargés."
        self.set_author(
            name=ctx.author.name,
            url=f"https://discord.gg/nesNrkn",
            icon_url=ctx.author.avatar_url,
        )
        self.set_thumbnail(url=ctx.bot.user.avatar_url)
        self.set_footer(
            text=f"Utilise {self.prefix}help pour obtenir de l'aide",
            icon_url=ctx.bot.user.avatar_url,
        )
        self.set_fields()
        for field in self.fields_list:
            self.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )
        super().__init__(
            title=title,
            colour=discord.Colour(
                int("ff3f3f", 16) if result["failed"] else int("3fff52", 16)
            ),
            timestamp=TZ.localize(datetime.now()),
        )

    def set_fields(self):
        """Créer les différents "champs" contant les informations."""
        self.fields_list = [
            {"name": "Succès :", "value": self.result["success"], "inline": False},
            {"name": "Échecs :", "value": self.result["failed"], "inline": False},
        ]
