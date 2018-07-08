import discord, asyncio, time, datetime, random, json, aiohttp, logging, os
from discord.ext import commands
from time import ctime

bottoken = ""
with open("databases/token.txt") as f:
    bottoken = f.read()

def get_prefix(bot, message):
    """Gets a prefix from a server"""

    default_prefix = "%"

    # Default prefix
    if not os.path.exists(f"servers/{message.guild.id}/"):
        return default_prefix
    else:
        if not os.path.isfile(f"servers/{message.guild.id}/prefix.txt"):
            return default_prefix
        else:
            with open(f"servers/{message.guild.id}/prefix.txt", "r") as f:
                return f.read()


desc = "spec gaey"
bot = commands.Bot(command_prefix=get_prefix, description=desc, case_insensitive=True)

bot.remove_command("help")
presenceGame = ":)" # this shit is so that the bot doesn't die
defaultColor = "0x36393e" # Basically a nice color that matches discord's bg in dark mode
typeGame = random.randint(0,3)

startup_extensions = [

]

@bot.event
async def on_ready():
    print("=========\nConnected\n=========\n") # Confirmation is good
    await bot.change_presence(activity=discord.Game(name=(f"{presenceGame} | {len(bot.guilds)} guilds!"), url=("https://twitch.tv/gdspectrix"), type=typeGame))

@bot.command()
async def ping(ctx):

    """Pings 5 times and gets the average speed to test out the bot"""

    # prepare things
    msg = await ctx.send("`Pinging...` ()")
    times = []
    counter = 0

    # ping
    for _ in range(5):
        counter += 1
        start = time.perf_counter()
        await msg.edit(content=f"`Pinging...` {counter}/5")
        end = time.perf_counter()
        speed = end - start
        times.append(round(speed * 1000))

    # make embed
    embed = discord.Embed(description="Pinged 5 times and calculated the average.")
    counter = 0
    for speed in times:
        counter += 1
        embed.add_field(name=f"Round {counter}", value=f"`{speed}ms`", inline=True)
    embed.add_field(name="Average", value=f"`{round(sum(times) / 5)}ms`")
    await msg.edit(content=":ping_pong: **Ping results!**", embed=embed)

@bot.command()
async def roast(ctx):
    """Insults users"""
    roast = random.choice(open("RoastList.txt").readlines())
    await ctx.send(roast)


if __name__ == '__main__':
    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(bottoken)
