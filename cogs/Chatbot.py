import datetime, time, json, apiai, random, discord, asyncio, os, logging
from time import ctime
from discord.ext import commands

with open("databases/thesacredtexts.json") as f:
    config = json.load(f)
    ai = apiai.ApiAI(config["tokens"]["dialogflowtoken"])

class Chatbot(commands.Cog):
    """Kinda old, outdated, scuffed. Too lazy to update it honestly, it still works, its just nobody uses it. Was made for fun while initially learning py"""

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        message = ctx.message
        if isinstance(error, discord.ext.commands.CommandNotFound) and not message.author.bot and self.bot.user in message.mentions:
            try:
                if message.content.startswith(("$", "!", "?", "-", "*", "`", "~", "+", "/", ";", "=", "&", ">", ".")): # a bunch of generic checks to see if the bot is not supposed to reply
                    pass
                else:
                    async with message.channel.typing():
                        user_message = message.content.replace(f"{message.guild.me.mention} ",'') if message.guild else message.content
                        ctx = await self.bot.get_context(message)
                        if ctx.valid:
                            await self.bot.invoke(user_message)
                        else:
                            request = ai.text_request()
                            request.query = user_message

                            response = json.loads(request.getresponse().read())

                            result = response['result']
                            fulfillment = result['fulfillment']
                            speech = fulfillment['speech']
                            action = result.get('action')

                        if action == "user.requests.help":
                            try:
                                await message.author.send("**https://github.com/SpectrixOfficial/Spectrum**\n*Here's my help page!*")
                                helpMsg = await message.channel.send(f"**{message.author.mention} I sent you help in your DMs :mailbox_with_mail:**")
                            except Exception:
                                helpMsg = await message.channel.send(f"**{message.author.mention} https://github.com/SpectrixOfficial/Spectrum**\n*Here's my help page!*")
                                await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")
                        elif action == "user.requests.server":
                            try:
                                await message.author.send("**https://discord.gg/SuN49rm/**\n*Here's my official server!*")
                                helpMsg = await message.channel.send(f"**{message.author.mention} I sent you my server invite in your DMs :mailbox_with_mail:**")
                            except Exception:
                                helpMsg = await message.channel.send(f"**{message.author.mention} https://discord.gg/ecXdjTD/**\n*Here's my official server!*")
                                await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")
                        elif action == "user.requests.invite":
                            try:
                               await message.author.send("**https://bit.ly/SpectrumDiscord**\n*Here's my invite link!*")
                               helpMsg = await message.channel.send(f"**{message.author.mention} I sent my invite link in your DMs :mailbox_with_mail:**")
                            except Exception:
                                helpMsg = await message.channel.send(f"**{message.author.mention} https://bit.ly/SpectrumDiscord**\n*Here's my invite link!*")
                                await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")

                        elif action == "name.user.get":
                            await message.channel.send(f"{message.author.mention} Your name is {message.author.name}.")
                        elif action == "bot.time":
                            await message.channel.send(f"{message.author.mention} The time for me is currently {ctime()}")
                        elif action == "prefix.get":
                            await message.channel.send(f"{message.author.mention} My default prefix is `$`. But that's so 1983. Just **mention me with any command** ;)")
                        else:
                            await message.channel.send(f"{message.author.mention} {speech}")

            except Exception as e:
                await message.channel.send(f"{message.author.mention} ```fix\nWhoops! Something went wrong. Make sure you don't have too much or too little input!```")
                print(e)

    @commands.is_owner()
    @commands.command()
    async def devChat(self, ctx, *, chatMsg):
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
        emb = (discord.Embed(colour=0x36393e))
        emb.set_author(name="DevChat for SpectrumV2 Chatbot", icon_url=config["styling"]["logo"])
        emb.add_field(name="resolvedQuery", value=f"```{resolvedQuery}```", inline=False)
        emb.add_field(name="intentName", value=f"`{intentName}`")
        emb.add_field(name="score", value=f"`{score}`")
        if action == None:
            emb.add_field(name="action", value="`None assigned`")
        else:
            emb.add_field(name="action", value=f"`{action}`")
        if speech == None:
            emb.add_field(name="speech", value='```Somehow nothing. Spectrix, please fix.```', inline=False)
        else:
            emb.add_field(name="speech", value=f'```{speech}```', inline=False)
            emb.set_footer(text=f"Timestamp: {timestamp}")
            await ctx.send(embed=emb)

   

def setup(bot):
    bot.add_cog(Chatbot(bot))
