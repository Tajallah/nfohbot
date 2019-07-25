import discord

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as beausu
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

f = open("token", "r")
token = f.readline().strip()

client = discord.Client()

urls = [
        "https://www.morningbrew.com/latest",
        "https://www.morningbrew.com/latest/emerging-tech/",
        "https://www.morningbrew.com/latest/retail/"
        ]

channels = [
        "415146126501740544",#Headlines
        "571144217498353664", #tech
        "415139683346153472" #biz
        ]

def prune(text, blacklist, hardlist):
    result = text
    #print(text)
    if result == None:
        return None
    if len(result) < 3:
        result = None
    for word in blacklist:
        if word in text:
            result = None
    for word in hardlist:
        if word == text:
            result = None
    if result == '':
        result = None
    #print(result)
    return result

def get_stuff(soup, blacklist, hardlist, stocks):
    i = 0
    holding = ""
    paragraphs = []
    start_flag = True
    for paragraph in soup.find_all('p'):
        #print(paragraphs)
        #print(paragraph.get_text())
        p = paragraph.get_text().strip('\n').strip('\xa0').replace(u'\xa0', u'').replace(u'\n', u'').replace('  ', '')
        #print(p)
        p = prune(p, blacklist, hardlist)
        if p != None:
            if p not in stocks and i == 0:
                if start_flag == True:
                    paragraphs.append(p)
            else:
                start_flag = True
                holding = holding + " " +  p
                i += 1
                if i == 3:
                    if p[0] == '-':
                        holding = ':chart_with_downward_trend: ' + holding
                        paragraphs.append(holding)
                        holding = ""
                        i = 0
                    else:
                        holding = ':chart_with_upward_trend: ' + holding
                        paragraphs.append(holding)
                        holding = ""
                        i = 0
    links = []
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            if 'http' in link['href']:
                h = link['href']
                h = prune(h, blacklist, hardlist)
                if h != None:
                    links.append(h)
    print(paragraphs)
    print(links)
    return [paragraphs, links]

def doall():
    final = []
    for i in range(3):
        req = Request(urls[i], headers={"User-Agent": "Mozilla/5.0"})
        html = urlopen(req, context=ctx).read()
        soup = beausu(html, features="html.parser")
    
        blacklist = ['morningbrew', 'Morning Brew', 'sponsor', 'Sponsor', 'xa0', 'MorningBrew', 'the Brew']
        hardlist = ['Latest', 'SPONSORED BY', 'twitter.']
    
        stocks = ['S&P', 'NASDAQ', 'DJIA', '10-YR', 'GOLD', 'OIL']
    
        final.append([get_stuff(soup, blacklist, hardlist, urls[i]), channels[i]])
    return final

def get_channel(chan):
    ch = client.get_channel(int(chan))
    return ch

#so... this function is kind of a shitstorm, it basically unwraps a single datastructure that's a set of nested lists that contan the channel information and text from the scraped news.
@client.event
async def on_ready():
    print("START")
    stuff = doall() #the structure of stuff is [ [[text, links], channel], ...]
    for i in stuff:
        ch = get_channel(i[1])
        for section in i[0]:
            for line in section:
                await ch.send(line)
    print("DONE")

client.run(token)
