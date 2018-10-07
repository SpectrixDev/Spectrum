import discord, asyncio, time
from time import ctime
from discord.ext import commands

class UserMod:
    def __init__(self, bot):
        self.bot = bot
   
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(aliases=['k'])
    async def kick(self, ctx, user : discord.Member, *, reason=None):
        if ctx.author.top_role > user.top_role or ctx.author == ctx.guild.owner:
            if user == ctx.author:
                return await ctx.send(f"**:no_entry: {user.mention} You can't kick yourself... just, leave the server?**")
            await user.kick(reason=reason) # code  s p a g e h t
            if not reason:
                msg = await ctx.send(f"**{user} was kicked :wave:**")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
                await user.send(f"**You were kicked from {ctx.guild.name}**")
            else:
                msg = await ctx.send(f"**{user} was kicked :wave: Reason:** {reason}")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
                await user.send(f"**You were kicked from {ctx.guild.name}. Reason:** {reason}**")

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(aliases=['b'])
    async def ban(self, ctx, user : discord.Member, *, reason=None):
        if ctx.author.top_role > user.top_role or ctx.author == ctx.guild.owner:
            if user == ctx.author:
                return await ctx.send(f"***:no_entry: {user.mentiom} You can't ban yourself... just, uninstall Discord?***")
            await user.ban(reason=reason)
            if not reason:
                msg = await ctx.send(f"**{user} was banned :hammer:**")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            else:
                msg = await ctx.send(f"**{user} was banned :hammer: Reason:** {reason}")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(aliases=['sb'])
    async def softban(self, ctx, user : discord.Member, *, reason=None):
        if ctx.author.top_role > user.top_role or ctx.author == ctx.guild.owner:
            if user == ctx.author:
                return await ctx.send("***:no_entry: You can't softban yourself...***")
            await user.ban(reason=reason)
            await user.unban(reason=reason)
            if not reason:
                msg = await ctx.send(f"**{user} was softbanned :wave:**")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            else:
                msg = await ctx.send(f"**{user} was softbanned :wave: Reason:** {reason}")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
        
def setup(bot):
    bot.add_cog(UserMod(bot))