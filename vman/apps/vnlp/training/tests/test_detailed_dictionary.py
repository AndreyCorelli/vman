from unittest import TestCase

from vman.apps.vnlp.training.alphabet import EnAlphabet
from vman.apps.vnlp.training.corpus_features import CorpusFeatures
from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary


class TestDetailedDictionary(TestCase):
    def test_feed(self):
        path_src = '/home/andrey/sources/vman/vman/vman/corpus/raw/en'
        dd = DetailedDictionary.read_from_corpus(path_src)
        self.assertGreater(len(dd.words), 100)

    def test_corpus_features(self):
        path_src = '/home/andrey/sources/vman/vman/vman/corpus/raw/en'
        cf = CorpusFeatures('en', EnAlphabet, path_src)
        cf.build()
        self.assertGreater(len(cf.ngrams_collector.suffixes), 5)