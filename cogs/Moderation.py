import discord, asyncio, random, time, datetime
from discord.ext import commands
defaultColor = 0x36393e

class Moderation:
    """Very small cog, as I don't exactly plan for any actual moderation commands. Maybe in the future"""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def clear(self, ctx, number):
        try:
            msg = "message"
            if number <= 1:
                msg+='s'
            amt = await ctx.channel.purge(limit = (int(number) + 1))
            await asyncio.sleep(1)
            clearConfirmation = await ctx.send(f"**Cleared `{len(amt) - 1}` {msg} from this channel**", delete_after=4.0)
            await clearConfirmation.add_reaction("a:SpectrumOkSpin:466480898049835011")
        except discord.Forbidden:
            await ctx.send("```I seem to have missing permissions. I need the manage_message permission to preform this action.```")

def setup(bot):
    bot.add_cog(Moderation(bot))
