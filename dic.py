from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

def wotd():
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
    fnl = "*" + wotd + "* \n" + pos +  " \n**" + definition + "**"
    print(fnl)
    return(fnl)
