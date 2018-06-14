import discord
from discord.ext import commands
import aiohttp
import asyncio
import random

prefix = "$"

class SpectrumPhone:
    """Lets you chat with random person who has access to the bot."""

    def __init__(self, bot):
        self.bot = bot
        self.pool = {} # queue of users.id -> user channel
        self.link = {} # userid -> {target id, target user channel}
        self.colour = 0x3be801

    @commands.command(pass_context=True, no_pm=True)
    async def spectrumphone(self, ctx):
        """"Call" other people on different discord servers and have a little chat with them! Inspired by many bots :P"""
        user = ctx.message.author
        channel = ctx.message.channel
        server = user.server

        em = discord.Embed(description="SpectrumPhone is a way to talk to different users anonymously. To do this, you must message me in my DMs. Here are the commands you can use to get started!", colour=0x3be801)
        em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
        em.add_field(name="$joincall", value = "Puts you in a waiting list to be connected to partners")
        em.add_field(name="$next", value = "Changes your partners")
        em.add_field(name="$leavecall", value = "Hangs up the phone / takes you out of the waiting list")
        em.add_field(name="$phoneinfo", value = "Shows the current information about SpectrumPhone")
        em.set_thumbnail(url="http://www.emoji.co.uk/files/google-emojis/objects-android/7808-black-telephone.png")
        em.set_footer(text="REMEMBER: This only works in private messages!")

        await self.bot.say("**Check your DMs, I've sent instructions on how to use this command!** :mailbox_with_mail:")
        await self.bot.send_message(user, embed = em)

    async def direct_message(self, message):
        msg = message.content
        user = message.author
        channel = message.channel

        if channel.is_private and not msg.startswith(prefix) and user.id in self.link:
            target_channel = self.link[user.id]["TARGET_CHANNEL"]
            speakerName = "{0}#{1}:".format(message.author.name, message.author.discriminator)
            speakerPfp = message.author.avatar_url
            em = discord.Embed(description=msg, colour=0x3be801)
            em.set_author(name=speakerName, icon_url=speakerPfp)
            await self.bot.send_message(target_channel, embed = em)

        else:
            if channel.is_private:
                if msg == (prefix + "joincall"):
                    await self.add_to_pool(message)
                elif msg == (prefix + "leavecall"):
                    await self.remove_from_pool(message)
                elif msg == (prefix + "next"):
                    await self.get_next_user(message)
                elif msg == (prefix + "phoneinfo"):
                    await self.get_info(message)

    async def add_to_pool(self, message):
        user = message.author
        channel =  message.channel
        self.pool[user.id] = channel

        em = discord.Embed(description="**You have been added to the waiting list.**", colour=0x3be801)
        em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
        await self.bot.send_message(channel, embed = em)

    async def remove_from_pool(self, message):
        user = message.author
        channel =  message.channel

        if user.id in self.pool.keys():
            self.pool.pop(user.id)
            em = discord.Embed(description="**Leaving the SpectrumPhone waiting list.**", colour=0xE80303)
            em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            await self.bot.send_message(channel, embed = em)
        elif user.id in self.link.keys():
            # put partner back into pool
            partner_id = self.link[user.id]["TARGET_ID"]
            partner_channel = self.link[user.id]["TARGET_CHANNEL"]
            self.pool[partner_id] = partner_channel
            self.link.pop(partner_id)
            self.link.pop(user.id)

            em = discord.Embed(description="**Your partner has disconnected from the call.**", colour=0xE80303)
            em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            await self.bot.send_message(partner_channel, embed = em)

            em = discord.Embed(description="**You have disconnected from the call.**", colour=0xE80303)
            em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            await self.bot.send_message(channel, embed = em)
        else:
            em = discord.Embed(description="**Leaving SpectrumPhone call and waiting list.**", colour=0xE80303)
            em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            await self.bot.send_message(channel, embed = em)

    # puts both users back in the pool, but will go to same person if pool is small
    async def get_next_user(self, message):
        user = message.author
        channel =  message.channel

        if user.id in self.link.keys():
            # get partner information
            partner_id = self.link[user.id]["TARGET_ID"]
            partner_channel = self.link[user.id]["TARGET_CHANNEL"]
            self.pool[partner_id] = partner_channel
            self.pool[user.id] = channel

            self.link.pop(partner_id)
            self.link.pop(user.id)

            em = discord.Embed(description="**Your partner has disconnected.**", colour=0xE80303)
            em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            await self.bot.send_message(partner_channel, embed = em)

            em = discord.Embed(description="**Switching Users.**", colour=0xff6600)
            em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            await self.bot.send_message(channel, embed = em)

        elif user.id in self.pool.keys():
            em = discord.Embed(description="**You're still in the waiting list. Please wait.**", colour=0xff6600)
            em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            await self.bot.send_message(channel, embed = em)
        else:
            em = discord.Embed(description="**You are not in the waiting list. Please do `{}joincall`.**", colour=0xE80303)
            em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            await self.bot.send_message(channel, embed = em)

    async def get_info(self, message):
        channel =  message.channel

        em = discord.Embed(description="Call information", colour=0x3be801)
        em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
        em.add_field(name="Total users:", value = len(self.pool) + len(self.link), inline=False)
        em.add_field(name="Users currently in a call:", value = len(self.link), inline=False)
        em.add_field(name="Users currently not in any calls:", value = len(self.pool), inline=False)
        if len(self.pool) + len(self.link) == 0:
            phoneActivity = "No activity"
        elif len(self.pool) + len(self.link) < 3:
            phoneActivity = "Very little activity :("
        elif len(self.pool) + len(self.link) < 7:
            phoneActivity = "Fair activity"
        elif len(self.pool) + len(self.link) < 11:
            phoneActivity = "Good activity"
        elif len(self.pool) + len(self.link) < 27:
            phoneActivity = "Great activity!"
        elif len(self.pool) + len(self.link) < 51:
            phoneActivity = "Super active!"
        elif len(self.pool) + len(self.link) < 106:
            phoneActivity = "Incredibly super active! WOAH!"
        else:
            phoneActivity = "SO ACTIVE IT CAN'T BE REAL"
        em.add_field(name="Activity rating:", value = phoneActivity, inline=False)
        em.set_thumbnail(url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
        em.set_footer(text="Inspired by many, rewritten to be better (I hope).")
        await self.bot.send_message(channel, embed = em)

    async def create_link(self):
        while self == self.bot.get_cog('SpectrumPhone'):
            if len(self.pool) >= 2:
                # get two users
                user_one_id = random.choice(list(self.pool.keys()))
                user_one_channel = self.pool[user_one_id]
                self.pool.pop(user_one_id, None)

                user_two_id = random.choice(list(self.pool.keys()))
                user_two_channel = self.pool[user_two_id]
                self.pool.pop(user_two_id, None)

                self.link[user_one_id] = {"TARGET_ID": user_two_id, "TARGET_CHANNEL": user_two_channel}
                self.link[user_two_id] = {"TARGET_ID": user_one_id, "TARGET_CHANNEL": user_one_channel}

                em = discord.Embed(description="**Someone's picked up the phone! Say hello!**", colour=0x3be801)
                em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
                await self.bot.send_message(user_one_channel, embed = em)

                em = discord.Embed(description="**Someone's picked up the phone! Say hello!**", colour=0x3be801)
                em.set_author(name="SpectrumPhone™", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
                await self.bot.send_message(user_two_channel, embed = em)

            await asyncio.sleep(5)

    # I need to add antispam and maybe a limit for the calls?

def setup(bot):
    n = SpectrumPhone(bot)
    bot.add_listener(n.direct_message, 'on_message')
    bot.loop.create_task(n.create_link())
    bot.add_cog(n)
