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
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        since_joined = user.joined_at.strftime("%d %b %Y %H:%M")

        created_on = f"{user_created}\n({since_created} days ago)"
        joined_at = f"{user.joined_at}\n({since_joined} days ago)"

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

        data = discord.Embed(description=activity, colour=defaultColor)
        data.add_field(name="Joined Discord on:", value=created_on)
        data.add_field(name="Joined Server at: ", value=joined_at)
        data.add_field(name="Roles:", value=roles, inline=False)
        data.set_footer(text=f"User ID: {author.id}")

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        await ctx.send(embed=data)

def setup(bot):
    bot.add_cog(GetInfo(bot))