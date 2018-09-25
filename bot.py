import discord, asyncio, time, datetime, random, json, aiohttp, logging, os
from discord.ext import commands
from time import ctime
from os import listdir
from os.path import isfile, join

defaultColour = 0x36393e
gifLogo = "https://cdn.discordapp.com/attachments/323045050453852170/475197666716811275/SpectrumGIF.gif"
normalLogo = "https://cdn.discordapp.com/attachments/323045050453852170/475200894397579274/Spectrum.png"


lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
no_py = [s.replace('.py', '') for s in lst]
startup_extensions = ["cogs." + no_py for no_py in no_py]

with open("databases/thesacredtexts.json") as f:
    config = json.load(f)

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("$"),
                              owner_id=276707898091110400,
                              case_insensitive=True)

bot.remove_command("help")
bot.launch_time = datetime.datetime.utcnow()

url = "https://discordbots.org/api/bots/320590882187247617/stats"
headers = {"Authorization" : config["tokens"]["dbltoken"]}

def is_owner(ctx):
        if ctx.message.author.id == "276707898091110400":
            return True
        return False

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def update_activity():
    await bot.change_presence(
        activity=discord.Activity(
            name=f"@Spectrum help | {len(bot.guilds)} guilds!",
            type=1,
            url="https://www.twitch.tv/SpectrixYT"))

    payload = {"server_count"  : len(bot.guilds)}

    async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(
                url,
                data=payload,
                headers=headers)

@bot.event
async def on_ready():
    print("=========\nConnected\n=========\n")
    await update_activity()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command()
async def uptime(ctx):
    delta_uptime = datetime.datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

@bot.event
async def on_guild_join(guild):
    await update_activity()

@bot.event
async def on_guild_remove(guild):
    await update_activity()

if __name__ == '__main__':

    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(config["tokens"]["token"])