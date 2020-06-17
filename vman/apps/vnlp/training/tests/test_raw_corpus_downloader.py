from unittest import TestCase

from vman.apps.vnlp.training.alphabet import EnAlphabet
from vman.apps.vnlp.training.raw_corpus_downloader import RawCorpusDownloader


class TestRawCorpusDownloader(TestCase):
    def test_feed(self):
        path_src = '/home/andrey/Downloads/src_files/vman'
        path_dst = '/home/andrey/sources/vman/vman/vman/corpus/raw/en'
        RawCorpusDownloader.download(path_src, path_dst, EnAlphabet)
