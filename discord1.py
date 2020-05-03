import discord
import random
import asyncio
import aiohttp
import json
from discord.ext.commands import Bot
import youtube_dl
import requests
from lxml import html

BOT_PREFIX = ("?", "!")
TOKEN = 'NzA1Nzg5OTc2Mzk0MzM0MzI0.Xq7PVQ.jAHGgQ18AYH73IqB6W-8rJFzsHM'

players = {}

# client = discord.Client()

# bot = commands.Bot(command_prefix='$', description='A bot that greets the user back.')
client = Bot(command_prefix=BOT_PREFIX)


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)






# v = discord.VoiceChannel()









class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)




# def is_connected(ctx):
#     # voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
#     return voice_client and voice_client.is_connected()


@client.command(pass_context=True)
async def join(ctx):
    print(ctx, 'joinig')
    print(dir(ctx.message.author.voice))
    channel = ctx.message.author.voice.channel
    # await ctx.send(":smiley: :wave: Hello, there!")
    print(dir(client))
    # await client.connect(channel)
    print(type(discord.VoiceChannel.connect(channel)))
    vc = await  discord.VoiceChannel.connect(channel)




def get_url(query):
    
    print('*******************runnin url scrape\n', )
    url = f"https://www.youtube.com/results?search_query={query}"
    r = requests.get(url , timeout = 100)
    tree = html.fromstring(r.text)
    url = tree.xpath('//div[@class="yt-lockup-content"][1]//a/@href')
    print(url[0])
    u = "https://www.youtube.com" + url[0]
    
    return u


@client.command(pass_context=True)
async def play(ctx, *, query=None):
    url = get_url(query)
    print(dir(ctx))
    # print(dir(ctx.message))
    # print(get())
    print(dir(ctx.bot))
    # print(is_connected(ctx))
    print('\n\n\n\n\n\n\+++++++++++++\n', dir(client))
    print(ctx.bot.voice_clients)
    print(ctx.voice_client)
    server = ctx.message.guild
    # print('\n\n\n\n', dir(client))
    # print(client.voice_clients)
    # voice_cient = client.voice_clients(server)
    # player = await voice_cient.create_ytdl_player(url)
    # server[server.id] = player
    # player.start()
    # channel = ctx.message.author.voicevoice_channel
    # # await ctx.send(":smiley: :wave: Hello, there!")
    # await client.join_voice_channel(channel)

    player = await YTDLSource.from_url(url)
    # if not ctx.bot.voice_clients:
    # channel = ctx.message.author.voice.channel
    # if not discord.VoiceChannel.connect(channel).is_connected():
    # vc = await  discord.VoiceChannel.connect(channel)
    print('&&&&&&&&&&&&&&&&&&&&\n', ctx.bot.voice_clients)
    # print('\n\n\n\n', dir(vc))
    # vc.play(discord.FFmpegPCMAudio(url), after=lambda e: print('done', e))
    ctx.bot.voice_clients[0].play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('Now playing: {}'.format(player.title))
    
    

@client.command(pass_context=True)
async def stop(ctx,):
    print(dir(ctx.bot.voice_clients[0]))
    ctx.bot.voice_clients[0].stop()

    # await ctx.send('Stopped:')    
    
@client.command(pass_context=True)
async def pause(ctx,):
    print(dir(ctx.bot.voice_clients[0]))
    ctx.bot.voice_clients[0].pause()
    
@client.command(pass_context=True)
async def resume(ctx,):
    print(dir(ctx.bot.voice_clients[0]))
    ctx.bot.voice_clients[0].resume()  
    
    
    
@client.command(pass_context=True)
async def time(ctx, loc=None):
    url = f"https://www.timeanddate.com/worldclock/{loc}"    
    r = requests.get(url , timeout = 100)
    tree = html.fromstring(r.text)
    url = tree.xpath('//div/span[@id="ct"]/text()')
    print(url[0])  
    await ctx.send(f"time at {loc} is : {url[0]}")  
    
    
    
    
    
# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')
        
        
@client.command()
async def stream(self, ctx, *, url=None):
    """Streams from a url (same as yt, but doesn't predownload)"""
    print('herer')
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))






# @client.command(pass_context=True)
# async def stop(ctx, url):
#     print('stopping', ctx)
#     id = ctx.message.server.id
#     players[id].stop()

@client.command()
async def hello(ctx):
    print(ctx)
    await ctx.send(":smiley: :wave: Hello, there!")


@client.command()
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


@client.command()
async def square(ctx, number):
    print(number)
    squared_value = int(number) * int(number)
    await ctx.send(str(number) + " squared is " + str(squared_value))


# @client.event
# async def on_message(message):
#     # we do not want the bot to reply to itself
#     if message.author == client.user:
#         return

#     if message.content.startswith('!hello'):
#         msg = 'Hello {0.author.mention}'.format(message)
#         await client.send_message(message.channel, msg)

@client.event
# @bot.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)