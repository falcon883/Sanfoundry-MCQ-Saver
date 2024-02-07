import re

import cloudscraper

from bs4 import BeautifulSoup as bs
from tqdm import tqdm


class Urls(object):

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.url = input("\nEnter Sanfoundry Mcq Url where all sections are listed: ")
        self.urlList = []
        self.regx_url = re.compile(
            r"^(http://www\.|https://www\.|http://|https://)?[a-z0-9]+([\-.]{1}[a-z0-9]+)*\.[a-z]{2,"
            "5}(:[0-9]{1,5})?(/.*)?$")

    def getUrls(self):
        r = self.scraper.get(self.url)
        url_tables = ((bs(r.content, "html5lib")
                       .find("div", {"class": "inside-article"})
                       .find("div", {"class": "entry-content"}))
                      .find_all('table'))

        urls = []
        for t in url_tables:
            urls += t.find_all("a", {'href': self.regx_url})

        print("\n")
        for url in tqdm(urls, desc="Getting MCQ Urls"):
            try:
                if re.match("https://www.sanfoundry.com/(best-reference-books|mcq-pdf-download).*",
                            url['href']) is None:
                    self.urlList.append(url['href'])
            except KeyError:
                pass

        return self.urlList
