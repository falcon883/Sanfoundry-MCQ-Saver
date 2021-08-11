import re

import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm


class Urls(object):

    def __init__(self):
        self.url = input("\nEnter Sanfoundry Mcq Url where all sections are listed: ")
        self.urlList = list()
        self.regx_url = re.compile(
            r"^(http://www\.|https://www\.|http://|https://)?[a-z0-9]+([\-.]{1}[a-z0-9]+)*\.[a-z]{2,"
            "5}(:[0-9]{1,5})?(/.*)?$")

    def getUrls(self):
        r = requests.get(self.url)
        urls = bs(r.content, "html5lib")
        urls = urls.find("div", {"class": "inside-article"}).find_all("a", {'href': self.regx_url})
        print("\n")
        for url in tqdm(urls, desc="Getting MCQ Urls"):
            try:
                if re.match("https://www.sanfoundry.com/best-reference-books.*", url['href']) is None:
                    self.urlList.append(url['href'])
            except KeyError:
                pass

        return self.urlList
