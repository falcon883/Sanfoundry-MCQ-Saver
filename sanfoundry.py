import os
import re

import pdfkit
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from PyPDF2 import PdfFileMerger

from sanUrls import UrlsClass


def check_dir():
    if not os.path.exists('SanfoundryFiles'):
        os.makedirs('SanfoundryFiles')


class Sanfoundry(object):

    def __init__(self):
        self.mode = int(input("\nEnter 0 to download 'Single MCQ Page' \n\nEnter 1 to download 'MCQ Sets' \n\nEnter 2 to merge existing pdfs \n\nNOTE: By default selecting option 1 will merge all pdf for you and delete existing pdfs in SanfoundryFiles/ : "))
        self.extract_line = r"<p>\s*<strong>.*</strong>.*</p>"
        self.classes = lambda x: x and x.startswith(
            ('mobile-content', 'desktop-content', 'sf-nav-bottom', 'sf-mobile-ads', 'sf-video-yt'))
        self.pdf_options = {
            'quiet': '',
            'encoding': 'utf-8',
        }
        
        if self.mode == 1:
            self.auto()
            self.merge_all_pdf()
            self.delete_pdf_parts()

        elif self.mode == 2:
            self.merge_all_pdf()
      
        else:
            self.url = input("\nEnter Sanfoundry MCQ URL: ")
            self.scrape()

    def auto(self):
        urlList = UrlsClass().getUrls()
        print("\n")
        for i in tqdm(range(0, len(urlList)), desc="Saving MCQs"):
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
                str(html), "SanfoundryFiles/"+filename+".pdf", options=self.pdf_options)

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
    
    def merge_all_pdf(self): 
        path = 'SanfoundryFiles/'
        file_names = os.listdir(path)

        merger = PdfFileMerger()
        
        for names in file_names:
            merger.append(open(path+names,'rb'))
        
        with open("final_merge.pdf","wb") as fout:
            merger.write(fout)
    
    def delete_pdf_parts(self):
        path = 'SanfoundryFiles/' 
        files_to_delete = os.listdir(path)

        for file_name in files_to_delete:
            os.remove(os.path.join(path,file_name))


if __name__ == '__main__':
    Sanfoundry()