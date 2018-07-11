import discord, asyncio, random, time, datetime
from discord.ext import commands
defaultColor = 0x36393e

class GetInfo:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member=None):
        author = ctx.message.author
        guild = ctx.message.guild

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - user.joined_at).days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        user_joined = user.joined_at.strftime("%d %b %Y %H:%M")

        created_on = f"{user_created}\n({since_created} days ago)"
        joined_at = f"{user_joined}\n({since_joined} days ago)"

        activity = f"Currently in {user.status} status"

        if user.activity is None:
            pass
        else:
            if str(user.activity).startswith("<discord.activity.Activity"):
                pass
            else:
                activity = f"Playing {user.activity}"

        if roles:
            roles = sorted(roles, key=[x.name for x in guild.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = "\n".join(roles)
        else:
            roles = "None"

        embed = discord.Embed(description=activity, colour=defaultColor)
        embed.add_field(name="Joined Discord on:", value=created_on, inline=False)
        embed.add_field(name="Joined Server at: ", value=joined_at, inline=False)
        embed.add_field(name="Roles:", value=roles, inline=False)
        embed.set_footer(text=f"User ID: {author.id}")

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            embed.set_author(name=name, url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
        else:
            embed.set_author(name=name)

        await ctx.send(embed=embed)


    @commands.command(no_pm=True)
    async def serverinfo(self, ctx):
        guild = ctx.message.guild
        online = len([m.status for m in guild.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(guild.members)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Since {}. Over {} days ago."
                      "".format(guild.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        embed = discord.Embed(description=created_at, colour=discord.Colour(value=defaultColor))
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Users", value="{}/{}".format(online, total_users))
        embed.add_field(name="Text Channels", value=text_channels)
        embed.add_field(name="Voice Channels", value=voice_channels)
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Owner", value=str(guild.owner))
        embed.set_footer(text=f"Guild ID:{str(guild.id)}")

        if guild.icon_url:
            embed.set_author(name=guild.name, url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)
        else:
            embed.set_author(name=guild.name)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GetInfo(bot))