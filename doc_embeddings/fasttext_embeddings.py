
import re
from multiprocessing import Pool, cpu_count
from urllib import request
import pandas as pd
import numpy as np

import unidecode
import fasttext.util


def import_stopwords():
    """Download and import French stopwords."""
    URL = 'https://raw.githubusercontent.com/stopwords-iso/stopwords-fr/master/stopwords-fr.txt'
    response = request.urlopen(URL)
    stopwords = response.read().decode('utf-8').splitlines()
    stopwords = [unidecode.unidecode(x) for x in stopwords]
    return stopwords


def preprocess_and_tokenize(doc):
    """Preprocess document, tokenize and remove stop words."""
    doc = doc.lower()
    doc = unidecode.unidecode(doc)
    tokens = re.findall(r'\b\w\w+\b', doc)
    fr_stopwords = import_stopwords()
    tokens = [x for x in tokens if x not in fr_stopwords]
    return tokens


def import_fasttext(path_bin=None):
    """Download and import FastText pre-trained word vectors."""
    if path_bin is not None:
        model = fasttext.load_model(path_bin)
    else:
        print('The binary of FastText French model was not provided.',
              'Will download, uncompress and load it. This takes a long time.')
        fasttext.util.download_model('fr', if_exists='ignore')
        model = fasttext.load_model('cc.fr.300.bin')

    return model

fasttext_model = import_fasttext('models/cc.fr.300.bin')

def fasttext_wv_avg(doc):
    """Compute average of FastText's word vectors over a document tokens.."""
    tokens = preprocess_and_tokenize(doc)

    if tokens:
        wv_tokens = []
        for i, tok in enumerate(tokens):
            try:
                wv_tokens.append(fasttext_model.get_word_vector(tok))
            except KeyError:
                pass

        wv_mat = np.array(wv_tokens)
        text_vec = wv_mat.mean(axis=0)
    else:
        text_vec = np.zeros(fasttext_model.get_dimension())

    return text_vec


def fasttext_wv_avg_corpus(corpus, n_jobs=cpu_count()-1):
    """Parallelize preprocessing and document vectors computation."""
    with Pool(n_jobs) as p:
        corpus_prepro = p.map(fasttext_wv_avg, list(corpus))
    return np.array(corpus_prepro)
