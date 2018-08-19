import discord, asyncio, random, time, datetime
from discord.ext import commands
defaultColour = 0x36393e

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roast(self, ctx):
        await ctx.send(random.choice(open("databases/RoastList.txt").readlines()))

    @commands.command()
    async def help(self, ctx):
        try:
            await ctx.author.send("**https://spectrixofficial.github.io/Spectrix-Website/spectrum/**\n*Here's my help page!*")
            helpMsg = await ctx.send("**I sent you help in your DMs :mailbox_with_mail:**")
        except Exception:
            helpMsg = await ctx.send(f"**{ctx.author.mention} https://spectrixofficial.github.io/Spectrix-Website/spectrum/**\n*Here's my help page!*")
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
