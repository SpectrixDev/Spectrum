import discord, asyncio, json, os, time, datetime, aiohttp, pathlib
from datetime import datetime
from discord.ext import commands
from collections import Counter

BOOT = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

class Spectrum(commands.AutoShardedBot):
    def __init__(self, config: dict):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            case_insensitive=True,
            description="deez"  # nopep8
        )
        self.config = config
        self.owners = set(config.get("owners", {}))
        self.uptime = datetime.now()
        self.debug_mode = config.get("debug_mode", True)
        self.command_usage = Counter()
        self.db = None
        self.remove_command('help')

    async def is_owner(self, user):
        return user.id in self.owners or await super().is_owner(user)

    async def on_ready(self):
        await self.update()
        print("--" * 15)
        print(f"{self.user} is ready\n")
        print(f"ID:            {self.user.id}")
        print(f"Created_At:    {self.user.created_at}")
        print(f"User Count:    {len(set(self.get_all_members()))}")
        print(f"Channels:      {len(set(self.get_all_channels()))}")
        print(f"Guilds:        {len(self.guilds)}")
        print(f"Debug:         {str(self.debug_mode)}")
        print(f"--" * 15)
    
    async def on_resumed(self):
        print("Resumed..")

    async def login(self, *args, **kwargs):
        print("BOOT @ %s" % BOOT)
        print("Connecting to discord...")

        self.session = aiohttp.ClientSession(json_serialize=json.dumps)
        adapter = discord.AsyncWebhookAdapter(self.session)
        self.webhook = discord.Webhook.from_url(self.config["webhook_url"], adapter=adapter)

        extensions = [x.as_posix().replace("/", ".").replace(".py", "") for x in pathlib.Path("cogs").iterdir() if x.is_file()]
        extensions.append("jishaku")

        for ext in extensions:
            try:
                self.load_extension(ext)
                print("Loaded extension: %s " % ext)

            except commands.ExtensionFailed as e:
                print(f"Extension {ext} failed to load: {e}")

            except commands.ExtensionNotFound:
                print("Extension %s cannot be found" % ext)

            except commands.NoEntryPointError:
                print("Extension %s has no setup function" % ext)
        await super().login(*args, **kwargs)

    async def update(self):
        activity = discord.Activity(
            type=3,
            name=f"scat",
            url="https://www.twitch.tv/SpectrixYT"
        )
        await self.change_presence(activity=activity)

        if self.config.get("dbl_token") and not self.debug_mode:
            payload = {"server_count": len(self.guilds)}
            headers = {"Authorization": self.config["dbl_token"]}
            url = "https://top.gg/api/bots/%d/stats" % self.user.id
            async with self.session.post(url, json=payload, headers=headers) as resp:  # nopep8
                try:
                    data = await resp.json()
                    print("Recieved %s %s %d %s", resp.method, resp._url, resp.status, data)
                except (TypeError, ValueError):
                    print("Recieved %s %s %d", resp.method, resp._url, resp.status)


    async def close(self):
        try:
            await self.session.close()
            await self.db.close()
        except (RuntimeError, AttributeError):
            pass
            
        await super().close()


if __name__ == "__main__":
    with open("config.json") as file:
        config = json.load(file)
    h = Spectrum(config=config)
    h.run(config["bot_token"])