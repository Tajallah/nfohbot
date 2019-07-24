import discord
import dic
#import morningbrew
import wiki
from discord.ext import commands

#bot = commands.Bot(command_prefix='!!')

f = open("token", "r")
token = f.readline().strip()
print("------------------------------------------------------------%s---------------------------------------------------------------"%(token))

client = discord.Client()

@client.event
async def on_ready():
    print("SESSION STARTED -- Logged in as ", client.user)
    news = morningbrew.doall()
    '''for obj in news:
        for line in text:
            await client.send_message( ,obj[1])'''

@client.event
async def on_message(message):
    chn = message.channel
    author = message.author
    content = message.content.strip().lower()
    send = message.channel.send
    print(content)
    if author == client.user:
        return #do nothing
    #WIKIPEDIA FUNCTIONS
    elif content.startswith("what is "):
        term = content[7:].strip()
        await send(wiki.summ(term))
    elif content.startswith("look up "):
        term = content[7:].strip()
        await send(wiki.lookup(term))
    elif content.startswith("image of "):
        term = content[8:].strip()
        await send(wiki.img(term))

client.run(token)
