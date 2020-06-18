import os
from unittest import TestCase

from vman.apps.vnlp.training.alphabet import EnAlphabet
from vman.apps.vnlp.training.raw_corpus_downloader import RawCorpusDownloader
from vman.corpus.corpus_data import RAW_CORPUS_ROOT


class TestRawCorpusDownloader(TestCase):
    def test_feed(self):
        path_src = '/home/andrey/Downloads/src_files/text/en_classic'
        path_dst = os.path.join(RAW_CORPUS_ROOT, 'en')
        RawCorpusDownloader.download(path_src, path_dst, EnAlphabet)
