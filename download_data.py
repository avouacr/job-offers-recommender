
import gdown
from fasttext.util import download_model


if __name__ == '__main__':
    
    print('Download job offers data')
    offers_url = 'https://drive.google.com/uc?export=download&confirm=A6wL&id=1tI4SctLNkZU6vJuBw1Hf1lVqephc35cG'
    gdown.download(offers_url, 'data/all_offers.csv', quiet=False)

    print('Download FastText representations of job offers')
    vectors_url = 'https://drive.google.com/uc?export=download&confirm=1Rhc&id=1uK1wLdzR7dS-kqZti-4jLYXos5pLKyed'
    gdown.download(offers_url, 'data/offers_fasttext.npy', quiet=False)

    print('Download FastText French model')
    download_model('fr', if_exists='ignore')
