import discord, asyncio, time, datetime, random, json, aiohttp, logging, os
from discord.ext import commands
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
                      "cogs.Bigemote"]

with open("databases/token.txt") as f:
    bottoken = f.read()

def get_prefix(bot, message):
    """Gets a prefix from a server"""

    default_prefix = "$"

    # Default prefix
    if not os.path.exists(f"servers/{message.guild.id}/"):
        return default_prefix
    else:
        if not os.path.isfile(f"servers/{message.guild.id}/prefix.txt"):
            return default_prefix
        else:
            with open(f"servers/{message.guild.id}/prefix.txt", "r") as f:
                return f.read()

bot = commands.Bot(command_prefix=get_prefix, description="no", case_insensitive=True)
bot.remove_command("help")
bot.launch_time = datetime.datetime.utcnow()

def is_owner(ctx):
        if ctx.message.author.id == "276707898091110400":
            return True
        return False

@bot.event
async def on_ready():
    print("=========\nConnected\n=========\n") # Confirmation is good
    await bot.change_presence(activity=discord.Game(name=(f"$help | {len(bot.guilds)} guilds!"), url=("https://go.twitch.tv/SpectrixYT"), type=random.randint(0,3)))

@bot.command()
async def ping(ctx):
    """Pings the bot 3 times and calculates the average"""
    # Prepare things
    msg = await ctx.send("`Pinging...`")
    times = []
    counter = 0

    # Ping
    for _ in range(3):
        counter += 1
        start = time.perf_counter()
        await msg.edit(content=f"Pinging... {counter}/3")
        end = time.perf_counter()
        speed = end - start
        times.append(round(speed * 1000))

    # Make embed
    embed = discord.Embed(title="More information:", description="Pinged 3 times and calculated the average.", colour=discord.Colour(value=defaultColour))
    embed.set_author(name="Pong!", icon_url=normalLogo)
    counter = 0
    for speed in times:
        counter += 1
        embed.add_field(name=f"Ping {counter}:", value=f"{speed}ms", inline=True)
    embed.add_field(name="Average speed", value=f"{round(sum(times) / 3)}ms")
    embed.set_thumbnail(url=gifLogo)
    embed.set_footer(text=f"Estimated total time elapsed: {round(sum(times))}ms")
    await msg.edit(content=f":ping_pong: **{round(sum(times) / 3)}ms**", embed=embed)

@bot.command()
async def uptime(ctx):
    delta_uptime = datetime.datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity=discord.Game(name=(f"$help | {len(bot.guilds)} guilds!")))

@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity=discord.Game(name=(f"$help | {len(bot.guilds)} guilds!")))

if __name__ == '__main__':
    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(bottoken)
