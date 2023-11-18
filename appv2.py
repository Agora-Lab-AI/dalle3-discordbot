import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# Fetch keys from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def generate(ctx, *, prompt: str = None):
    """Generates a response or image based on the provided prompt or image"""
    if prompt:
        # Text prompt provided, generate image with DALL·E 3
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=4
        )
        image_url = response.data[0].url
        await ctx.send(image_url)
    elif ctx.message.attachments:
        # Image attached, use GPT-4 with Vision
        image_url = ctx.message.attachments[0].url
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": {"image": image_url}}
            ],
            max_tokens=300
        )
        await ctx.send(response.choices[0].message['content'])
    else:
        await ctx.send("Please provide a text prompt or an image.")

@generate.error
async def generate_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must provide a prompt or an image!")
    else:
        await ctx.send(f"An error occurred: {error}")

bot.run(DISCORD_TOKEN)
