import discord, asyncio, random, time, datetime, json, logging, psutil, humanize, platform
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)

class GetInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("```Invalid Arguments. Here's what you can do:\n$info user <@user>\n$info server\n$info bot```")

    @info.command(name='user', alias="userinfo")
    async def _user(self, ctx, *, user: discord.Member=None):
        author = ctx.message.author

        if not user:
            user = author 

        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - user.joined_at).days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        user_joined = user.joined_at.strftime("%d %b %Y %H:%M")

        created_on = f"{user_created}\n({since_created} days ago)"
        joined_at = f"{user_joined}\n({since_joined} days ago)"

        activity = f"Currently in {user.status} status"
        roles = list(reversed([x.name for x in user.roles if x.name != "@everyone"]))

        if user.activity is None:
            pass
        else:
            if str(user.activity).startswith("<discord.activity.Activity"):
                pass
            else:
                activity = f"Playing {user.activity}"

        if roles:
            roles = "\n".join(roles)
        else:
            roles = "None"

        embed = discord.Embed(description=activity, colour=0x36393e)
        embed.add_field(name="Joined Discord on:", value=created_on, inline=False)
        embed.add_field(name="Joined Server at: ", value=joined_at, inline=False)
        embed.add_field(name="Roles:", value=roles, inline=False)
        embed.set_footer(text=f"User ID: {user.id}")

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.bot:
            embed.set_author(name=f"{name} [Bot]", url=user.avatar_url)
        elif user.id == self.bot.owner_id:
            embed.set_author(name=f"{name} [My creator]", url=user.avatar_url)
        elif user.id == self.bot.user.id:
            embed.set_author(name=f"{name} [You can also do $botinfo]", url=user.avatar_url)
        else:
            embed.set_author(name=name, url=user.avatar_url)

        if user.avatar_url:
            embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)


    @info.command(name='server', aliases=["serverinfo"], no_pm=True)
    async def _server(self, ctx):
        guild = ctx.message.guild
        online = len([m.status for m in guild.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(guild.members)
        total_bots = len([member for member in guild.members if member.bot == True])
        total_humans = total_users - total_bots
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Since {}. Over {} days ago."
                      "".format(guild.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        embed = discord.Embed(description=created_at, colour=discord.Colour(value=0x36393e))
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Users", value="{}/{}".format(online, total_users))
        embed.add_field(name="Humans", value=total_humans)
        embed.add_field(name="Bots", value=total_bots)
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

    @info.command(name='bot', alias="botinfo")
    async def _bot(self, ctx):
        """Show's Spectrum's current information"""
        embed = discord.Embed(title=str("⚡ Spectrum Info"), color=discord.Color(value=0xc904e2))
        proc = psutil.Process()
        usage = sum(v for k, v in self.bot.command_usage.items())

        embed.description = "\n".join([
            self.bot.description,
            f'\n🚀 **{usage:,d}** commands has been executed since last boot\n',
            f'[Upvote](https://top.gg/bot/{self.bot.user.id}/vote)',
            f'[Support](https://discord.gg/ehR2Qw4GgN)',
            f'[GitHub](https://github.com/SpectrixOfficial/Spectrum)'
        ])

        counts = (
            f"I'm in {len(self.bot.guilds):,d} guilds",
            f'Seeing {len(set(self.bot.get_all_channels())):,d} channels',
            f'Listening to {len(set(self.bot.get_all_members())):,d} users'
        )
        os_info = (
            f'OS: `{platform.platform()}`',
            f'CPU Usage: {psutil.cpu_percent()}%',
            f'CPU Cores: {psutil.cpu_count()}',
        )
        stats = (
            f'Been running since {humanize.naturaltime(self.bot.uptime)}',
            f'Using {humanize.naturalsize(proc.memory_full_info().rss)} physical memory',
            f'Using discord.py {discord.__version__} and Python {platform.python_version()}',
        )
        embed.add_field(name="Runtime", value="\n".join(stats), inline=False)
        embed.add_field(name="Host", value="\n".join(os_info))
        embed.add_field(name="Counts", value="\n".join(counts))
        embed.set_footer(text="Made by Spectrix#7745 with love ❤", icon_url=config['styling']['logo'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GetInfo(bot))
