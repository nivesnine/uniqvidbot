# uniqVidBot.py 
import os
import discord

from dotenv import load_dotenv
import re

from urllib.parse import urlparse, parse_qs

def get_video_code(url):
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    # fail?
    return None

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    content = message.content
    search = re.search("(?P<url>https?://[^\s]+)", content)
    if search:
        url = get_video_code(search.group("url"))
        messages = await channel.history(limit=300).flatten()
        count = 0
        for msg in messages:
            if url in msg.content:
                count += 1
        if count > 1:
            await message.delete()
            await message.channel.send(message.author.mention + ' We already saw that one!')

client.run(TOKEN)
