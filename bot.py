import discord, asyncio, time, datetime, random, json, aiohttp, logging, os
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from time import ctime

defaultColour = 0x36393e # Basically a nice color that matches discord's bg in dark mode
gifLogo = "https://cdn.discordapp.com/attachments/323045050453852170/475197666716811275/SpectrumGIF.gif" # r a i n b o w
normalLogo = "https://cdn.discordapp.com/attachments/323045050453852170/475200894397579274/Spectrum.png"

startup_extensions = ["cogs.General",
                      "cogs.Moderation",
                      "cogs.Fun",
                      "cogs.GetInfo",
                      "cogs.SubredditFetcher",
                      "cogs.WhosPlaying",
                      "cogs.OwnerCommands",
                      "cogs.Chatbot",
                      "cogs.QRcode",
                      "cogs.Bigemote",
                      "cogs.TextConverters"]

with open("databases/thesacredtexts.json") as f: # https://i.kym-cdn.com/entries/icons/original/000/025/082/sacredtexts.jpg
    config = json.load(f)

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("$"), description="no", case_insensitive=True)
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

@bot.event
async def on_ready():
    print("=========\nConnected\n=========\n")
    await bot.change_presence(activity=discord.Activity(name=f"@Spectrum help | {len(bot.guilds)} guilds!", type=1, url="https://www.twitch.tv/SpectrixYT"))
    payload = {"server_count"  : len(bot.guilds)}
    async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@commands.cooldown(1, 5, BucketType.user)
@bot.command()
async def ping(ctx):
    try:
        msg = await ctx.send("`Pinging bot latency...`")
        times = []
        counter = 0
   
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Pinging... {counter}/3")
            end = time.perf_counter()
            speed = end - start
            times.append(round(speed * 1000))

        embed = discord.Embed(title="More information:", description="Pinged 4 times and calculated the average.", colour=discord.Colour(value=defaultColour))
        embed.set_author(name="Pong!", icon_url=normalLogo)
        counter = 0
        for speed in times:
            counter += 1
            embed.add_field(name=f"Ping {counter}:", value=f"{speed}ms", inline=True)

        embed.add_field(name="Bot latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Average speed", value=f"{round((round(sum(times)) + round(bot.latency * 1000))/4)}ms")
        embed.set_thumbnail(url=gifLogo)
        embed.set_footer(text=f"Estimated total time elapsed: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(bot.latency * 1000))/4)}ms**", embed=embed)

@bot.command()
async def uptime(ctx):
    delta_uptime = datetime.datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity=discord.Activity(name=f"@Spectrum help | {len(bot.guilds)} guilds!", type=1, url="https://www.twitch.tv/SpectrixYT"))
    payload = {"server_count"  : len(bot.guilds)} 
    async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)
@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity=discord.Activity(name=f"@Spectrum help | {len(bot.guilds)} guilds!", type=1, url="https://www.twitch.tv/SpectrixYT"))
    payload = {"server_count"  : len(bot.guilds)}
    async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)
        
if __name__ == '__main__':

    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(config["tokens"]["token"])
