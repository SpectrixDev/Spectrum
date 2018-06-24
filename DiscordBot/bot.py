import discord
import asyncio
import time
from time import ctime
import datetime
import random
import requests
import os
import sys
import json
import subprocess
import inspect
import aiohttp
from collections import deque
import urllib.request
from urllib.request import urlopen,Request
from   os.path import splitext
from   discord.ext import commands

try:

    import apiai

except ImportError:

    sys.path.append(

        os.path.join(

            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            os.pardir

        )
    )

    import apiai

# Tokens (changed for GitHub)
bot_run_token = "y"
CLIENT_ACCESS_TOKEN = 'u'
dbltoken = "lookin?"

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")
roast_database = "241"
presenceGame = ":)"
typeGame = "3"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

startup_extensions = ['cogs.ownerCommands',
                      'cogs.getInfo',
                      'cogs.whosPlaying',
                      'cogs.subredditFetcher',
                      'cogs.SpectrumPhone',
                      'cogs.bigEmote',
                      'cogs.fun']

@bot.event
async def on_ready():
    # Startup
    print("=========\nConnected\n=========\n")
    print("Current servers: {}".format(len(bot.servers)))
    print("Time on start: {}".format(datetime.datetime.now()))
    # DBL Publishing
    url = "https://discordbots.org/api/bots/" + bot.user.id + "/stats"
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data={ "server_count": len(bot.servers) }, headers={"Authorization": dbltoken})
        await bot.change_presence(game=discord.Game(name=("$help on {0} servers!".format(len(bot.servers))),
                                                        url="https://go.twitch.tv/gdspectrix",
                                                        type=random.randint(0, 3)))
    print("\nStartup successful. Ready for use!\n")


def is_owner(ctx):
        if ctx.message.author.id == "276707898091110400":
            return True
        return False

@bot.event
async def on_server_join(server):
    url = "https://discordbots.org/api/bots/" + bot.user.id + "/stats"
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data={"server_count": len(bot.servers)}, headers={"Authorization": dbltoken})
        await bot.change_presence(game=discord.Game(name=("$help on {0} servers!".format(len(bot.servers))),
                                                    url="https://go.twitch.tv/gdspectrix",
                                                    type=random.randint(0, 3)))

@bot.event
async def on_server_remove(server):
    url = "https://discordbots.org/api/bots/" + bot.user.id + "/stats"
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data={"server_count": len(bot.servers)}, headers={"Authorization": dbltoken})
        await bot.change_presence(game=discord.Game(name=("$help on {0} servers!".format(len(bot.servers))),
                                                    url="https://go.twitch.tv/gdspectrix",
                                                    type=random.randint(0, 3)))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send(f"```Error: NotPrivateMessage ({ctx.command} can not be used in Private Messages.)```")
        except:
            pass
    elif isinstance(error, commands.BadArgument):
        try:
            return await ctx.author.send("```Error: BadArgument```")
        except:
            pass

@bot.command(pass_context=True)
async def ping():
    t1 = time.perf_counter()
    ping1 = await bot.say("Pinging... 1/3")
    t2 = time.perf_counter()
    speed = t2 - t1
    speed1 = round(speed * 1000)
    t1 = time.perf_counter()
    await bot.edit_message(ping1, "Pinging.... 2/3")
    t2 = time.perf_counter()
    speed = t2 - t1
    speed2 = round(speed * 1000)
    t1 = time.perf_counter()
    await bot.edit_message(ping1, "Pinging..... 3/3")
    t2 = time.perf_counter()
    speed = t2 - t1
    speed3 = round(speed * 1000)
    speedAverage = round((speed1+speed2+speed3)/3)
    if 89 < speedAverage <= 125:
        speedComment = "Good"
    elif 125 < speedAverage <= 175:
        speedComment = "Poor"
    elif speedAverage > 175:
        speedComment = "Very poor"
    elif 55 < speedAverage <= 89:
        speedComment = "Great!"
    elif speedAverage <= 55:
        speedComment = "Very fast!"
    else:
        speedComment = "Idk lol"

    pingEmbed = discord.Embed(description="Pinged 3 times and calculated the avarage.", colour=discord.Colour(value=0x3be801))
    pingEmbed.set_author(name="Pong!")
    pingEmbed.set_thumbnail(url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
    pingEmbed.add_field(name="First ping:", value="{0}ms".format(speed1), inline=True)
    pingEmbed.add_field(name="Second ping:", value="{0}ms".format(speed2), inline=True)
    pingEmbed.add_field(name="Third ping:", value="{0}ms".format(speed3), inline=True)
    pingEmbed.add_field(name="Speed comment:", value=speedComment, inline=True)
    pingEmbed.add_field(name=">> Average speed: <<", value=">> {0}ms <<".format(speedAverage), inline=False)
    pingEmbed.set_footer(text="Estimated total time elapsed: {0}ms".format(speed1+speed2+speed3))
    await bot.delete_message(ping1)
    await bot.say(embed=pingEmbed)


@bot.command(name="database", pass_context=True)
async def database(ctx, databaseType):
    """Current databases:\nroast""" # lol that's all
    if databaseType == "roast":
        await bot.say("**My roast database consists of `{0}` roasts**".format(roast_database))
    else:
        await bot.say("```Incorrect input. Try $help database.\nCurrent databases:\nroast```")


@bot.command(name="roast", pass_context=True)
async def roast(ctx):
    """Insults picked and created by Spectrix specifically for the bot."""
    roast = random.choice(open("RoastList.txt").readlines())
    await bot.say(roast)


@bot.command(name="poll", pass_context=True)
async def poll(ctx, *, pollInfo):
    """Creates a simple poll within the server"""
    emb = (discord.Embed(description=pollInfo, colour=0x3be801))
    emb.set_author(name="Add your vote!", icon_url="https://lh3.googleusercontent.com/7ITYJK1YP86NRQqnWEATFWdvcGZ6qmPauJqIEEN7Cw48DZk9ghmEz_bJR2ccRw8aWQA=w300")
    emb.set_footer(text="Poll created by {}".format(ctx.message.author))
    try:
        await bot.delete_message(ctx.message)
    except discord.Forbidden:
        pass
    pollMessage = await bot.say(embed=emb)
    await bot.add_reaction(pollMessage, "\N{THUMBS UP SIGN}")
    await bot.add_reaction(pollMessage, "\N{THUMBS DOWN SIGN}")


@bot.command(name="presence", pass_context=True)
async def presence(ctx, typeGame: int, *, presenceGame):
    """Changes the bot's presence"""
    if ctx.message.author.id == "276707898091110400":
        await bot.change_presence(game=discord.Game(name=("{0} | {1} servers!".format(presenceGame, len(bot.servers))), url=("https://go.twitch.tv/gdspectrix"), type=typeGame))
        await bot.say("Done!")
    else:
        await bot.say("No. (Only Spectrix can do that)")


@commands.has_permissions(manage_messages=True)
@bot.command(name="clear", pass_context=True)
async def clear(ctx, number):
        try:
            await bot.purge_from(ctx.message.channel, limit = (int(number) + 1))
            await asyncio.sleep(1)
            clearConfirmation = await bot.say("**Cleared `{}` messages from this channel**".format(number))
            await bot.add_reaction(clearConfirmation, "\N{OK HAND SIGN}")
            await asyncio.sleep(4)
            await bot.delete_message(clearConfirmation)

        except discord.Forbidden:
            await bot.say("```I seem to have missing permissions. I need the manage_message permission to preform this action.```")


@bot.command(name="invite", pass_context=True)
async def invite(ctx):
    await bot.send_message(ctx.message.author, "**https://bit.ly/SpectrumDiscord**\n*Here's my invite link!*")
    await bot.say("**I sent you the invite link in your DMs :mailbox_with_mail:**")


@bot.command(name="support", pass_context=True)
async def support(ctx):
    await bot.send_message(ctx.message.author, "**https://discord.gg/ecXdjTD/**\n*Here's my official server! *")
    await bot.say("**I sent you the server invite in your DMs :mailbox_with_mail:**")


@bot.command(name="server", pass_context=True)
async def server(ctx):
    await bot.send_message(ctx.message.author, "**https://discord.gg/ecXdjTD/**\n*Here's my official server!*")
    await bot.say("**I sent you the server invite in your DMs :mailbox_with_mail:**")


@bot.command(name="help", pass_context=True)
async def help(ctx):
    await bot.send_message(ctx.message.author, "**https://spectrix.pythonanywhere.com/spectrum**\n*Here's my help page!*")
    await bot.say("**I sent you help in your DMs :mailbox_with_mail:**")


@bot.command(name="changelog", pass_context=True)
async def whatsnew(ctx):
    await bot.say("""```Finally, I have released SpectrumV2. I can actually be proud of this version. Anyways, here's some new stuff:\n\n
    The bot is completely rewritten in discord.ext (Python)\n
    New commands include SpectrumPhone™, currentgames, whosplaying, me_irl, bigemote, zalgo, userinfo, serverinfo, botinfo, clear, and more! (Do $help for more information)\n\n
    All commands actually work now, such as $ship\n
    Improved roasts, showerthoughts (now updated hourly), 8ball (ew), poll, ping, botinfo and basiclly everything else :)\n
    Removed stupid commands as well\n\n
    Also, rewritten the whole chatbot. It needs to learn a bit, so be patient :)\n
    And now I'm actually gonna work on the bot!```""")


@bot.listen()
async def on_message(message):
    if not message.author.bot and bot.user in message.mentions:
        try:
            if message.content.startswith("$"):
                pass
            else:
                await bot.send_typing(message.channel)
                user_message = message.content.replace(message.server.me.mention,'') if message.server else message.content

                request = ai.text_request()
                # will hopefully update to dialogflowV2 soon, not api.ai
                request.query = user_message

                response = json.loads(request.getresponse().read())

                result = response['result']
                action = result.get('action')
                actionIncomplete = result.get('actionIncomplete', False)

                if action == "user.requests.help":
                    await bot.send_message(message.author, "**https://spectrix.pythonanywhere.com/spectrum**\n*Here's my help page!*")
                    await bot.send_message(message.channel, f"** {message.author.mention} I sent you help in your DMs :mailbox_with_mail:**")
                elif action == "name.user.get":
                    await bot.send_message(message.channel, f"{message.author.mention} Your name is {message.author.name}.")
                elif action == "bot.time":
                    await bot.send_message(message.channel, f"{message.author.mention} The time for me is currently {ctime()}")

                else:
                    await bot.send_message(message.channel, f"{message.author.mention} {response['result']['fulfillment']['speech']}")

                print ("Chatted with a user on the server: {0}. Time: {1}".format((message.server.name), datetime.datetime.now().time()))

        except KeyError:
            await bot.send_message(message.channel, "`Error: 'KeyError', make sure you gave not too little input and not too much ;)`")


if __name__ == '__main__':

    for extension in startup_extensions:
        bot.load_extension(extension)

bot.run(bot_run_token)
