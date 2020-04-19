
import re
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd
import unidecode
import fasttext.util


def import_stopwords():
    """Import list of French stopwords.

    Source : https://github.com/stopwords-iso/stopwords-fr
    """
    with open('data/stopwords-fr.txt', 'r') as f:
        stopwords = f.read().splitlines()
    stopwords = [unidecode.unidecode(x) for x in stopwords]
    return stopwords

fr_stopwords = import_stopwords()

def preprocess_and_tokenize(doc):
    """Preprocess document, tokenize and remove stop words."""
    doc = doc.lower()
    doc = unidecode.unidecode(doc)
    tokens = re.findall(r'\b\w\w+\b', doc)
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

def compute_vectors(corpus, n_jobs=1):
    """Compute document vectors over the whole corpus."""
    if n_jobs == 1:
        corpus_prepro = []
        for doc in corpus:
            corpus_prepro.append(fasttext_wv_avg(doc))
    elif n_jobs > 1:
        with Pool(n_jobs) as p:
            corpus_prepro = p.map(fasttext_wv_avg, corpus)

    return np.array(corpus_prepro)


if __name__ == '__main__':
    # Load job offers in the current db
    print('Load job offers.')
    df_offers = pd.read_csv('data/all_offers_nodup.csv',
                            usecols=['id', 'description'])
    df_offers['description'] = df_offers['description'].astype(str)
    # TODO: handle duplicates and string conversion while generating the csv
    # df_offers = df_offers.drop_duplicates()

    # Compute document representations using FastText model
    print('Compute FastText representations of job offers.')
    doc_vectors = compute_vectors(df_offers['description'].values,
                                  n_jobs=cpu_count())

    # Safety checks
    assert doc_vectors.shape[0] == df_offers.shape[0]
    assert doc_vectors.shape[1] == fasttext_model.get_dimension()

    # Store document vectors
    print('Save results.')
    np.save('data/offers_fasttext.npy',
            doc_vectors)
