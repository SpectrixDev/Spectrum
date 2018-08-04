import discord, asyncio, random, time, datetime, qrcode, os
from discord.ext import commands
defaultColour = 0x36393e

class QRcode:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def qr(self, ctx, *, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        img = qr.make_image(fill_color="white", back_color="black")
        img.save("databases/qrcodes/QR.png")
        await ctx.send(f"{ctx.author.mention}", file=discord.File("databases/qrcodes/QR.png"))
        os.remove("databases/qrcodes/QR.png")

def setup(bot):
    bot.add_cog(QRcode(bot))