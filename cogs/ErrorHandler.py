import traceback
import sys
from discord.ext import commands
import discord

class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'**:no_entry: `{ctx.command}` has been disabled.**')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'**:no_entry: `{ctx.command}` can not be used in Private Messages.**')
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                return await ctx.send('**:no_entry: I could not find that member. Please try again.**')

        elif isinstance(error, commands.NotOwner):
            return await ctx.send('**:no_entry: Only my owner can run this command.**')

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send('**:no_entry: You have insufficiant permissions to run this command.**', delete_after=4.0)
            
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
                
def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))