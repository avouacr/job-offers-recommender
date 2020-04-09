"""Extract text from a CV, preprocess it and compute its vector representation."""

import os
import io

import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
import unidecode
import spacy
import fr_core_news_md


def cv_to_text(cv_path):
    """
    Extract raw text from a (pdf) resume.

    Sources :
    https://dzone.com/articles/exporting-data-from-pdfs-with-python
    https://gist.github.com/terencezl/61fe3f28c44a763dd1e9f060b8ff6f2e
    https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
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


def extract_experience(cv_text):

    cv_text = unidecode.unidecode(cv_text)
    cv_spacy = nlp(cv_text)

    tokens = []
    for token in cv_spacy:
        if (token.is_stop or token.is_digit or token.is_punct
                or token.is_space or token.ent_type
                or not token.is_alpha):
            # Remove irrelevant tokens
            continue
        else:
            # Lemmatize relevant tokens
            tokens.append(token.lemma_)

    return tokens




# if __name__ == '__main__':

# Test
CV_NAME = 'romain'
CV_DIR = 'cv_tests'
CV_PATH = os.path.join(CV_DIR, CV_NAME) + '.pdf'

cv_text = cv_to_text(CV_PATH)

nlp = fr_core_news_md.load()
cv_spacy = nlp(cv_raw_text)

list(cv_spacy.sents)
