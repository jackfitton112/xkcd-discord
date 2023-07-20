# XKCD Discord
![Python Version](https://img.shields.io/badge/python-3.8.10%2B-blue.svg)
![License](https://img.shields.io/github/license/jackfitton112/xkcd-discord?color=orange)
![Issues](https://img.shields.io/github/issues/jackfitton112/xkcd-discord)
![Pull Requests](https://img.shields.io/github/issues-pr/jackfitton112/xkcd-discord)

A Discord bot that sends XKCD comics to a channel.

Add the bot to your server [ADD TO DISCORD](https://discord.com/api/oauth2/authorize?client_id=1128423843460026409&permissions=3072&redirect_uri=https%3A%2F%2Ft2k.group&response_type=code&scope=bot%20messages.read).

## Installation - Self Hosting
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

the base command is `!xkcd` and can be used in the following ways:

- `!xkcd help` - Shows the help message
- `!xkcd latest` - Sends the latest XKCD comic
- `!xkcd random` - Sends a random XKCD comic
- `!xkcd <comic number>` - Sends the XKCD comic with the given number
- `!xkcd search <search term>` - searches for an XKCD comic with the given search term
- `!xkcd explain <comic number>` - Sends the explain xkcd page for the given comic number


TODO: (Feek free to make a pull request to add any of these features)

- [ ] change to slash commands [Difficult as needs rework of code]
- [ ] add notes about interactive comics  [https://www.explainxkcd.com/wiki/index.php/Category:Interactive_comics]
- [ ] make scraping more efficient [async threading etc]
- [ ] add more search options
- [ ] add more explain xkcd options
- [ ] add more error handling

