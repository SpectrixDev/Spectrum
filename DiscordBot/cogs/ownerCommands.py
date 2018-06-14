from discord.ext import commands
import time
import datetime
import math
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io

#---------------------------------
ownerid = "276707898091110400"
class owner:
    bot=commands.Bot(description='Spectrum',command_prefix="$")
    def is_owner(ctx):
        if ctx.message.author.id == "276707898091110400":
            return True
        return False


    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

#Say command-----------------------------------------
    @commands.check(is_owner)
    @commands.command(hidden=True)
    async def say(self, *, something):
        await self.bot.say(something)

#Repl & exec---------------------------------
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        if ctx.message.author.id != ownerid:
            return
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.server,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            em = discord.Embed(description=self.get_syntax_error(e), colour=0x3be801)
            em.set_author(name="OUTPUT")
            await self.bot.say(embed=em)

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            em = discord.Embed(description='```py\n{}{}\n```'.format(value, traceback.format_exc()), colour=0x3be801)
            em.set_author(name="OUTPUT")
            await self.bot.say(embed=em)
        else:
            value = stdout.getvalue()
            try:
                await self.bot.add_reaction(ctx.message, '\N{OK HAND SIGN}')
            except:
                pass

            if ret is None:
                if value:
                    em = discord.Embed(description='```py\n%s\n```' % value, colour=0x3be801)
                    em.set_author(name="OUTPUT")
                    await self.bot.say(embed=em)
            else:
                self._last_result = ret
                discord.Embed(description='```py\n%s%s\n```' % (value, ret), colour=0x3be801)
                em.set_author(name="OUTPUT")
                await self.bot.say(embed=em)

    @commands.command(pass_context=True, hidden=True)
    async def repl(self, ctx):
        if ctx.message.author.id != ownerid:
            return
        msg = ctx.message

        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'server': msg.server,
            'channel': msg.channel,
            'author': msg.author,
            '_': None,
        }

        if msg.channel.id in self.sessions:
            await self.bot.say('Already running a REPL session in this channel. Exit it with `quit`.')
            return

        self.sessions.add(msg.channel.id)
        await self.bot.say('Enter code to execute or evaluate. `exit()` or `quit` to exit.')
        while True:
            response = await self.bot.wait_for_message(author=msg.author, channel=msg.channel,
                                                       check=lambda m: m.content.startswith('`'))

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await self.bot.say('Exiting.')
                self.sessions.remove(msg.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await self.bot.say(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = '```py\n{}{}\n```'.format(value, traceback.format_exc())
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = '```py\n{}{}\n```'.format(value, result)
                    variables['_'] = result
                elif value:
                    fmt = '```py\n{}\n```'.format(value)

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await self.bot.send_message(msg.channel, 'Content too big to be printed.')
                    else:
                        await self.bot.send_message(msg.channel, fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await self.bot.send_message(msg.channel, 'Unexpected error: `{}`'.format(e))

def setup(bot):
    bot.add_cog(owner(bot))
