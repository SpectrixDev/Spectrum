import discord
from discord.ext import commands

#####################################
thinkingPages = "1"
#####################################

class EmoteFinder:
    def __init__(self, bot):
        self.bot = bot

        """ Finds emotes duh"""
        # Work in progress

    @commands.command(pass_context=True, no_pm=True)
    async def emote_finder(self, ctx):
        """Shows a list of many different emotes for the user to use"""
        em = discord.Embed(title="Different available categories", colour=discord.Colour(value=0x3be801))
        em.add_field(name="Thinking emotes:", value="$getemote <thinking> <page>", inline=True)
        em.add_field(name="Blobs:", value="$getemote <blobs> <page>", inline=True)
        em.add_field(name="Others:", value="$getemote <others> <page>", inline=True)
        em.set_footer(text="Original emotes belong to their original creators.")
        em.set_author(name="Spectrum's Emote Finder", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def getemote(self, ctx, emoteType, page):
        """Gets a list of current emotes for a selected category"""
        if emoteType == "thinking":
            em = discord.Embed(title="Thinking emotes", colour=discord.Colour(value=0x3be801))
            if page == "1":
                em.add_field(name="Thonk", value="https://tinyurl.com/thonk", inline=True)
                em.add_field(name="MegaThink", value="https://tinyurl.com/y7on8u8f", inline=True)
                em.add_field(name="ThinkOh", value="https://tinyurl.com/y8zs5n3u", inline=True)
                em.add_field(name="bhinking", value="https://tinyurl.com/ybl8r2qk", inline=True)
                em.add_field(name="ThinkEyes", value="https://tinyurl.com/y7bs858g", inline=True)
                em.add_field(name="HyperThink", value="https://tinyurl.com/y9vsumz9", inline=True)
                em.add_field(name="UltraHyperThink", value="https://tinyurl.com/ybwyspe4", inline=True)
                em.add_field(name="HmmThink", value="https://tinyurl.com/y9vtqsea", inline=True)
                em.add_field(name="RealisticThink", value="https://tinyurl.com/y9qfwjxef", inline=True)
                em.add_field(name="SpeedyRotateThink", value="https://tinyurl.com/y74uxnmt", inline=True)
                em.set_author(name="Spectrum's Emote Finder", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
                em.set_footer(text=f"Page 1/{thinkingPages} | Do $getemote thinking <page>")
                await self.bot.say(embed=em)

            else:
                await self.bot.say(f"```Error: Page doesn't exit. Current pages for thinking emotes: {thinkingPages}")
                
# Still working on this!
