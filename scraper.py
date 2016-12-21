"""
scrap blogs from the web and save them
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


def getLinks(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return "error occured"
    else:
        newObj = BeautifulSoup(html, "html.parser")
        if newObj is not None:
            links = []
            for link in newObj.findAll("a"):
                links.append(link)
                return links
        else:
            return "error occured"


def getExtLinks(bsObj, excludeURL):
    externalLinks = set()
    for link in bsObj.findAll(
            "a", href=re.compile("^(http|www)((?!" + excludeURL + ").)*$")):
        if link.attrs['href'] not in externalLinks:
            externalLinks.add(link.attrs['href'])
    return externalLinks
