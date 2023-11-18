[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)

# Dalle3 API Discord Bot
A discord bot for the dalle3 api


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Commands](#commands)

## Prerequisites

- Python 3.7 or higher
- A Discord bot token
- DALL-E 3 Unofficial API's cookie value

## Installation

1. **Clone the Repository**:

   ```bash
   git clonehttps://github.com/Agora-X/dalle3-discordbot.git
   cd dalle3-discordbot
   ```

   Replace `YOUR_REPOSITORY_URL` with the URL of your repository and `YOUR_REPOSITORY_NAME` with the name of your repository.

2. **Set Up a Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

   Make sure you have a `requirements.txt` file in the root of your repository with the following content:

   ```
   dalle3
   discord
   ```

## Configuration
- Get your openAI key
`export OPENAI_API_KEY=""`

## Running the Bot

With everything set up, you can now run the bot:

```bash
python app.py
```

Replace `app.py` with the actual name of your bot script.

Once running, you should see a message in the console indicating that the bot has logged in.

## Commands

- `!generate <prompt>`: Generates images based on the provided prompt.
- `!helpme`: Displays help about bot usage.
- `!ping`: Check bot's responsiveness.
- `!setdir <directory>`: Set directory for saving images.
- `!viewlast`: View the last generated image.
- `!clear [amount]`: Clear bot messages. `amount` defaults to 10 if not provided.
- `!uptime`: Get bot's uptime.
- `!restart`: Restart the bot (owner only).


# Note
- 1 only generation at a time
- cookie expires
- will output the most 4 recent images in time


# Todo
- make a playwright verison
- Make censorship detection if it waits, Should code some censorship detection to send a message that it couldn’t generated
- Also suggested trying playwright with a manual login instead of this cookie thing if OpenAI somehow patched it
- but yeah. there's no error. it's a bug with get_urls() where it freezes on that function 
d
- No error, just when I do .run() I get this "INFO:root:[20/10/2023 21:26:56] Bing Image Creator (Dalle-3) Opened
INFO:root:[20/10/2023 21:26:58] Cookie values added " and then nothing else 
- where is the log saved?
- Idk wym by paste error log cause there’s no error it just gets stuck on get_urls()
- feedback, censorship detection, 
oh it suddenly started working for me
maybe it's because I didn't have undetected_chromedriver installed
but I installed it to try the other github?
- parse token usage and print and notify user if there are none left
- and if it's censored does it at least throw an error wait error around 10 seconds, it would be, perhaps we could do time timeout where it just stops everything, I think better would be to also have a loop that checks for the words "unsafe content detected" or whatever the message is
- @Kye does it tell you when the cookie expires?
- Can't we add something like before generation add you own link or something to generate?
- Make the retreival better, parse only the 4 images for the request
- parse when cookie expires somehow, set a day maybe
- that makes the need for it to say censored instead of getting stuck in a loop more prevalent
so you can properly schedule it
otherwise if it gets stuck in a loop there's no way to tell the difference programmatically if another request is still generating or it got censored
!generate photorealistic 3D render of batman made out of legos