from discord.ext import commands, tasks
import discord
import EzMudae
import asyncio
import shelve


class Mudae(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot
        self.mudae_wrap = EzMudae.Mudae(bot)
        self.data = shelve.open("data", writeback=True)
        self.channel = bot.get_channel(self.data.channel)
        self.server = self.bot.get_guild(self.data.server)
        self.mudae_role = self.server.get_role(self.data.role)

    async def wish_check(self, message: discord.Message):
        waifu = self.mudae_wrap.waifu_from(message)
        mention = ""
        if waifu and waifu.type == EzMudae.Waifu.Type.roll and not waifu.is_claimed:
            for player, wishes in self.data.wishes.items():
                if waifu.series.lower() in wishes or waifu.name.lower() in wishes:
                    mention = f"{mention} {player.mention},"
            if mention != "":
                await message.channel.send(f"Wished by {mention}")

    async def check_activity(self, message: discord.Message):
        if message.channel == self.channel and not message.author.bot:
            self.used_mudae.add(message.author)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await asyncio.gather(self.wish_check(message), self.check_activity(message))

    async def mention(self, message):
        mentions = str()
        for user in self.used_mudae:
            mentions = f"{mentions}{user.mention}, "
        await self.channel.send(f"{message} {mentions}")

    @tasks.loop()
    async def claims(self):
        await self.mudae_wrap.wait_claim()
        await self.mention("Claims have reset!")
        self.used_mudae = set()

    @tasks.loop()
    async def rolls(self):
        await self.mudae_wrap.wait_roll()
        await self.mention("Rolls have reset!")

    @claims.before_loop
    async def before_claims(self):
        await asyncio.sleep(60)

    @rolls.before_loop
    async def before_rolls(self):
        await asyncio.sleep(60)

    @commands.command(aliases=["w"])
    async def want(self, ctx: commands.context, name: str, k_value: str = None):
        if k_value is None:
            k_string = ""
        else:
            k_string = f" and is offering a girl worth {k_value} kakera"
        async for message in ctx.channel.history(limit=30):
            if message.author.id != EzMudae.MUDA or len(message.embeds) != 1:
                continue
            waifu = message.embeds[0].author.name
            if waifu[:len(name)].lower() == name.lower():
                await ctx.send(f"{self.mudae_role.mention} {ctx.author.mention} wants {waifu} at {message.jump_url}{k_string}")
                break

    @commands.command()
    async def wish(self, ctx: commands.context, *series):
        series = str(" ").join(series).lower()

        if ctx.author not in self.data.wishes:
            self.data.wishes[ctx.author] = []

        if series in self.data.wishes[ctx.author]:
            self.data.wishes[ctx.author].remove(series)
        else:
            self.data.wishes[ctx.author].append(series)

        await ctx.send("Done")

    @commands.command()
    async def view_wishes(self, ctx: commands.context, start: int = None, stop: int = None):
        if start is None:
            start = 0
        if stop is None:
            stop = len(self.data.wishes[ctx.author])
        if ctx.author not in self.data.wishes or self.data.wishes[ctx.author] == []:
            await ctx.send("No Wishes")
            return
        text = "```"
        for index, elem in enumerate(self.data.wishes[ctx.author][start: stop]):
            text = f"{text}\n{index:2}: {elem}"
        await ctx.send(f"{text}```")

    @commands.command(brief="Bot Owner")
    async def config_loops(self, ctx: commands.context, roll_time: int, claim_time: int):
        new_timing = EzMudae.get_timing(60, 180, roll_time, claim_time)
        await ctx.send(new_timing)