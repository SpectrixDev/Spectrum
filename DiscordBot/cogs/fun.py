import discord
import asyncio
import random
from discord.ext import commands

class fun:
    """Some fun commands made for entertainment"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def combine(self, ctx, name1, name2):
        name1letters = name1[:round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2):]
        ship = "".join([name1letters, name2letters])
        await self.bot.say(ship)
    
    @commands.command(pass_context=True)
    async def ship(self, ctx, name1 : discord.User, name2 : discord.User):
        """Test your love for another user"""
        shipnumber = random.randint(0,100)
        if 0 == shipnumber <= 10:
            status = "Really low! {}".format(random.choice(["Friendzone ;(", 'Just "friends"', '"Friends"', "Little to no love ;(", "There's barely any love ;("]))
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(random.choice(["Still in the friendzone", "Still in that friendzone ;(", "There's not a lot of love there... ;("]))
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!", "But there's a small bit of love somewhere", "I sense a small bit of love!", "But someone has a bit of love for someone..."]))
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(random.choice(["There's a bit of love there!", "There is a bit of love there...", "A small bit of love is in the air..."]))
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO", "It appears one sided!", "There's some potential!", "I sense a bit of potential!", "There's a bit of romance going on here!", "I feel like there's some romance progressing!", "The love is getting there..."]))
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(random.choice(["I feel the romance progressing!", "There's some love in the air!", "I'm starting to feel some love!"]))
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(random.choice(["There is definitely love somewhere!", "I can see the love is there! Somewhere...", "I definitely can see that love is in the air"]))
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(random.choice(["Love is in the air!", "I can definitely feel the love", "I feel the love! There's a sign of a match!", "There's a sign of a match!", "I sense a match!", "A few things can be imporved to make this a match made in heaven!"]))
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(random.choice(["It's a match!", "There's a match made in heaven!", "It's definitely a match!", "Love is truely in the air!", "Love is most definitely in the air!"]))

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        emb = (discord.Embed(color=shipColor, title="Love test for:", description="**{0}** and **{1}** {2}".format(name1.name, name2.name, random.choice([":sparkling_heart:", ":heart_decoration:", ":heart_exclamation:", ":heartbeat:", ":heartpulse:", ":hearts:", ":blue_heart:", ":green_heart:", ":purple_heart:", ":revolving_hearts:", ":yellow_heart:", ":two_hearts:"]), colour=0x3DF270)))
        emb.add_field(name="Results:", value="{}%".format(shipnumber), inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
        await self.bot.say(embed=emb)


    @commands.command(name="8ball", pass_context=True)
    async def _ball(self, ctx, *, _ballInput):
        """Ask the magic 8 ball any question!"""
        choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
        if choiceType == "(Affirmative)":
            prediction = random.choice(["It is certain :8ball:", "It is decidedly so :8ball:", "Without a doubt :8ball:", "Yes, definitely :8ball:", "You may rely on it :8ball:", "As I see it, yes :8ball:","Most likely :8ball:", "Outlook good :8ball:", "Yes :8ball:", "Signs point to yes :8ball:"])
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
        elif choiceType == "(Non-committal)":
            prediction = random.choice(["Reply hazy try again :8ball:", "Ask again later :8ball:", "Better not tell you now :8ball:", "Cannot predict now :8ball:", "Concentrate and ask again :8ball:"])
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
        elif choiceType == "(Negative)":
            prediction = random.choice(["Don't count on it :8ball:", "My reply is no :8ball:", "My sources say no :8ball:", "Outlook not so good :8ball:", "Very doubtful :8ball:"])
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))

        emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
        await self.bot.say(embed=emb)

def setup(bot):
    bot.add_cog(fun(bot))
