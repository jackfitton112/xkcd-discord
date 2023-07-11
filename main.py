import discord
from bs4 import BeautifulSoup
import aiohttp, asyncio
from lxml import etree
from random import randint
from dotenv import load_dotenv
import os

load_dotenv()


# Discord Config - Set intents to true to get the message content
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Set rich presence
activity = discord.Activity(name='# !xkcd <post> or just !xkcd', type=discord.ActivityType.playing)

# Get the token from the .env file
TOKEN = os.getenv("DISCORD_TOKEN") # Dont forget to add your token to the .env file

async def get_num_of_posts() -> int:

    # Base URL goes to the latest post
    url = "https://xkcd.com/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            dom = etree.HTML(text=str(soup), parser=None)
            # Get the number of posts
            # The number of posts is the number in the URL
            # that is displayed on the page
            # /html/body/div[2]/a[1]

            # Get the number of posts
    new_post_url = dom.xpath("/html/body/div[2]/a[1]")[0].attrib["href"] #Xpath to the first link

    #split at the /
    new_post_url = new_post_url.split("/")

    # Get the last element
    return int(new_post_url[-1]) # Get the last element of the list

async def pick_random_post() -> int:
    max_posts = await get_num_of_posts() # Get the max number of posts from the site

    return randint(1, max_posts) # Pick a random number between 1 and the max number of posts

async def get_post_info(post_number: int) -> list:

    max_posts = await get_num_of_posts()

    #type cast to int as the post number is a string (even though post_number is an int... ty python)
    if int(post_number) > int(max_posts):
        return ["https://imgs.xkcd.com/comics/now.png", "404", "https://xkcd.com/404/"]

    # forms the url for the requested post
    url = f"https://xkcd.com/{post_number}/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            dom = etree.HTML(text=str(soup), parser=None)
            # Get the image URL 
            # /html/body/div[2]/a[2]
            url = dom.xpath("/html/body/div[2]/a[2]")[0].attrib["href"] #This is the image URL
            title = str(dom.xpath("/html/body/div[2]/div[1]")[0].text) # This is the title of the post
            link = "https://xkcd.com/" + str(post_number) # This is the perm link to the post
            return [url, title, link] # Return the list of the image URL, title and link
        

async def help(channel: discord.TextChannel) -> None:

    message = "# XKCD Discord Bot\n\n### Commands\n\n- !xkcd help - help menu\n- !xkcd latest - Get the latest post\n- !xkcd <comic number> - Get the requested comic"

    await channel.send(message)



    

@client.event
async def on_ready():
    # This is called when the bot has connected to discord
    await client.change_presence(activity=activity) # Set the rich presence
    print(f'{client.user} has connected to Discord!') # Print to the console that the bot has connected - This is for debugging


@client.event
async def on_message(message):

    if message.author == client.user:
        return # Ignore messages from the bot

    post = 404 # Set the post to 404; this is for type safety
    if message.content.startswith('!xkcd'):

        #if there is a number after the command
        if len(message.content.split()) > 1:
            # Get the post number
            if type(message.content.split()[1]) == int:
                post = message.content.split()[1] 


            elif message.content.split()[1] == "help":
                await help(channel=message.channel)
                return
        
            elif message.content.split()[1] == "latest":
                post = await get_num_of_posts()




        else:
            # Get a random post
            post = await pick_random_post()

        
        img_url, title, post_url = await get_post_info(post)

        # Create the embed
        embed = discord.Embed(title=title, url=post_url, color=0x00ff00)
        embed.set_image(url=img_url)
        # Send the embed
        await message.channel.send(embed=embed)

# .env returns a string or None if the key is not found
if type(TOKEN) == str:
    client.run(TOKEN)
else:
    exit("No token found - Please add your token to the .env file")
    

