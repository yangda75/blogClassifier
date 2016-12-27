"""
scrap blogs from the web and save them
"""

# from urllib.request import urlopen
# from urllib.error import HTTPError
import time
import requests
from bs4 import BeautifulSoup

# def getLinks(url):
#     try:
#         html = urlopen(url)
#     except HTTPError as e:
#         print(e)
#         return "error occured"
#     else:
#         newObj = BeautifulSoup(html, "html.parser")
#         if newObj is not None:
#             links = []
#             for link in newObj.findAll("a"):
#                 links.append(link)
#                 return links
#         else:
#             return "error occured"

# def getExtLinks(bsObj, excludeURL):
#     externalLinks = set()
#     for link in bsObj.findAll(
#             "a", href=re.compile("^(http|www)((?!" + excludeURL + ").)*$")):
#         if link.attrs['href'] not in externalLinks:
#             externalLinks.add(link.attrs['href'])
#     return externalLinks


def get_rec10(username):
    """
    accepts a username and returns ten recent articles of that user in the
    form of BeautifulSoup objects
    """
    url = "https://medium.com/@" + username + "/latest"
    user_page = requests.get(url)
    soup = BeautifulSoup(user_page, "html5lib")
    articles = []
    for div in soup.find_all('div', {'class', 'layoutSingleColumn'}):
        link = div.find('a')['href']
        time.sleep(10)  #sleep for a while to avoid being banned
        articles.append(BeautifulSoup(requests.get(link), "html5lib"))
    return articles
