import asyncio, discord
import functools
import io
import os
import unicodedata

import aiohttp
from discord.ext import commands


class bigEmote(commands.Cog):

    """Makes your emotes bigger. Half stolen oof"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(pass_context=True, aliases=['bigemoji/'])
    async def bigemote(self, ctx, emoji):
        """Make a certain emote bigger"""
        try:
            if emoji[0] == '<':
                name = emoji.split(':')[1]
                emoji_name = emoji.split(':')[2][:-1]
                anim = emoji.split(':')[0]
                if anim == '<a':
                    url = f'https://cdn.discordapp.com/emojis/{emoji_name}.gif'
                else:
                    url = f'https://cdn.discordapp.com/emojis/{emoji_name}.png'
                try:
                    await ctx.send(url)
                except Exception as e:
                    print(e)
                    async with self.session.get(url) as resp:
                        if resp.status != 200:
                            await ctx.send('```Error: Emote not found.```')
                            return
                        img = await resp.read()

                    kwargs = {'parent_width': 1024, 'parent_height': 1024}
                    convert = False
                    task = functools.partial(bigEmote.generate, img, convert, **kwargs)
                    task = self.bot.loop.run_in_executor(None, task)
                    try:
                        img = await asyncio.wait_for(task, timeout=15)
                    except asyncio.TimeoutError:
                        await ctx.send("```Error: Timed Out. Try again in a few seconds")
                        return
                    await ctx.send(file=discord.File(img, filename=name + '.png'))
            
        except Exception as e:
            await ctx.send(f"```Error, couldn't send emote. Please tell my bot master\n{e}```")
    
    @staticmethod
    def generate(img, convert, **kwargs):
        img = io.BytesIO(img)
        return img


def setup(bot):
    bot.add_cog(bigEmote(bot))
