import wikipedia as w
from wikipedia.exceptions import DisambiguationError, PageError

def lookup(term):
    l = w.search(term, results=10)
    retstring = "Here's what I found for *" + term + "*:\n\n"
    for line in l:
        retstring += "**" + line + "**\n"
    return retstring

def summ(term):
    try:
        s = w.summary(term, chars=1700)
        lnk = w.page(term).url
    except DisambiguationError as e:
        print(e)
        l = e.options
        retstring = "I'm not entirely sure what you mean by that. Here's what I found for **" + term + "**:\n\n"
        for line in l:
            retstring += "**" + line + "**\n"
        return retstring
    except PageError as e:
        print(e)
        return("I don't know what you mean by that...\n\nI didn't find any results for **%s**"%(term))
    retstring = "** " + term + "** \n\n" + s + "\n\n " + lnk
    return retstring

def img(term):
    try:
        img = w.page(term).images[0]
    except PageError as e:
        print(e)
        return("I couldn't find any images for **%s**"%(term))
    return img
