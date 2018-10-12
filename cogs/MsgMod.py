import asyncio, discord
from discord.ext import commands

class MsgModeration:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["purge"])
    async def clear(self, ctx, number: int):
        msg = "message"
        if number != 1:
            msg+='s'
        amt = await ctx.channel.purge(limit = (int(number) + 1))
        await asyncio.sleep(1)
        clearConfirmation = await ctx.send(f"**Cleared `{len(amt) - 1}` {msg} from this channel**", delete_after=4.0)
        await clearConfirmation.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['slowmo'])
    async def slowmode(self, ctx, seconds: int=0):
        if seconds > 120:
            return await ctx.send(":no_entry: Amount can't be over 120 seconds")
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            a = await ctx.send("**Slowmode is off for this channel**")
            await a.add_reaction("a:SpectrumOkSpin:466480898049835011")
        else:
            if seconds == 1:
                numofsecs = "second"
            else:    
                numofsecs = "seconds"
            await ctx.channel.edit(slowmode_delay=seconds)
            confirm = await ctx.send(f"**Set the channel slow mode delay to `{seconds}` {numofsecs}\nTo turn this off, do $slowmode**")
            await confirm.add_reaction("a:SpectrumOkSpin:466480898049835011")

def setup(bot):
    bot.add_cog(MsgModeration(bot))