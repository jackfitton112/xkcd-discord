import sqlite3
import requests
import asyncio
import queue
import xml.etree.ElementTree as ET
from alive_progress import alive_bar
import random
import mwparserfromhell
import time
import threading

processing_queue = queue.Queue()

# initalise the database and create a table (if it doesn't exist)
def init_database():

    # connect to database
    conn = sqlite3.connect('xkcd.db')

    # create cursor
    c = conn.cursor()

    # create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS xkcd (
        id integer PRIMARY KEY,
        post_id integer,
        post_title text,
        post_alt text,
        post_url text,
        post_img text,
        explination text)
        ''')
    
    # commit changes
    conn.commit()

    # close connection
    conn.close()
    
# SETTERS

# add a new post to the database
# post_id: the id of the post
# post_title: the title of the post
# post_alt: the alt text of the post
# post_url: the url of the post
# post_img: the image url of the post
# exp: the explination of the post
# returns: True if successful, False if not      
def add_post(post_id: int, post_title: str, post_alt: str, post_url: str, post_img: str, exp: str, conn = None) -> bool:

    close_conn = False

    if conn is None: # This is to lower the amount of connections to the database
        # connect to database
        conn = sqlite3.connect('xkcd.db')
        close_conn = True
        # create cursor
    c = conn.cursor()

    # insert data
    try:
        c.execute("INSERT INTO xkcd VALUES (:id, :post_id, :post_title, :post_alt, :post_url, :post_img, :explination)",
                {
                    'id': None,
                    'post_id': post_id,
                    'post_title': post_title,
                    'post_alt': post_alt,
                    'post_url': post_url,
                    'post_img': post_img,
                    'explination': exp

                }
            )

        # commit changes
        conn.commit()
    
    except sqlite3.IntegrityError:
        print(f"Post {post_id} already exists in database")
        return False
    
    if close_conn:
        # close connection
        conn.close()

    return True    

def add_posts(posts: list) -> bool:

    for post in posts:

        if not add_post(post[0], post[1], post[2], post[3], post[4], post[5]):
            return False


    return True

def latest_stored_post_id() -> int:
    
        # connect to database
        conn = sqlite3.connect('xkcd.db')
    
        # create cursor
        c = conn.cursor()
    
        # get data
        c.execute("SELECT post_id FROM xkcd ORDER BY post_id DESC LIMIT 1")
    
        # fetch data
        post = c.fetchone()
    
        # close connection
        conn.close()
    
        if post is None:
            return 0
        else:
            return post[0]

async def get_page_count() -> int:
    rss_url = "https://xkcd.com/rss.xml"

    # Get the RSS feed
    rss = requests.get(rss_url).text

    root = ET.fromstring(rss)

    # Find the 'guid' element under the first 'item' element of the 'channel'
    guid_element = root.find('.//channel/item[1]/guid')

    if guid_element is not None:
        # The 'guid' element usually contains the link in the format "https://xkcd.com/{page_number}/"
        # Extract the page number from the 'guid'
        guid_text = guid_element.text

        if guid_text is not None:
            page_number = int(guid_text.strip('/').split('/')[-1])
            return page_number

    # If the 'guid' element is not found or parsing fails, return 0 as the default value
    return 0

async def scrape_xkcd():

    def scrape_post(post_id):

        url = f"https://xkcd.com/{post_id}/info.0.json"

        # get data
        response = requests.get(url)

        # check if response is valid
        if response.status_code != 200:
            return False
        
        # get json
        post = response.json()

        id = post['num']
        title = post['title']
        alt = post['alt']
        url = f"https://xkcd.com/{post_id}/"
        img = post['img']

        #replace spaces with underscores
        exp_title = title.replace(" ", "_")
        exp_url = f"https://www.explainxkcd.com/wiki/api.php?action=parse&page={id}:_{exp_title}&prop=wikitext&sectiontitle=Explanation&format=json"

        # get data
        response = requests.get(exp_url)

        # check if response is valid
        if response.status_code != 200:
            return [id, title, alt, url, img, ""]
        
        # get json
        try:
            exp = response.json()

            wiki_text = exp['parse']['wikitext']['*']


            # Parse the wikitext using mwparserfromhell
            wikicode = mwparserfromhell.parse(wiki_text)

            # Find the section by heading title
            explanation_section = None

            for section in wikicode.get_sections(include_lead=True, include_headings=True):
                if section.strip_code().strip().startswith("Explanation"):
                    explanation_section = section
                    break

            if explanation_section:
                exp = explanation_section.strip_code().strip()

            else:
                exp = "No explanation found"

        except:
            exp = "No explanation found"


        #return [id, title, alt, url, img, exp]
        processing_queue.put_nowait([id, title, alt, url, img, exp])

  # connect to database
    conn = sqlite3.connect('xkcd.db')

    latest_xkcd = await get_page_count()

    latest_db = latest_stored_post_id()

    if latest_xkcd > latest_db:
        
        with alive_bar(latest_xkcd - latest_db + 1) as bar:
            for i in range(latest_db + 1, latest_xkcd):

                # add scrape to queue
                #post = await scrape_post(i)
                #if post:
                #    add_post(post[0], post[1], post[2], post[3], post[4], post[5], conn)
                #else:
                #   print(f"Failed to scrape post {i}")

                #start a thread to scrape the post
                thread = threading.Thread(target=scrape_post, args=(i,)).start()

                bar()

            # go through the queue and add the posts to the database
            with alive_bar(processing_queue.qsize()) as bar:
                time.sleep(5)
                while not processing_queue.empty():
                    post = processing_queue.get_nowait()
                    add_post(post[0], post[1], post[2], post[3], post[4], post[5], conn)
                    bar()

        conn.close()


# GETTERS
def get_post_by_id(post_id: int) -> tuple:

    # connect to database
    conn = sqlite3.connect('xkcd.db')

    # create cursor
    c = conn.cursor()

    # get data
    c.execute("SELECT * FROM xkcd WHERE post_id=:post_id", {'post_id': post_id})

    # fetch data
    post = c.fetchone()

    # close connection
    conn.close()

    return post # (id, post_id, post_title, post_alt, post_url, post_img)

def search_posts(search_term: str) -> list: # returns a list of tuples (id, post_id, post_title, post_alt, post_url, post_img)

    # connect to database
    conn = sqlite3.connect('xkcd.db')

    # create cursor
    c = conn.cursor()

    # get data
    c.execute("SELECT post_id FROM xkcd WHERE post_title LIKE :search_term OR post_alt LIKE :search_term", {'search_term': f"%{search_term}%"})

    # fetch data
    posts = c.fetchall()

    # close connection
    conn.close()

    return posts

def get_random_post() -> tuple:

    max_id = latest_stored_post_id()

    random_id = random.randint(1, max_id)

    return get_post_by_id(random_id)

def get_latest_post() -> tuple:
    
        max_id = latest_stored_post_id()
    
        return get_post_by_id(max_id)






async def main ():

    init_database()

    await scrape_xkcd()

    


def apiInit():
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())

