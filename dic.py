import discord
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

f = open("token", "r")
token = f.readline().strip()

client = discord.Client()

channel = 413883696530325506

def wotd():
    wotd_header = "The word of the day is: \n\n"
    url = "https://www.dictionary.com/e/word-of-the-day/"
    req = Request(url)
    html = urlopen(req).read()
    #print(str(html))
    soup = bs(html, features='html.parser')
    grabfrom = "wotd-item__definition"
    wordtag = "h1"
    block = soup.find(class_=grabfrom)
    wotd = block.h1.get_text()
    pos = block.find(class_="wotd-item__definition__pronunciation").get_text().strip()
    definition = block.find(class_="wotd-item__definition__text").get_text().strip("\"").strip()
    fnl = wotd_header + "**" + wotd + "** \n\n" + pos +  " \n\n*" + definition + "*"
    print(fnl)
    return(fnl)

@client.event
async def on_ready():
    ch = client.get_channel(channel)
    await ch.send(wotd())

client.run(token)
