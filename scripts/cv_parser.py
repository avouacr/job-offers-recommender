"""Extract text from a CV, preprocess it and compute its vector representation."""

import os
import io
from multiprocessing import Pool, cpu_count
import urllib.request

import numpy as np
import unidecode
import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
import spacy
import fr_core_news_md
import fasttext.util


N_CORES = cpu_count()
nlp = fr_core_news_md.load()


def import_stopwords():
    """Download and import French stopwords."""
    URL = 'https://raw.githubusercontent.com/stopwords-iso/stopwords-fr/master/stopwords-fr.txt'
    response = urllib.request.urlopen(URL)
    stopwords = response.read().decode('utf-8').splitlines()
    stopwords = [unidecode.unidecode(x) for x in stopwords]
    return stopwords


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


def preprocess_cv_text(spacy_doc):

    tokens = []

    for token in spacy_doc:
        if (token.is_stop or token.is_digit or token.is_punct
                or token.is_space or token.ent_type
                or not token.is_alpha):
            continue
        else:
            token = str(token)
            token = token.lower()
            token = unidecode.unidecode(token)
            tokens.append(token)

    return tokens


def import_fasttext(path_bin=None):
    """Download and import FastText pre-trained word vectors."""
    if path_bin is not None:
        ft = fasttext.load_model(path_bin)
    else:
        print('The binary of FastText French model was not provided.',
              'Will download, uncompress and load it. This takes a long time.')
        fasttext.util.download_model('fr', if_exists='ignore')
        ft = fasttext.load_model('cc.fr.300.bin')

    return ft


def fasttext_wv_avg(tokens, fasttext_model):
    """Compute average of FastText's word vectors over a sequence of tokens.."""
    WV_SIZE = fasttext_model.get_dimension()

    wv_tokens = []
    for i, tok in enumerate(tokens):
        try:
            wv_tokens.append(fasttext_model.get_word_vector(tok))
        except KeyError:
            pass

    wv_mat = np.array(wv_tokens)
    text_vec = wv_mat.mean(axis=0)
    return text_vec


CV_NAME = 'romain'
CV_DIR = 'cv_tests'
CV_PATH = os.path.join(CV_DIR, CV_NAME) + '.pdf'

cv_raw_text = cv_to_text(CV_PATH)
spacy_doc = nlp(cv_raw_text)
tokens = preprocess_cv_text(spacy_doc)

fasttext_model = import_fasttext('models/cc.fr.300.bin')
cv_vector = fasttext_wv_avg(tokens, fasttext_model)
