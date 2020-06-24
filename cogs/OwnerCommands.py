import traceback
import inspect
import textwrap
from contextlib import redirect_stdout
import io
from collections import Counter
from os import listdir
from os.path import isfile, join
import asyncio, discord
from discord.ext import commands


lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
no_py = [s.replace('.py', '') for s in lst]
startup_extensions = ["cogs." + no_py for no_py in no_py]

class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates code"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('a:SpectrumOkSpin:466480898049835011')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(hidden=True)
    async def reload(self, ctx, *, ext):
        try:
            if ext == 'all':
                for extension in startup_extensions:
                    self.bot.unload_extension(extension)
                    self.bot.load_extension(extension)
            else:
                self.bot.unload_extension(f"cogs.{ext}")
                self.bot.load_extension(f"cogs.{ext}")
            await ctx.message.add_reaction('a:SpectrumOkSpin:466480898049835011')
        except Exception:
            try:
                self.bot.unload_extension(f"{ext}")
                self.bot.load_extension(f"ext")
                await ctx.message.add_reaction('a:SpectrumOkSpin:466480898049835011')
            except Exception as e:
                await ctx.send(f"Couldn't reload extension `{ext}`. Error: ```{e}```")

    @commands.command(hidden=True)
    async def load(self, ctx, *, extention):
        try:
            self.bot.load_extension(f"cogs.{extention}")
            await ctx.message.add_reaction('a:SpectrumOkSpin:466480898049835011')
        except Exception:
            try:
                self.bot.load_extension(extention)
                await ctx.message.add_reaction('a:SpectrumOkSpin:466480898049835011')
            except Exception as e:
                await ctx.send(f"Couldn't load extention `{extention}`. Error: ```{e}```")

    @commands.command(hidden=True)
    async def unload(self, ctx, *, extention):
        try:
            self.bot.unload_extension(f"cogs.{extention}")
            await ctx.message.add_reaction('a:SpectrumOkSpin:466480898049835011')
        except Exception:
            try:
                self.bot.unload_extension(extention)
                await ctx.message.add_reaction('a:SpectrumOkSpin:466480898049835011')
            except Exception as e:
                await ctx.send(f"Couldn't unload extention `{extention}`. Error: ```{e}```")

def setup(bot):
    bot.add_cog(OwnerCommands(bot))