from config import *
import discord, asyncio, random, time, datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command()
    async def ping(self, ctx):
        msg = await ctx.send("`Pinging bot latency...`")
        times = []
        counter = 0
   
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Pinging... {counter}/3")
            end = time.perf_counter()
            speed = end - start
            times.append(round(speed * 1000))

        embed = discord.Embed(title="More information:", description="Pinged 4 times and calculated the average.", colour=discord.Colour(value=defaultColour))
        embed.set_author(name="Pong!", icon_url=normalLogo)
        counter = 0
        for speed in times:
            counter += 1
            embed.add_field(name=f"Ping {counter}:", value=f"{speed}ms", inline=True)
        
        embed.add_field(name="Bot latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Average speed", value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
        embed.set_thumbnail(url=gifLogo)
        embed.set_footer(text=f"Estimated total time elapsed: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**", embed=embed)

    @commands.command()
    async def roast(self, ctx):
        await ctx.send(random.choice(open("databases/RoastList.txt").readlines()))

    @commands.command()
    async def help(self, ctx):
        try:
            await ctx.author.send("**http://spectrix.me/spectrum/**\n*Here's my help page!*")
            helpMsg = await ctx.send("**I sent you help in your DMs :mailbox_with_mail:**")
        except Exception:
            helpMsg = await ctx.send(f"**{ctx.author.mention} http://spectrix.me/spectrum/**\n*Here's my help page!*")
        await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.command()
    async def invite(self, ctx):
        try:
            await ctx.author.send("**https://bit.ly/SpectrumDiscord**\n*Here's my invite link!*")
            helpMsg = await ctx.send("**I sent my invite link in your DMs :mailbox_with_mail:**")
        except Exception:
            helpMsg = await ctx.send(f"**{ctx.author.mention} https://bit.ly/SpectrumDiscord**\n*Here's my invite link!*")
        await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.command(aliases=['support'])
    async def server(self, ctx):
        try:
            await ctx.author.send("**https://discord.gg/SuN49rm/**\n*Here's my official server!*")
            helpMsg = await ctx.send("**I sent you my server invite in your DMs :mailbox_with_mail:**")
        except Exception:
            helpMsg = await ctx.send(f"**{ctx.author.mention} https://discord.gg/ecXdjTD/**\n*Here's my official server!*")
        await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.command()
    async def poll(self, ctx, *, pollInfo):
        emb = (discord.Embed(description=pollInfo, colour=defaultColour))
        emb.set_author(name=f"Poll by {ctx.message.author}", icon_url="https://lh3.googleusercontent.com/7ITYJK1YP86NRQqnWEATFWdvcGZ6qmPauJqIEEN7Cw48DZk9ghmEz_bJR2ccRw8aWQA=w300")
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        try:
            pollMessage = await ctx.send(embed=emb)
            await pollMessage.add_reaction("\N{THUMBS UP SIGN}")
            await pollMessage.add_reaction("\N{THUMBS DOWN SIGN}")
        except Exception as e:
            await ctx.send(f"Oops, I couldn't react to the poll. Check that I have permission to add reactions! ```py\n{e}```")

def setup(bot):
    bot.add_cog(General(bot))
