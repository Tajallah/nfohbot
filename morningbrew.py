from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as beausu
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
        "https://www.morningbrew.com/latest",
        "https://www.morningbrew.com/latest/emerging-tech/",
        "https://www.morningbrew.com/latest/retail/"
        ]

final = []

def prune(text):
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
    start_flag = False
    for paragraph in soup.find_all('p'):
        #print(paragraph.get_text())
        p = paragraph.get_text().strip('\n').strip('\xa0').replace(u'\xa0', u'').replace(u'\n', u'').replace('  ', '')
        #print(p)
        p = prune(p)
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
                h = prune(h)
                if h != None:
                    links.append(h)

    print(paragraphs)
    print(links)

for url in urls[0:1]:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(req, context=ctx).read()
    soup = beausu(html, features="html.parser")
    
    blacklist = ['morningbrew', 'Morning Brew', 'sponsor', 'Sponsor', 'xa0']
    hardlist = ['Latest', 'SPONSORED BY']
    
    stocks = ['S&P', 'NASDAQ', 'DJIA', '10-YR', 'GOLD', 'OIL']
    
    final.append(get_stuff(soup, blacklist, hardlist, url))

#return final
