import datetime
import discord
from discord.ext import commands
import os
import time
from dalle3 import Dalle  # Assuming the provided Dalle3 class is named 'dalle3.py'

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
SAVE_DIRECTORY = 'images/'

bot = commands.Bot(command_prefix="!")
bot.launch_time = time.time()
dalle_instance = Dalle("YOUR_COOKIE_VALUE")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def generate(ctx, *, prompt: str):
    """Generates images based on the provided prompt"""
    await ctx.send(f"Generating images for prompt: `{prompt}`...")
    dalle_instance.run(prompt)
    for root, dirs, files in os.walk(SAVE_DIRECTORY):
        for filename in files:
            filepath = os.path.join(root, filename)
            await ctx.send(file=discord.File(filepath))


@bot.command()
async def helpme(ctx):
    """Displays help about bot usage"""
    help_text = (
        "Commands available:\n"
        "!generate <prompt>: Generate images based on prompt\n"
        "!ping: Check bot's responsiveness\n"
        "!setdir <directory>: Set directory for saving images\n"
        "!viewlast: View last generated image\n"
        "!clear: Clear bot messages\n"
        "!uptime: Get bot's uptime\n"
        "!restart: Restart the bot (owner only)"
    )
    await ctx.send(help_text)


@bot.command()
async def ping(ctx):
    """Pings the bot"""
    await ctx.send('Pong!')


@bot.command()
async def setdir(ctx, directory: str):
    """Set directory for saving images"""
    global SAVE_DIRECTORY
    SAVE_DIRECTORY = directory
    await ctx.send(f"Directory set to: {SAVE_DIRECTORY}")


@bot.command()
async def viewlast(ctx):
    """View last generated image"""
    images = sorted([os.path.join(SAVE_DIRECTORY, f) for f in os.listdir(SAVE_DIRECTORY) if os.path.isfile(os.path.join(SAVE_DIRECTORY, f))], key=os.path.getctime)
    if images:
        await ctx.send(file=discord.File(images[-1]))
    else:
        await ctx.send("No images generated yet!")


@bot.command()
async def clear(ctx, amount: int = 10):
    """Clear bot messages for neatness"""
    await ctx.channel.purge(limit=amount)


@bot.command()
async def uptime(ctx):
    """Gets the bot's uptime"""
    current_time = time.time()
    difference = int(round(current_time - bot.launch_time))
    text = str(datetime.timedelta(seconds=difference))
    await ctx.send(f"Bot has been up for: {text}")


@bot.command()
@commands.is_owner()
async def restart(ctx):
    """Restarts the bot (only accessible by the bot owner)"""
    await ctx.send("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)


@generate.error
async def generate_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must provide a prompt for image generation!")
    else:
        await ctx.send(f"An error occurred: {error}")


bot.run(TOKEN)
