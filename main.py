import discord
import asyncio
from random import randint
from dotenv import load_dotenv
import os
import api


load_dotenv()


# Discord Config - Set intents to true to get the message content
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Set rich presence
activity = discord.Activity(name='# !xkcd <post> or just !xkcd', type=discord.ActivityType.playing)

# Get the token from the .env file
TOKEN = os.getenv("DISCORD_TOKEN") # Dont forget to add your token to the .env file

# Sends a message to the channel with the help menu
async def help(channel: discord.TextChannel) -> None:

    message = '''
    # XKCD Discord Bot
    ### Commands
    - `!xkcd help` - help menu
    - `!xkcd latest` - Get the latest post
    - `!xkcd search <search term>` - Search for a post (may return multiple posts)
    - `!xkcd <comic number>` - Get the requested comic
    - `!xkcd random` - Get a random comic
    - `!xkcd explain <comic number>` - Get the explanation for the requested comic
    '''

    await channel.send(message)

# Sends a message to the channel with the error message
async def error(channel: discord.TextChannel, error) -> None:

    #list of funny error messages
    error_messages = [
    "Oops, looks like the hamsters powering this bot took a coffee break! 🐹💤 Please stand by for their return.",
    "Error 404: Witty Comment Not Found. The developers are working on their jokes. Please try again later.",
    "It's not you, it's the bot! We've sent it to the laughter therapy clinic. It should be back soon!",
    "Error: Bot.exe has encountered a problem and needs more coffee to recover ☕. Please be patient.",
    "Roses are red, violets are blue, the bot crashed and so did our humor too!",
    "Looks like the bot's circuits got tangled up in a dance-off! 🕺💃 We're rebooting the disco lights now.",
    "Oh no! The bot ate too many cookies 🍪 and got stuck in a sugar coma. We're feeding it veggies to wake it up.",
    "Error: This bot is experiencing an identity crisis and thinks it's a penguin. 🐧 Please remind it that it's a Discord bot.",
    "404 Error: Humor.exe not found. We've dispatched our top comedians to fix it.",
    "The bot attempted to speak cat but accidentally triggered a system failure. We're decoding the feline language to fix it."
    ]

    await channel.send(error_messages[randint(0, len(error_messages) - 1)])

    #log the error
    print(error)

# Sends a message to the channel with the comic not found message 
async def commic_out_of_range(channel: discord.TextChannel) -> None:

    comic_not_found_messages = [
    "Comic Not Found: Looks like the comic went on a secret mission with the CIA.",
    "Comic Not Found: The comic escaped to join a stand-up comedy tour. It's cracking up audiences!",
    "Comic Not Found: This comic got tangled in a spaghetti code. We're debugging it now.",
    "Comic Not Found: The comic is off exploring the infinite loops of the universe.",
    "Comic Not Found: Our AI bot read the comic and couldn't stop laughing. It'll be back soon.",
    "Comic Not Found: The comic joined a time-travel adventure. We'll bring it back from the past.",
    "Comic Not Found: The comic took a quantum leap into parallel dimensions. We're chasing after it.",
    "Comic Not Found: The comic is on a journey to find the meaning of life. Deep stuff!",
    "Comic Not Found: We suspect the comic is in a witness protection program. Stay tuned!",
    "Comic Not Found: The comic went on a quest to defeat the Error Dragon. We wish it luck!",
    ]

    await channel.send(comic_not_found_messages[randint(0, len(comic_not_found_messages) - 1)])

#handles the sending and formatting of the post
async def send_post(channel: discord.TextChannel, post: tuple) -> None:

    post_id = post[1]
    title = post[2]
    alt_text = post[3]
    post_url = f"https://xkcd.com/{post_id}/"
    img = post[5]

    embed = discord.Embed(title=f"{post_id}: {title}", url=post_url, description=f"{alt_text}", color=0x00ff00)
    embed.set_author(name="XKCD", url="https://xkcd.com/", icon_url="https://xkcd.com/s/0b7742.png")
    embed.set_image(url=img)
    embed.set_footer(text="XKCD Discord Bot")


    await channel.send(embed=embed)

#handles the sending and formatting of the explination
async def send_explination(channel: discord.TextChannel, post: tuple) -> None:

    try:
        explination = post[6]
    except:
        explination = "No explination found"

    #loop through the explination and send it in chunks of 1999 characters
    for i in range(0, len(explination), 1999):
        await channel.send(explination[i:i+1999])

#debug function to test the api
async def debug(channel: discord.TextChannel) -> None:
    
    #send latest post
    data = api.get_latest_post()
    await channel.send("Latest post:")
    await send_post(channel, data)

    #send random post
    data = api.get_random_post()
    await channel.send("Random post:")
    await send_post(channel, data)

    #send post by id
    data = api.get_post_by_id(1)
    await channel.send("Post by id (1):")
    await send_post(channel, data)

    #explain post by id
    data = api.get_post_by_id(1)
    await channel.send("Explain post by id (1):")
    await send_explination(channel, data)

    #search posts
    data = api.search_posts("twitter bot")
    await channel.send("Search posts (python):")
    for post in data:
        await send_post(channel, post)

    

@client.event
async def on_ready():
    # This is called when the bot has connected to discord
    await client.change_presence(activity=activity) # Set the rich presence
    print(f'{client.user} has connected to Discord!') # Print to the console that the bot has connected - This is for debugging


@client.event
async def on_message(message):

    if message.author == client.user:
        return # Ignore messages from the bot

    #checks if the bot is being called
    if message.content.startswith('!xkcd'):


        #get the command or set it to help if no command is given
        if len(message.content.split()) > 1:
            command = message.content.split()[1]

        else:
            command = "help"

        #DEBUG
        #print(f"User {message.author} sent command: {command}")

        if command == "help":
            await help(message.channel)

        elif command == "latest":
            data = api.get_latest_post() # get the latest post from the api
            await send_post(message.channel, data)

        elif command == "random":
            data = api.get_random_post() # get a random post from the api
            await send_post(message.channel, data)

        elif command == "explain":
            post_id = message.content.split()[2] # get the post id from the message
            data = api.get_post_by_id(post_id)  # get the post from the api
            await send_explination(message.channel, data) # send the explination

        elif command == "debug":
            await debug(message.channel)
            return

        elif command == "search":
            # search term is anything after the command
            search_term = message.content.replace("!xkcd search ", "")
            dataset = api.search_posts(search_term)

            if dataset: # if the search returns results
                await message.reply(f"Found {len(dataset)} results for '{search_term}', would you like to send them? (y/n)") # ask the user if they want to send the results

                def check(m): # check if the message is from the same user and if it is yes or no
                    return m.author == message.author and m.content.lower() in ["y", "yes", "n", "no"]

                try:
                    # wait for a response for 30 seconds
                    msg = await client.wait_for('message', check=check, timeout=30)

                    # if the user says yes send the posts, else cancel the search
                    if msg.content.lower() in ["y", "yes"]:
                        for data in dataset:
                            post = api.get_post_by_id(data[0])
                            await send_post(message.channel, post)
                    else:
                        await message.reply("Search cancelled")

                #add a catch for timeout
                except asyncio.TimeoutError:
                    await message.reply("Search timed out. Try again if you want to proceed.")

            else:
                # if the search returns no results, send a message to the channel
                await commic_out_of_range(message.channel)
    

        elif command.isdigit(): # if the command is a number, get the post by id
            data = api.get_post_by_id(command)
            if data: # if the post exists, send it
                await send_post(message.channel, data)
            else: # if the post does not exist, send a message to the channel
                await commic_out_of_range(message.channel)

        else:
            #if unhandled command, send help            
            await help(message.channel)




# .env returns a string or None if the key is not found
if type(TOKEN) == str:
    client.run(TOKEN)
else:
    #stops the bot if no token is found
    exit("No token found - Please add your token to the .env file")
    

