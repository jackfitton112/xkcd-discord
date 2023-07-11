# XKCD Discord
![Python Version](https://img.shields.io/badge/python-3.8.10%2B-blue.svg)
![License](https://img.shields.io/github/license/jackfitton112/xkcd-discord?color=orange)
![Issues](https://img.shields.io/github/issues/jackfitton112/xkcd-discord)
![Pull Requests](https://img.shields.io/github/issues-pr/jackfitton112/xkcd-discord)

A Discord bot that sends XKCD comics to a channel.

## Installation
1. Clone the repository
2. Install the requirements 

```bash
git clone https://github.com/jackfitton112/xkcd-discord.git;
cd xkcd-discord;
```
    
3. Create a `.env` file in the root directory
4. Add the following to the `.env` file

```bash
DISCORD_TOKEN=<your token here>
```

5. Run the bot

```bash
python3 main.py
```

Thats it! The bot should now be running.

## Usage

`!xkcd` - Sends a random XKCD comic to the channel.

`!xkcd <comic number>` - Sends a specific XKCD comic to the channel.

`!xkcd latest` - Sends the latest XKCD comic to the channel.

`!xkcd help` - Sends a help message to the channel.



