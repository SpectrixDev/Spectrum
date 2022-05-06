import discord, json, asyncio, logging
from discord.ext import commands

class RoleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def giverole(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.top_role > user.top_role or ctx.author == ctx.guild.owner:
            await user.add_roles(role)
            msg = await ctx.send(f"**Gave {user.mention} `{role}`**")
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def removerole(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.top_role >= user.top_role or ctx.author == ctx.guild.owner:
            await user.remove_roles(role)
            msg = await ctx.send(f"**Ok, `{role}` was removed from {user.mention}**")
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            
def setup(bot):
    bot.add_cog(RoleCommands(bot))