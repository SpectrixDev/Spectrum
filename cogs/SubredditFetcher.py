import discord
from discord.ext import commands
from random import randint
from random import choice
from urllib.parse import quote_plus
import datetime
import time
import aiohttp
import asyncio
import random
from collections import deque

acceptableImageFormats = [".png",".jpg",".jpeg",".gif",".gifv",".webm",".mp4","imgur.com"]
memeHistory = deque()
memeSubreddits = ["dankmemes", "dankmeme", "memes", "2meirl4meirl", "deepfriedmemes", "MemeEconomy", "greentext"]

class SubredditFetcher:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def me_irl(self, ctx):
        """Memes from the only good sub"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.reddit.com/r/me_irl/hot.json?limit=100") as response:
                request = await response.json()

        attempts = 1
        while attempts < 5:
            if 'error' in request:
                print("failed request {}".format(attempts))
                await asyncio.sleep(2)
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.reddit.com/r/me_irl/hot.json?limit=100") as response:
                        request = await response.json()
                attempts += 1
            else:
                index = 0

                for index, val in enumerate(request['data']['children']):
                    if 'url' in val['data']:
                        url = val['data']['url']
                        urlLower = url.lower()
                        accepted = False
                        for j, v, in enumerate(acceptableImageFormats): #check if it's an acceptable image
                            if v in urlLower:
                                accepted = True
                        if accepted:
                            if url not in memeHistory:
                                memeHistory.append(url)  #add the url to the history, so it won't be posted again
                                if len(memeHistory) > 63: #limit size
                                    memeHistory.popleft() #remove the oldest

                                break #done with this loop, can send image
                await ctx.send(memeHistory[len(memeHistory) - 1]) #send the last image
                return
        await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))

    @commands.command()
    async def meme(self, ctx):
        """Memes from various subreddits (excluding r/me_irl as there is a seperate command due to lots of memes that many won't understand. i mean me too thanks)"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.reddit.com/r/{0}/hot.json?limit=100".format(random.choice(memeSubreddits))) as response:
                request = await response.json()

        attempts = 1
        while attempts < 5:
            if 'error' in request:
                print("failed request {}".format(attempts))
                await asyncio.sleep(2)
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.reddit.com/r/{0}/hot.json?limit=100".format(random.choice(memeSubreddits))) as response:
                        request = await response.json()
                attempts += 1
            else:
                index = 0

                for index, val in enumerate(request['data']['children']):
                    if 'url' in val['data']:
                        url = val['data']['url']
                        urlLower = url.lower()
                        accepted = False
                        for j, v, in enumerate(acceptableImageFormats): #check if it's an acceptable image
                            if v in urlLower:
                                accepted = True
                        if accepted:
                            if url not in memeHistory:
                                memeHistory.append(url)  #add the url to the history, so it won't be posted again
                                if len(memeHistory) > 63: #limit size
                                    memeHistory.popleft() #remove the oldest

                                break #done with this loop, can send image
                await ctx.send(memeHistory[len(memeHistory) - 1]) #send the last image
                return
        await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))

    @commands.command()
    async def showerthought(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.reddit.com/r/showerthoughts/hot.json?limit=100") as response:
                request = await response.json()

        attempts = 1
        while attempts < 5:
            if 'error' in request:
                print("failed request {}".format(attempts))
                await asyncio.sleep(2)
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.reddit.com/r/showerthoughts/hot.json?limit=100") as response:
                        request = await response.json()
                attempts += 1
            else:
                index = 0

                for index, val in enumerate(request['data']['children']):
                    if 'title' in val['data']:
                        url = val['data']['title']
                        urlLower = url.lower()
                        accepted = False
                        if url == "What Is A Showerthought?":
                            accepted = False
                        elif url == "Showerthoughts is looking for new moderators!":
                            accepted = False
                        else:
                            accepted = True
                        if accepted:
                            if url not in memeHistory:
                                memeHistory.append(url)  #add the url to the history, so it won't be posted again
                                if len(memeHistory) > 63: #limit size
                                    memeHistory.popleft() #remove the oldest

                                break #done with this loop, can send image
                await ctx.send(memeHistory[len(memeHistory) - 1]) #send the last image
                return
        await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))
        
def setup(bot):
    bot.add_cog(SubredditFetcher(bot))
