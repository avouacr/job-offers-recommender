
import os
from multiprocessing import Pool, cpu_count
import urllib.request

import numpy as np
import unidecode
import spacy
import fr_core_news_md
import fasttext.util

from scripts.cv_parser import cv_to_text


def import_stopwords():
    """Download and import French stopwords."""
    URL = 'https://raw.githubusercontent.com/stopwords-iso/stopwords-fr/master/stopwords-fr.txt'
    response = urllib.request.urlopen(URL)
    stopwords = response.read().decode('utf-8').splitlines()
    stopwords = [unidecode.unidecode(x) for x in stopwords]
    return stopwords


def preprocess_cv_text(text, nlp_model):

    doc = nlp_model(text)

    tokens = []
    for token in doc:
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


fasttext_model = import_fasttext('models/cc.fr.300.bin')
spacy_fr_md = fr_core_news_md.load()

CV_NAME = 'romain'
CV_DIR = 'cv_tests'
CV_PATH = os.path.join(CV_DIR, CV_NAME) + '.pdf'

cv_raw_text = cv_to_text(CV_PATH)
tokens = preprocess_cv_text(cv_raw_text, nlp_model=spacy_fr_md)
cv_vector = fasttext_wv_avg(tokens, fasttext_model)

# Safety check
assert len(cv_vector) == fasttext_model.get_dimension()
