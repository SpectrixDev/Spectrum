import discord
from discord.ext import commands
from random import randint
from random import choice
from urllib.parse import quote_plus
import datetime
import time
import aiohttp
import asyncio

class getInfo:
    """Commands designed to get information of servers/people"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def userinfo(self, ctx, *, user: discord.Member=None):
        """Shows users's information"""
        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        since_created = (ctx.message.timestamp - user.created_at).days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")

        created_on = "{}\n({} days ago)".format(user_created, since_created)

        game = "Currently in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.type == "0" or user.game.url is None:
            game = "Playing {}".format(user.game)
        elif user.game.type == "1":
            game = "Streaming: [{}]({})".format(user.game, user.game.url)
        elif user.game.type == "2":
            game = "Listening to {}".format(user.game)
        elif user.game.type == "3":
            game = "Watching {}".format(user.game)
        else:
            game = "Playing {}".format(user.game)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text="User ID: " + author.id)

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Shows the server's information"""
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.voice])
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. Over {} days ago."
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=0x3be801))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def botinfo(self, ctx):
        """Show's Spectrum's current information"""
        servers = str(len(self.bot.servers))
        users = str(len(set(self.bot.get_all_members())))
        channels = str(len(set(self.bot.get_all_channels())))
        em = discord.Embed(description="Some current stats for Spectrum", colour=discord.Colour(value=0x3be801))
        em.add_field(name="Server count:", value=servers, inline=False)
        em.add_field(name="Users bot can see:", value=users, inline=False)
        em.add_field(name="Channels bot can see:", value=channels, inline=False)
        em.set_author(name="Bot Information", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
        em.set_thumbnail(url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(getInfo(bot))
