import settings
import cog
from discord.ext import commands

bot = commands.Bot(command_prefix=settings.prefix)  # DELETE THIS

# UNCOMMENT THIS
# bot = commands.Bot(command_prefix="YOUR PREFIX HERE")

bot.add_cog(cog.Mudae(bot))
bot.run(settings.token)  # DELETE THIS

# UNCOMMENT THIS FOR BOT
# bot.run("YOUR TOKEN HERE")


