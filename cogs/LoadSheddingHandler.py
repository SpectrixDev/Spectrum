import time, json, asyncio, discord
from datetime import datetime
from httplib2 import Http
from urllib.parse import urlencode
from pytz import timezone
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class LoadSheddingHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['shedding', 'load-shedding'])
    async def LoadShedding(self, ctx):
        """ Return the current Loadshedding Stage
        0 = No load shedding
        1-3 = Stage 1-3
        """
        h = Http()
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 
               'Referer': 'https://loadshedding.eskom.co.za/', 
              'X-Requested-With': 'XMLHttpRequest'}

        timestamp=str(int(time.time()*1000))
        resp, content = h.request("http://loadshedding.eskom.co.za/LoadShedding/GetStatus?_="+timestamp, "GET", headers=headers)

        response = {}
        if int(resp['status']) == 200:
            response['status'] = 'Success'
            response['stage'] = int(content)-1
        else:
          response['status'] = 'Error'
        
        if response['stage'] == 0:
            loadsheddingnow = 'Currently not load shedding 😄'
        else:
            loadsheddingnow = 'Currently load shedding 😭'

        embed = discord.Embed(color=discord.Color(value=0x7628F1))
        embed.set_image(url="https://turntable.kagiso.io/images/SheddingSchedule2018English-2.original.jpg")
        embed.set_author(name="LoadShedding Info", url="http://loadshedding.eskom.co.za/", icon_url="https://cisp.cachefly.net/assets/articles/images/resized/0000585954_resized_eskomnew.jpg")

        embed.add_field(name="LoadShedding Status:", value=loadsheddingnow)
        embed.add_field(name="Stage:", value=(response['stage'] if response['stage'] != 0 else "None"), inline=False)
        embed.set_footer(text="Info from http://loadshedding.eskom.co.za/")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LoadSheddingHandler(bot))
