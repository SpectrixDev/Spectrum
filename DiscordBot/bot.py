import discord
import asyncio
import time
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

# And now for some useless code that's awful

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")
commandUsage = "[None found owo]"
roast_database = "241"
presenceGame = ":)"
typeGame = "3"
CLIENT_ACCESS_TOKEN = 'no_stop_looking'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
dbltoken = "no"

startup_extensions = ['cogs.ownerCommands',
                      'cogs.getInfo',
                      'cogs.whosPlaying',
                      'cogs.subredditFetcher',
                      'cogs.spectrumPhone',
                      'cogs.bigEmote']


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


async def on_server_join(server):
    url = "https://discordbots.org/api/bots/" + bot.user.id + "/stats"
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data={"server_count": len(bot.servers)}, headers={"Authorization": dbltoken})
        await bot.change_presence(game=discord.Game(name=("$help on {0} servers!".format(len(bot.servers))),
                                                    url="https://go.twitch.tv/gdspectrix",
                                                    type=random.randint(0, 3)))


async def on_server_remove(server):
    url = "https://discordbots.org/api/bots/" + bot.user.id + "/stats"
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data={"server_count": len(bot.servers)}, headers={"Authorization": dbltoken})
        await bot.change_presence(game=discord.Game(name=("$help on {0} servers!".format(len(bot.servers))),
                                                    url="https://go.twitch.tv/gdspectrix",
                                                    type=random.randint(0, 3)))

async def on_command_error(discord.ext.commands.CommandNotFound, ctx):
    if ctx.message.content == "iq"or"insult"or"gay-scanner"or"dog"or"cat"or"spectrumchallenge":
        await bot.send_message(ctx.message.channel, "That command has been removed. Do $help to see the current commands ;)")
    else:
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
    if 89 < speedAverage < 125:
        speedComment = "Good"
    elif 125 < speedAverage < 175:
        speedComment = "Poor"
    elif speedAverage > 175:
        speedComment = "Very poor"
    elif 55 < speedAverage < 89:
        speedComment = "Great!"
    elif speedAverage < 55:
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


@bot.command(pass_context=True)
async def ship(ctx, name1 : discord.User, name2 : discord.User):
    """Test your love for another user/thing! Example: $ship [Spectrum] [Chocolate]"""
    shipnumber = random.randint(0,100)
    if shipnumber == "101":
        print("what")
    else:
        try:
            if int("0") < shipnumber < int("10"):
                    status = "Really low! {}".format(random.choice(["Friendzone ;(",
                                                                   'Just "friends"',
                                                                   '"Friends"',
                                                                    "Little to no love ;(",
                                                                    "There's barely any love ;("]))
            elif 10 < shipnumber < 20:
                status = "Low! {}".format(random.choice(["Still in the friendzone",
                                                        "Still in that friendzone ;(",
                                                        "There's not a lot of love there... ;("]))
            elif 20 < shipnumber < 30:
                status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!",
                                                        "But there's a small bit of love somewhere",
                                                        "I sense a small bit of love!",
                                                        "But someone has a bit of love for someone..."]))
            elif 30 < shipnumber < 40:
                status = "Fair! {}".format(random.choice(["There's a bit of love there!",
                                            "There is a bit of love there...",
                                            "A small bit of love is in the air..."]))
            elif 40 < shipnumber < 60:
                status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO",
                                                             "It appears one sided!",
                                                            "There's some potential!",
                                                             "I sense a bit of potential!",
                                                            "There's a bit of romance going on here!",
                                                            "I feel like there's some romance progressing!",
                                                            "The love is getting there..."]))
            elif 60 < shipnumber < 70:
                status = "Good! {}".format(random.choice(["I feel the romance progressing!",
                                                        "There's some love in the air!",
                                                        "I'm starting to feel some love!"]))
            elif 70 < shipnumber < 80:
                status = "Great! {}".format(random.choice(["There is definitely love somewhere!",
                                                        "I can see the love is there! Somewhere...",
                                                        "I definitely can see that love is in the air"]))
            elif 80 < shipnumber < 90:
                status = "Over average! {}".format(random.choice(["Love is in the air!",
                                                                "I can definitely feel the love",
                                                                "I feel the love! There's a sign of a match!",
                                                                "There's a sign of a match!",
                                                                "I sense a match!",
                                                                "A few things can be imporved to make this a match made in heaven!"]))
            elif 90 < shipnumber < 100:
                status = "True love! {}".format(random.choice(["It's a match!",
                                                            "There's a match made in heaven!",
                                                            "It's definitely a match!",
                                                            "Love is truely in the air!",
                                                            "Love is most definitely in the air!"]))

            emb = (discord.Embed(title="Love test for:", description="**{0}** and **{1}** {2}".format(name1.name, name2.name, random.choice([":sparkling_heart:",
                                                                                                                                                   ":heart_decoration:",
                                                                                                                                                   ":heart_exclamation:",
                                                                                                                                                   ":heartbeat:",
                                                                                                                                                   ":heartpulse:",
                                                                                                                                                   ":hearts:",
                                                                                                                                                   ":blue_heart:",
                                                                                                                                                   ":green_heart:",
                                                                                                                                                   ":purple_heart:",
                                                                                                                                                   ":revolving_hearts:",
                                                                                                                                                   ":yellow_heart:",
                                                                                                                                                   ":two_hearts:"]), colour=0x3DF270)))
            emb.add_field(name="Results:", value="{}%".format(shipnumber), inline=True)
            emb.add_field(name="Status:", value=(status), inline=False)
            emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
            await bot.say(embed=emb)

        except TypeError:
            bot.say("oops idk what just happened lol")


@bot.command(name="8ball", pass_context=True)
async def _ball(ctx, *, _ballInput):
    """Ask the magic 8 ball any question!"""
    if _ballInput == ""or" ":
        bot.say(errorMessage)
        pass
    choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
    try:
        if choiceType == "(Affirmative)":
            prediction = random.choice(["It is certain :8ball:", "It is decidedly so :8ball:", "Without a doubt :8ball:", "Yes, definitely :8ball:", "You may rely on it :8ball:", "As I see it, yes :8ball:","Most likely :8ball:", "Outlook good :8ball:", "Yes :8ball:", "Signs point to yes :8ball:"])
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
            emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
            await bot.say(embed=emb)
        elif choiceType == "(Non-committal)":
            prediction = random.choice(["Reply hazy try again :8ball:", "Ask again later :8ball:", "Better not tell you now :8ball:", "Cannot predict now :8ball:", "Concentrate and ask again :8ball:"])
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
            emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
            await bot.say(embed=emb)
        elif choiceType == "(Negative)":
            prediction = random.choice(["Don't count on it :8ball:", "My reply is no :8ball:", "My sources say no :8ball:", "Outlook not so good :8ball:", "Very doubtful :8ball:"])
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))
            emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
            await bot.say(embed=emb)

    except Exception as e:
        bot.say(errorMessage)


@bot.command(name="database", pass_context=True)
async def database(ctx, databaseType):
    """Current databases:\nroast"""
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
async def presence(ctx, typeGame: int, presenceGame):
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
            number = int(number)
            await bot.purge_from(ctx.message.channel, limit = number)
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
                    await bot.send_message(message.channel, "**I sent you help in your DMs :mailbox_with_mail:**")
                else:
                    await bot.send_message(message.channel, f"{message.author.mention} {response['result']['fulfillment']['speech']}")

                print ("Chatted with a user on the server: {0}. Time: {1}".format((message.server.name), datetime.datetime.now().time()))

        except KeyError:
            await bot.send_message(message.channel, "`Error: 'KeyError', make sure you gave not too little input and not too much ;)`")


if __name__ == '__main__':

    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run('token')
