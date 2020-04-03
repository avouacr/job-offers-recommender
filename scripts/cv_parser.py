
import os
import io

import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
import spacy
import fr_core_news_md


nlp = fr_core_news_md.load()


def cv_to_text(cv_path):
    """
    Extract raw text from a (pdf) resume.

    Sources :
    https://dzone.com/articles/exporting-data-from-pdfs-with-python
    https://gist.github.com/terencezl/61fe3f28c44a763dd1e9f060b8ff6f2e
    https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/

    Parameters
    ----------
    cv_path (str): Path of the resume as a pdf file.

    Returns
    -------
    str: Raw text from the resume.

    """
    assert os.path.splitext(cv_path)[-1] == '.pdf', 'The resume should be a pdf file.'

    # Perform layout analysis for all text
    laparams = pdfminer.layout.LAParams()
    setattr(laparams, 'all_texts', True)

    resource_manager = PDFResourceManager()
    retstr = io.StringIO()
    txt_converter = TextConverter(resource_manager, retstr, laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, txt_converter)

    with open(cv_path, "rb") as fp:
        for page in PDFPage.get_pages(fp, check_extractable=True, caching=True):
            # Extract text from each page of the CV
            page_interpreter.process_page(page)
            text = retstr.getvalue()
            # Close open handles
            txt_converter.close()
            retstr.close()

    if text:
        return text


def TextPreprocessor():

    def __init__(self, cv_text):
        self.cv_text = cv_text
        self.doc = nlp(cv_text)

    def remove_named_entities(self):






CV_NAME = 'romain'
CV_DIR = 'cv_tests'
CV_PATH = os.path.join(CV_DIR, CV_NAME) + '.pdf'

cv_text = cv_to_text(CV_PATH)



doc = nlp(cv_text)
for ent in doc.ents:




