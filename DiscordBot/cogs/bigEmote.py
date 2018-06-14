import asyncio
import functools
import io
import os
import unicodedata

import aiohttp
from discord.ext import commands

try:
    import cairosvg
    cairo = True
except:
    cairo = False


class bigEmote:

    """Makes your emotes bigger"""
    # Half stolen xd

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(name="bigemote", pass_context=True)
    async def bigemote(self, ctx, emoji):
        """Make a certain emote bigger"""
        channel = ctx.message.channel

        if emoji[0] == '<':
            convert = False
            name = emoji.split(':')[1]
            emoji_name = emoji.split(':')[2][:-1]
            anim = emoji.split(':')[0]
            if anim == '<a':
                url = 'https://cdn.discordapp.com/emojis/' + emoji_name + '.gif'
            else:
                url = 'https://cdn.discordapp.com/emojis/' + emoji_name + '.png'
        else:
            chars = []
            name = []
            for char in emoji:
                chars.append(str(hex(ord(char)))[2:])
                try:
                    name.append(unicodedata.name(char))
                except ValueError:
                    name.append("none")
            name = '_'.join(name)
            if cairo:
                convert = True
                url = 'https://twemoji.maxcdn.com/2/svg/' + '-'.join(chars) + '.svg'
            else:
                convert = False
                url = 'https://twemoji.maxcdn.com/2/72x72/' + '-'.join(chars) + '.png'

        async with self.session.get(url) as resp:
            if resp.status != 200:
                await self.bot.say('```Error: Emote not found.```')
                return
            img = await resp.read()

        kwargs = {'parent_width': 1024,
                  'parent_height': 1024}

        task = functools.partial(bigEmote.generate, img, convert, **kwargs)
        task = self.bot.loop.run_in_executor(None, task)

        try:
            img = await asyncio.wait_for(task, timeout=15)
        except asyncio.TimeoutError:
            await self.bot.say("```Error: Timed Out. Try again in a few seconds")
            return

        if emoji.split(':')[0] == '<a':
            await self.bot.send_file(channel, img, filename=name + '.gif')
        else:
            await self.bot.send_file(channel, img, filename=name + '.png')

    @staticmethod
    def generate(img, convert, **kwargs):
        if convert:
            img = io.BytesIO(cairosvg.svg2png(bytestring=img, **kwargs))
        else:
            img = io.BytesIO(img)
        return img

    def __unload(self):
        self.session.close()


def setup(bot):
    n = bigEmote(bot)
    bot.add_cog(n)
