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
   git clone https://github.com/YOUR_REPOSITORY_URL.git
   cd YOUR_REPOSITORY_NAME
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
   discord.py
   requests
   undetected-chromedriver
   selenium
   ```

## Configuration

1. **Token & Cookie Configuration**:
   
   Open the bot script in a text editor and replace `'YOUR_DISCORD_BOT_TOKEN'` with your actual Discord bot token and `'YOUR_COOKIE_VALUE'` with the cookie value from the DALL-E 3 Unofficial API.

2. **Permissions**:

   Make sure your bot has the following permissions in Discord:

   - Read Messages
   - Send Messages
   - Attach Files
   - Manage Messages

## Running the Bot

With everything set up, you can now run the bot:

```bash
python bot_script_name.py
```

Replace `bot_script_name.py` with the actual name of your bot script.

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

## Conclusion

You now have a Discord bot capable of generating images using DALL-E. Enjoy and be creative with your prompts!