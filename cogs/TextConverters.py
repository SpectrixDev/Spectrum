import discord, asyncio, random, time, datetime, binascii
from discord.ext import commands
from discord.ext.commands import clean_content

class TextConverters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['mock'])
    async def drunkify(self, ctx, *, s):
        lst = [str.upper, str.lower]
        newText = await commands.clean_content().convert(ctx, ''.join(random.choice(lst)(c) for c in s))
        if len(newText) <= 380:
            await ctx.send(newText)
        else:
            try:
                await ctx.author.send(newText)
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command()
    async def expand(self, ctx,  num: int, *, s: clean_content):
        spacing = ""
        if num > 0 and num <= 5:
            for _ in range(num):
                spacing+=" "
            result = spacing.join(s)
            if len(result) <= 200:
                await ctx.send(result)
            else:
                try:
                    await ctx.author.send(result)
                    await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
                except Exception:
                    await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
        else:
            await ctx.send("```fix\nError: The number can only be from 1 to 5```")

    @commands.command()
    async def reverse(self, ctx, *, s: clean_content):
        result = await commands.clean_content().convert(ctx, s[::-1])
        if len(result) <= 350:
            await ctx.send(f"{result}")
        else:
            try:
                await ctx.author.send(f"{result}")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command()
    async def texttohex(self, ctx, *, s):
        try:
            hexoutput = await commands.clean_content().convert(ctx, (" ".join("{:02x}".format(ord(c)) for c in s)))
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/hexadecimal/#data**")
        if len(hexoutput) <= 479:
            await ctx.send(f"```fix\n{hexoutput}```")
        else:
            try:
                await ctx.author.send(f"```fix\n{hexoutput}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command()
    async def hextotext(self, ctx, *, s):
        try:
            cleanS = await commands.clean_content().convert(ctx, bytearray.fromhex(s).decode())
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/hexadecimal/#data**")
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command()
    async def texttobinary(self, ctx, *, s):
        try:
            cleanS = await commands.clean_content().convert(ctx, ' '.join(format(ord(x), 'b') for x in s))
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**")
        if len(cleanS) <= 479:
            await ctx.send(f"```fix\n{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```fix\n{cleanS}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command()
    async def binarytotext(self, ctx, *, s):
        try:
            cleanS = await commands.clean_content().convert(ctx, ''.join([chr(int(s, 2)) for s in s.split()]))
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**")
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.group()
    async def specrypt(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("```fix\nInvalid input. Please use one of the following:\nencrypt (e)\ndecrypt (d)\n\nExample: $specrypt e Hello world!```")

    @specrypt.command(aliases=['e'])
    async def encrypt(self, ctx, *, s):
        a = ''
        try:
            for letter in s:
                a+=chr(ord(letter)+len(s))
            cleanS = await commands.clean_content().convert(ctx, a)
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the input is malformed. Sorry, I'm not perfect and my creator is dumb**")
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @specrypt.command(aliases=['d'])
    async def decrypt(self, ctx, *, s):
        a = ''
        try:
            for letter in s:
                a+=chr(ord(letter)-len(s))
            cleanS = await commands.clean_content().convert(ctx, a)
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the input is malformed. Sorry, I'm not perfect and my creator is dumb**")
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

def setup(bot):
    bot.add_cog(TextConverters(bot))
