import discord
from discord.ext import commands
import operator


class WhosPlaying:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def whosplaying(self, ctx, *, game):
        """Shows who's playing a specific game"""
        if len(game) <= 1:
            await ctx.send("```The game should be at least 2 characters long...```", delete_after=5.0)
            return

        user = ctx.message.author
        server = ctx.message.server
        members = server.members
        playing_game = ""
        count_playing = 0

        for member in members:
            if not member:
                continue
            if not member.game or not member.game.name:
                continue
            if member.bot:
                continue
            if game.lower() in member.game.name.lower():
                count_playing += 1
                if count_playing <= 15:
                    playing_game += ">>> {} ({})\n".format(member.name, member.game.name)

        if playing_game == "":
            await self.bot.say("```Search results:\nNo users are currently playing that game.```")
        else:
            msg = playing_game
            em = discord.Embed(description=msg, colour=0x3be801)
            if count_playing > 15:
                showing = "(Showing 15/{})".format(count_playing)
            else:
                showing = "({})".format(count_playing)
            text = 'These are the people who are playing "{}":\n{}'.format(game, showing)
            em.set_author(name=text, icon_url='https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512')
            await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def currentgames(self, ctx):
        """Shows the most played games right now"""
        user = ctx.message.author
        server = ctx.message.server
        members = server.members

        freq_list = {}
        for member in members:
            if not member:
                continue
            if not member.game or not member.game.name:
                continue
            if member.bot:
                continue
            if member.game.name not in freq_list:
                freq_list[member.game.name] = 0
            freq_list[member.game.name] += 1

        sorted_list = sorted(freq_list.items(),
                             key=operator.itemgetter(1),
                             reverse=True)

        if not freq_list:
            await self.bot.say("```Search results:\nNo users are currently playing any games. Odd...```")
        else:
            # create display
            msg = ""
            max_games = min(len(sorted_list), 10)
            for i in range(max_games):
                game, freq = sorted_list[i]
                msg += ">>> {}: __{}__\n".format(game, freq_list[game])

            em = discord.Embed(description=msg, colour=0x3be801)
            em.set_author(name="Top games being played right now in the server:", icon_url='https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512')
            await self.bot.say(embed=em)



def setup(bot):
    n = WhosPlaying(bot)
    bot.add_cog(n)