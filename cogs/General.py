import discord, asyncio, random, time, datetime, json, aiohttp, requests, logging, math, psutil, humanize, platform
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

with open("config.json") as f:
    config = json.load(f)

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as roastJson:
            return await roastJson.json()
class General(commands.Cog):
    """ General-use commands """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description="Calculates Round-Trip Time to the API, basically a fancy kinda ping")
    async def ping(self, ctx):
        """
        Calculates Round-Trip Time to the API, basically a fancy kinda ping
        """

        message = None

        # We'll show each of these readings as well as an average and standard deviation.
        api_readings = []
        # We'll also record websocket readings, but we'll only provide the average.
        websocket_readings = []

        # We do 6 iterations here.
        # This gives us 5 visible readings, because a request can't include the stats for itself.
        for _ in range(6):
            # First generate the text
            text = "**🤖 __Aight, calculating round-trip time...__ <a:pingpong:760170839332093964>**\n"
            text += "\n".join(f"> **Reading {index + 1}:** {reading * 1000:.2f}ms" for index, reading in enumerate(api_readings))

            if api_readings:
                average = sum(api_readings) / len(api_readings)

                if len(api_readings) > 1:
                    stddev = math.sqrt(sum(math.pow(reading - average, 2) for reading in api_readings) / (len(api_readings) - 1))
                else:
                    stddev = 0.0

                text += f"\n\n⏱ **Average:** {average * 1000:.2f} \N{PLUS-MINUS SIGN} {stddev * 1000:.2f}ms"
            else:
                text += "\n\nNo readings yet. <a:blue_note:760170836794802257>"

            if websocket_readings:
                average = sum(websocket_readings) / len(websocket_readings)

                text += f"\n**⌛ Websocket latency:** {average * 1000:.2f}ms"
            else:
                text += f"\n**⌛ Websocket latency:** {self.bot.latency * 1000:.2f}ms"

            # Now do the actual request and reading
            if message:
                before = time.perf_counter()
                await message.edit(content=text)
                after = time.perf_counter()

                api_readings.append(after - before)
            else:
                before = time.perf_counter()
                message = await ctx.send(content=text)
                after = time.perf_counter()

                api_readings.append(after - before)

            # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
            if self.bot.latency > 0.0:
                websocket_readings.append(self.bot.latency)
        

    @commands.command()
    async def uptime(self, ctx):
        """See how long the bot has been online for"""
        uptime = datetime.now() - self.bot.uptime
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"**Uptime:** {days}d, {hours}h, {minutes}m, {seconds}s 🚀⏳✨")


    # Creds to zedchance for original template. Added more styling and subcommand checks.
    @commands.command(name='help',
                      description='Help command',
                      aliases=['commands'])
    async def help_command(self, ctx, *commands: str):
        """ Shows this message """
        bot = ctx.bot
        prefix = config["prefix"]
        embed = discord.Embed(color=0xf03030)
        embed.set_author(name="Spectrum Help", icon_url=config['styling']['logo'])
        embed.set_footer(text="Made by Spectrix with love ❤", icon_url=config['styling']['logo'])

        def generate_usage(command_name):
            """ Generates a string of how to use a command """
            temp = f'{prefix}'
            command = bot.get_command(command_name)
            # Aliases
            if len(command.aliases) == 0:
                temp += f'{command_name}'
            elif len(command.aliases) == 1:
                temp += f'[{command.name}|{command.aliases[0]}]'
            else:
                t = '|'.join(command.aliases)
                temp += f'[{command.name}|{t}]'
            
            
            # Subcommands
            tempsubcommands = '<'
            for i in bot.walk_commands():
                if str(i).startswith(command.name) and len(str(i)) != len(command_name):
                    tempsubcommands += str(i)[len(command_name):] + '|'

            if tempsubcommands != '<':
                temp += ' ' + tempsubcommands[:-1].replace(" ", "") + '> <args>'
                return temp

            else:
                # Parameters
                params = f' '
                for param in command.clean_params:
                    params += f'<{command.clean_params[param]}> '
                temp += f'{params}'
                return temp

        def generate_command_list(cog):
            """ Generates the command list with properly spaced help messages """
            # Determine longest word
            max = 0
            for command in bot.get_cog(cog).get_commands():
                if not command.hidden:
                    if len(f'{command}') > max:
                        max = len(f'{command}')
            # Build list
            temp = ""
            for command in bot.get_cog(cog).get_commands():
                if command.hidden:
                    temp += ''
                elif command.help is None:
                    temp += f'• `{config["prefix"] + str(command)}`\n'
                else:
                    temp += f'• `{config["prefix"] + str(command)}` - {command.help}\n'
            return temp

        # Help by itself just lists our own commands.
        if len(commands) == 0:
            for cog in bot.cogs:
                temp = generate_command_list(cog)
                if temp != "":
                    embed.add_field(name=f'**{cog}**', value=temp, inline=True)
            embed.add_field(name=":information_source: More info:", inline=False, value="- **Type `"+config["prefix"]+"help command` for more info on a command.**\n"+
                                                    "- **You can also type `"+config["prefix"]+"help category` for more info on a category.**\n\n"+
                                                    "🥰 **Like what you see? Vote for me on [top.gg](https://top.gg/bot/753289892007510017/vote)!\n\n"+
                                                    "🔰 [[Add me to your server]](https://discord.com/oauth2/authorize?client_id=320590882187247617&scope=bot&permissions=201649223)\n\n"+
                                                    "❓ [[Support server]](https://discord.gg/ehR2Qw4GgN)\n\n🛠 [[GitHub]](https://github.com/SpectrixDev/Spectrum)**")
        elif len(commands) == 1:
            # Try to see if it is a cog name
            name = commands[0].capitalize()
            command = None

            if name in bot.cogs:
                cog = bot.get_cog(name)
                msg = generate_command_list(name)
                embed.add_field(name=name, value=msg, inline=False)
                msg = f'{cog.description}\n'
                embed.set_footer(text=msg)

            # Must be a command then
            else:
                command = bot.get_command(name)
                if command is not None:
                    help = f''
                    if command.help is not None:
                        help = command.help
                    embed.add_field(name=f'**{command}**',
                                    value=f'{command.description}```{generate_usage(name)}```\n{help}',
                                    inline=False)
                else:
                    msg = ' '.join(commands)
                    embed.add_field(name="Not found", value=f'Command/category `{msg}` not found.')
        else:
            msg = ' '.join(commands)
            embed.add_field(name="Not found", value=f'Command/category `{msg}` not found.')

        return await ctx.send(f'{ctx.author.mention}', embed=embed)

    @commands.command()
    async def roast(self, ctx):
        response = requests.get(url="https://evilinsult.com/generate_insult.php?lang=en&type=json")
        roast = json.loads(response.text)
        await ctx.send(roast['insult'])

    @commands.command()
    async def invite(self, ctx):
        try:
            await ctx.author.send("**https://bit.ly/SpectrumDiscord**\n*Here's my invite link!*")
            helpMsg = await ctx.send("**I sent my invite link in your DMs :mailbox_with_mail:**")
        except Exception:
            helpMsg = await ctx.send(f"**{ctx.author.mention} https://bit.ly/SpectrumDiscord**\n*Here's my invite link!*")
        await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")
         
    @commands.command(aliases=['support'])
    async def server(self, ctx):
        try:
            await ctx.author.send("**https://discord.gg/Kghqehz**\n*Here's my official server!*")
            helpMsg = await ctx.send("**I sent you my server invite in your DMs :mailbox_with_mail:**")
        except Exception:
            helpMsg = await ctx.send(f"**{ctx.author.mention} https://discord.gg/Kghqehz/**\n*Here's my official server!*")
        await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.command()
    async def poll(self, ctx, *, pollInfo):
        emb = (discord.Embed(description=pollInfo, colour=0x36393e))
        emb.set_author(name=f"Poll by {ctx.message.author}", icon_url="https://lh3.googleusercontent.com/7ITYJK1YP86NRQqnWEATFWdvcGZ6qmPauJqIEEN7Cw48DZk9ghmEz_bJR2ccRw8aWQA=w300")
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        try:
            pollMessage = await ctx.send(embed=emb)
            await pollMessage.add_reaction("\N{THUMBS UP SIGN}")
            await pollMessage.add_reaction("\N{THUMBS DOWN SIGN}")
        except Exception as e:
            await ctx.send(f"Oops, I couldn't react to the poll. Check that I have permission to add reactions! ```py\n{e}```")

def setup(bot):
    bot.add_cog(General(bot))
