import discord, datetime, time, aiohttp, asyncio, random
from discord.ext import commands
from random import randint
from random import choice
from urllib.parse import quote_plus
from collections import deque

acceptableImageFormats = [".png",".jpg",".jpeg",".gif",".gifv",".webm",".mp4","imgur.com"]
memeHistory = deque()
memeSubreddits = ["BikiniBottomTwitter", "memes", "2meirl4meirl", "deepfriedmemes", "MemeEconomy"]

async def getSub(self, ctx, sub):
        """Get stuff from requested sub"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.reddit.com/r{sub}/hot.json?limit=100") as response:
                request = await response.json()

        attempts = 1
        while attempts < 5:
            if 'error' in request:
                print("failed request {}".format(attempts))
                await asyncio.sleep(2)
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://www.reddit.com/r/{sub}/hot.json?limit=100") as response:
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

class SubredditFetcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
      async with ctx.typing(): #loading the meme takes a couple moments, this lets the user know the bot is working on it
        """Memes from various subreddits (excluding r/me_irl. some don't understand those memes)"""
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
                        for j, v, in enumerate(acceptableImageFormats): 
                            if v in urlLower:
                                accepted = True
                        if accepted:
                            if url not in memeHistory:
                                memeHistory.append(url)  
                                if len(memeHistory) > 63: 
                                    memeHistory.popleft() 

                                break 
                await ctx.send(memeHistory[len(memeHistory) - 1])
                return
        await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))
    
    @commands.command()
    async def showerthought(self, ctx):
      async with ctx.typing():
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
                                memeHistory.append(url)
                                if len(memeHistory) > 63:
                                    memeHistory.popleft()

                                break
                await ctx.send(memeHistory[len(memeHistory) - 1])
                return
        await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))

    
    @commands.command(aliases=['dankmeme', 'dank'])
    async def dankmemes(self, ctx):
      async with ctx.typing():
        await getSub(self, ctx, 'dankmemes')
        
    @commands.command()
    async def me_irl(self, ctx):
      async with ctx.typing():
        await getSub(self, ctx, 'me_irl')

    @commands.command()
    async def programmerhumor(self, ctx):
      async with ctx.typing():
        await getSub(self, ctx, 'ProgrammerHumor')

    @commands.command()
    async def surrealmemes(self, ctx):
      async with ctx.typing():
        await ctx.send("**This command has been moved to another bot due to popular demand. You can find that bot here:** https://discordbots.org/bot/532917889926299648")
    
    @commands.command(aliases=['hm', 'hmm', 'hmmmm', 'hmmmmm'])
    async def hmmm(self, ctx):
      async with ctx.typing():
        await ctx.send("**This command has been moved to another bot due to popular demand. You can find that bot here:** https://discordbots.org/bot/532917889926299648")

def setup(bot):
    bot.add_cog(SubredditFetcher(bot))
