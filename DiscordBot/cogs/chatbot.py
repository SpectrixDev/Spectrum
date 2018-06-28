import discord
import asyncio
import random
import apiai
import json
from discord.ext import commands

CLIENT_ACCESS_TOKEN = '74a84564d7cc44cdb58b210c46f48f28'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

class chatbot:
    """Commands for the Spectrum Chatbot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def devChat(self, ctx, *, chatMsg):
        if ctx.message.author.id == "276707898091110400":
            await self.bot.send_typing(ctx.message.channel)
            request = ai.text_request()
            request.query = chatMsg
            response = json.loads(request.getresponse().read())

            result = response['result']
            timestamp = response['timestamp']

            action = result.get('action')
            resolvedQuery = result.get('resolvedQuery')
            intentName = result.get('intentName')
            score = result.get('score')
            fulfillment = result.get('fulfillment')
            speech = fulfillment.get('speech')

            actionIncomplete = result.get('actionIncomplete', False)

            emb = (discord.Embed(colour=0x3be801))
            emb.set_author(name="DevChat for SpectrumV2 Chatbot", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            emb.add_field(name="resolvedQuery", value=f"```{resolvedQuery}```", inline=False)
            emb.add_field(name="intentName", value=f"`{intentName}`")
            emb.add_field(name="score", value=f"`{score}`")
            if action == "":
                emb.add_field(name="action", value="`None assigned`")
            else:
                emb.add_field(name="action", value=f"`{action}`")
            if speech == "":
                emb.add_field(name="speech", value='```Somehow nothing. Spectrix, please fix.```', inline=False)
            else:
                emb.add_field(name="speech", value=f'```{speech}```', inline=False)
            emb.set_footer(text=f"Timestamp: {timestamp}")
            await self.bot.say(embed=emb)

        else:
            await self.bot.say("Sorry, this command is for my devs only. Please just mention me if you'd like to chat!")

def setup(bot):
    bot.add_cog(chatbot(bot))
