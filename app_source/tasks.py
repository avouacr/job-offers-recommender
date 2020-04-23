
import fasttext.util

def import_fasttext():
    """Download and extract FastText pre-trained word vectors."""
    print('Downloading and extracting FastText French model.')
    fasttext.util.download_model('fr', if_exists='ignore')
    print('FastText model ready to use.')
    return True