import discord, json, asyncio
from discord.ext import commands

class RoleCommands:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print("RoleCommands is Loaded")

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def giverole(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.top_role > user.top_role:
            await user.add_roles(role)
            msg = await ctx.send(f"**Gave {user.mention} Role: `{role}`**")
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
        elif ctx.guild.owner:
            await user.add_roles(role)
            msg = await ctx.send(f"**Gave {user.mention} Role: `{role}`**")
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def removerole(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.top_role >= user.top_role:
            await user.remove_roles(role)
            msg = await ctx.send(f"**Removed {user.mention} From role: `{role}`**")
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
        elif ctx.guild.owner:
            await user.remove_roles(role)
            msg = await ctx.send(f"**Removed {user.mention} From role: `{role}`**")
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
        
def setup(bot):
    bot.add_cog(RoleCommands(bot))