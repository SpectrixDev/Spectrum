import discord, asyncio, qrcode, os, logging
from discord.ext import commands

class QRcode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['qrcode'])
    async def qr(self, ctx, *, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("temp/QR.png")
        await ctx.send(f"{ctx.author.mention}", file=discord.File("temp/QR.png"))
        os.remove("temp/QR.png")

def setup(bot):
    bot.add_cog(QRcode(bot))
