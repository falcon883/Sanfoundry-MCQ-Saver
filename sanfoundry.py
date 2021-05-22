import os
import re

import pdfkit
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from sanUrls import UrlsClass


def check_dir():
    if not os.path.exists('SanfoundryFiles'):
        os.makedirs('SanfoundryFiles')


class Sanfoundry(object):

    def __init__(self):
        self.mode = int(input("\nEnter 0 to download 'Single MCQ Page' and 1 to download 'MCQ Sets': "))
        self.extract_line = r"<p>\s*<strong>.*</strong>.*</p>"
        self.classes = lambda x: x and x.startswith(
            ('mobile-content', 'desktop-content', 'sf-nav-bottom', 'sf-mobile-ads', 'sf-video-yt'))
        self.pdf_options = {
            'quiet': '',
            'encoding': 'utf-8',
        }
        if self.mode == 1:
            self.auto()
        else:
            self.url = input("\nEnter Sanfoundry MCQ URL: ")
            self.scrape()

    def auto(self):
        urlList = UrlsClass().getUrls()
        print("\n")
        for i in tqdm(range(0, len(urlList)), desc="Saving Mcqs"):
            self.url = urlList[i]
            self.scrape()

    def scrape(self):
        with requests.Session() as s:
            r = s.get(self.url)
            soup = bs(r.content, "html5lib")
            div = soup.find("div", {"class": "entry-content"})
            div.attrs = {}
            [tag.extract() for tag in div(['script', 'a'])]
            [tag.extract() for tag in div.find_all(["div"], {"class": self.classes})]
            [tag.extract() for tag in div.find_all("span", {"class": "collapseomatic"})]
            [tag.extract() for tag in div.find_all("div") if tag.text == "advertisment"]
            for tags in div.find_all(True):
                tags.attrs = {}
            data = ' '.join(str(div).split())
            data = re.sub(self.extract_line, "", data)

            filename = self.url.split("/")[3]
            check_dir()
            html = bs(data, "html5lib")
            head = html.head
            head.append(html.new_tag('style', type='text/css'))
            head.style.append('*{font-family: Arial, Helvetica, sans-serif !important;}')
            pdfkit.from_string(
                str(html), f"SanfoundryFiles/{filename}.pdf", options=self.pdf_options)

            if self.mode == 0:
                more = input("Scrape More? (Y/N): ").lower().strip()
                try:
                    if more[0] == 'y':
                        self.url = input("\nEnter Sanfoundry MCQ URL: ")
                        self.scrape()
                    elif more[0] == 'n':
                        exit()
                    else:
                        print('Invalid Input')
                except Exception as error:
                    print("An Error Occured: ")
                    print(error)


if __name__ == '__main__':
    Sanfoundry()
