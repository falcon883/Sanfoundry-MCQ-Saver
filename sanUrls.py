from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import requests
import re

class UrlsClass(object):

    def __init__(self):
        self.url = input("\nEnter Sanfoundry Mcq Url where all sections are listed: ")
        self.urlList = list()

    def getUrls(self):
        r = requests.get(self.url)
        urls = bs(r.content, "html5lib")
        urls = urls.find("div", {"class":"inside-article"})
        urls = urls.find_all("a")
        print("\n")
        for i in tqdm(range(0, len(urls)), desc ="Getting MCQ Urls"):
            if re.match("https://www.sanfoundry.com/best-reference-books.*", urls[i]['href']) is None:
                self.urlList.append(urls[i]['href'])
        return self.urlList