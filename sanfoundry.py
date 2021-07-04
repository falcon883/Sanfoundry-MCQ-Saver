import os
from datetime import datetime

import pdfkit
import requests
from PyPDF2 import PdfFileMerger, PdfFileReader
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from utils.sanCleaner import Cleaner
from utils.sanUrls import Urls


def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def confirm_prompt(question: str) -> bool:
    reply = None
    while reply not in ("", "y", "n"):
        reply = input(f"{question} (Y/n): ").lower()
    return reply in ("", "y")


class Sanfoundry(object):

    def __init__(self):
        self.mode = int(input(
            "\nEnter 0 to download 'Single MCQ Page' "
            "\nEnter 1 to download 'MCQ Sets' "
            "\nEnter 2 to merge existing pdfs"
            "\n\nEnter Input (0 - 2): "
        ))
        self.pdf_options = {
            'quiet': '',
            'encoding': 'utf-8',
        }
        self.sf_path = "SanfoundryFiles/"
        self.merged_path = "Merged Pdfs/"

        if self.mode == 1:
            self.auto()
            self.merge_all_pdf()
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
            check_dir(self.sf_path)
            pdfkit.from_string(html, f"{self.sf_path}{filename}.pdf", options=self.pdf_options)

            if self.mode == 0:
                more = confirm_prompt("Scrape More?")
                if more:
                    self.url = input("\nEnter Sanfoundry MCQ URL: ")
                    self.scrape()
                else:
                    exit()

    def merge_all_pdf(self):
        pdf_files = os.listdir(self.sf_path)

        if not pdf_files:
            print("\nNo PDF Files Found.")
            exit()

        delete = confirm_prompt("Delete pdfs after merging?")
        merger = PdfFileMerger()

        for pdf_file in pdf_files:
            with open(self.sf_path + pdf_file, "rb") as pdf:
                merger.append(PdfFileReader(pdf), import_bookmarks=False)
                pdf.close()

        check_dir(self.merged_path)
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        with open(f"{self.merged_path}Sanfoundry_Merged_{current_time}.pdf", "wb") as fout:
            merger.write(fout)

        if delete:
            self.delete_all_pdf()

    def delete_all_pdf(self):
        files_to_delete = os.listdir(self.sf_path)

        for file_name in files_to_delete:
            os.remove(os.path.join(self.sf_path, file_name))


if __name__ == '__main__':
    Sanfoundry()
