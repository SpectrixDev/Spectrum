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
        if ctx.author.top_role > user.top_role:
            if user == ctx.author:
                return await ctx.send("***:no_entry: You Can't Ban Yourself..***", delete_after=1.75)
            await user.kick(reason=reason)
            if not reason:
                msg = await ctx.send(f"**{user} has Been Banned From The Server**")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            msg = await ctx.send(f"**{user} has Been Kicked From The Server With A Reason:** {reason}")                
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
        elif ctx.guild.owner:
            await user.ban(reason=reason)
            if not reason:
                msg = await ctx.send(f"**{user} has Been Kicked From The Server**") 
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            msg = await ctx.send(f"**{user} has Been Banned From The Server With A Reason:** {reason}")                
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(aliases=['b'])
    async def ban(self, ctx, user : discord.Member, *, reason=None):
        if ctx.author.top_role > user.top_role:
            if user == ctx.author:
                return await ctx.send("***:no_entry: You Can't Ban Yourself..***", delete_after=1.75)
            await user.ban(reason=reason)
            if not reason:
                msg = await ctx.send(f"**{user} has Been Banned From The Server**")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            msg = await ctx.send(f"**{user} has Been Banned From The Server With A Reason:** {reason}")                
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
        elif ctx.guild.owner:
            await user.ban(reason=reason)
            if not reason:
                msg = await ctx.send(f"**{user} has Been Banned From The Server**") 
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            msg = await ctx.send(f"**{user} has Been Banned From The Server With A Reason:** {reason}")                
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(aliases=['sb'])
    async def softban(self, ctx, user : discord.Member, *, reason=None):
        if ctx.author.top_role > user.top_role:
            if user == ctx.author:
                return await ctx.send("***:no_entry: You Can't Softban Yourself..***", delete_after=1.75)
            await user.ban(reason=reason)
            await user.unban(reason=reason)
            if not reason:
                msg = await ctx.send(f"**{user} has Been Softbanned From The Server**")                
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            msg = await ctx.send(f"**{user} has Been Softbanned From The Server With A Reason:** {reason}")                
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
        elif ctx.guild.owner:
            await user.ban(reason=reason)
            await user.unban(reason=reason)
            if not reason:
                msg = await ctx.send(f"**{user} has Been Softbanned From The Server**") 
                await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
            msg = await ctx.send(f"**{user} has Been Softbanned From The Server With A Reason:** {reason}")                
            await msg.add_reaction("a:SpectrumOkSpin:466480898049835011")
        
def setup(bot):
    bot.add_cog(UserMod(bot))