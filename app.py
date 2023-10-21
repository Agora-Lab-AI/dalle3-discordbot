import datetime
import os
import sys
import time
import concurrent.futures

import discord
from dalle3 import Dalle
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import glob
import boto3

load_dotenv()

# AWS S3 Configuration (commented out in your original code)
# ... (keep this part unchanged if you decide to use it)

# Fetch keys from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DALLE_TOKEN = os.getenv("DALLE_TOKEN")

SAVE_DIRECTORY = "images/"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot.launch_time = time.time()
dalle_instance = Dalle(DALLE_TOKEN)

# Initialize the ThreadPoolExecutor
executor = concurrent.futures.ThreadPoolExecutor()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def generate(ctx, *, prompt: str):
    """Generates images based on the provided prompt"""
    await ctx.send(f"Generating images for prompt: `{prompt}`...")
    loop = asyncio.get_event_loop()

    # Initialize a Future object for the DALLE instance
    future = loop.run_in_executor(executor, dalle_instance.run, prompt)

    try:
        # Wait for the DALLE request to complete, with a timeout of 60 seconds
        await asyncio.wait_for(future, timeout=300)
        print("Done generating images!")

        # List all files in the SAVE_DIRECTORY
        all_files = [os.path.join(root, file) for root, _, files in os.walk(SAVE_DIRECTORY) for file in files]

        # Sort files by their creation time (latest first)
        sorted_files = sorted(all_files, key=os.path.getctime, reverse=True)

        # Get the 4 most recent files
        latest_files = sorted_files[:4]
        print(f"Sending {len(latest_files)} images to Discord...")

        # Send all the latest images in a single message
        await ctx.send(files=[discord.File(filepath) for filepath in latest_files])

    except asyncio.TimeoutError:
        await ctx.send("The request took too long! It might have been censored or you're out of boosts. Please try entering the prompt again.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")




# @bot.command()
# async def generate(ctx, *, prompt: str):
#     """Generates images based on the provided prompt"""
#     await ctx.send(f"Generating images for prompt: `{prompt}`...")

#     # Make a unique directory for this generation session using the message ID
#     session_save_directory = os.path.join(SAVE_DIRECTORY, str(ctx.message.id))
#     os.makedirs(session_save_directory, exist_ok=True)

#     # Offload the image generation to another thread.
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(executor, dalle_instance.run, prompt, session_save_directory)

#     # Get all the images saved in the session's directory.
#     generated_images = sorted(glob.glob(os.path.join(session_save_directory, '*')), key=os.path.getctime)

#     # Upload to S3 and send the URL to the user:
#     for image_path in generated_images:
#         file_name = os.path.basename(image_path)
#         s3.upload_file(image_path, S3_BUCKET_NAME, file_name, ExtraArgs={'ACL': 'public-read'})
        
#         image_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
#         await ctx.send(image_url)

#     # Cleanup: Optionally, delete the session's directory after sending the images.
#     for image_path in generated_images:
#         os.remove(image_path)
#     os.rmdir(session_save_directory)

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
    await ctx.send("Pong!")


@bot.command()
async def setdir(ctx, directory: str):
    """Set directory for saving images"""
    global SAVE_DIRECTORY
    SAVE_DIRECTORY = directory
    await ctx.send(f"Directory set to: {SAVE_DIRECTORY}")


@bot.command()
async def viewlast(ctx):
    """View last generated image"""
    images = sorted(
        [
            os.path.join(SAVE_DIRECTORY, f)
            for f in os.listdir(SAVE_DIRECTORY)
            if os.path.isfile(os.path.join(SAVE_DIRECTORY, f))
        ],
        key=os.path.getctime,
    )
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
    os.execv(sys.executable, ["python"] + sys.argv)


@generate.error
async def generate_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must provide a prompt for image generation!")
    else:
        await ctx.send(f"An error occurred: {error}")


bot.run(DISCORD_TOKEN)
