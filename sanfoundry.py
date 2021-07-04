import os

import pdfkit
import requests
from PyPDF2 import PdfFileMerger, PdfFileReader
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from utils.sanCleaner import Cleaner
from utils.sanUrls import Urls


def check_dir():
    if not os.path.exists('SanfoundryFiles'):
        os.makedirs('SanfoundryFiles')


class Sanfoundry(object):

    def __init__(self):
        self.mode = int(input(
            "\nEnter 0 to download 'Single MCQ Page' \n\nEnter 1 to download 'MCQ Sets' \n\nEnter 2 to merge existing "
            "pdfs \n\nNOTE: By default selecting the option '1' will merge and delete "
            "all the existing pdfs in SanfoundryFiles/ : "))
        self.pdf_options = {
            'quiet': '',
            'encoding': 'utf-8',
        }
        self.sf_path = "SanfoundryFiles/"

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
        urlList = Urls().getUrls()

        for i in tqdm(range(0, len(urlList)), desc="Saving MCQs"):
            self.url = urlList[i]
            self.scrape()

    def scrape(self):
        with requests.Session() as s:
            r = s.get(self.url)
            soup = bs(r.content, "html5lib")
            div = soup.find("div", {"class": "entry-content"})
            html = Cleaner().clean(div)
            filename = self.url.split("/")[3]
            check_dir()
            pdfkit.from_string(html, f"{self.sf_path}{filename}.pdf", options=self.pdf_options)

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
        pdf_files = os.listdir(self.sf_path)

        if not pdf_files:
            print("No PDF Files Found.")
            exit()

        merger = PdfFileMerger()

        for pdf_file in pdf_files:
            with open(self.sf_path + pdf_file, "rb") as pdf:
                merger.append(PdfFileReader(pdf), import_bookmarks=False)
                pdf.close()

        with open("final_merge.pdf", "wb") as fout:
            merger.write(fout)

    def delete_pdf_parts(self):
        files_to_delete = os.listdir(self.sf_path)

        for file_name in files_to_delete:
            os.remove(os.path.join(self.sf_path, file_name))


if __name__ == '__main__':
    Sanfoundry()
