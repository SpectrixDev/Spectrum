import dbl
import discord
from discord.ext import commands

import aiohttp
import asyncio
import logging


class dblUpdater:
    """Handles interactions with the discordbots.org API. Mostly copy pasted from https://discordbots.org/api/docs#pylib"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'no'
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count""" # Will probably make it each time the bot is added to a server

        while True:
            logger.info('attempting to post server count')
            try:
                await self.dblpy.post_server_count()
                logger.info('posted server count ({})'.format(len(self.bot.guilds)))
            except Exception as e:
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(dblUpdater(bot))
