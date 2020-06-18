import os
from unittest import TestCase

from vman.apps.vnlp.training.alphabet import EnAlphabet
from vman.apps.vnlp.training.corpus_features import CorpusFeatures
from vman.corpus.corpus_data import RAW_CORPUS_ROOT


class TestCorpusFeatures(TestCase):
    def test_corpus_features(self):
        path_src = os.path.join(RAW_CORPUS_ROOT, 'en')
        cf = CorpusFeatures('en', EnAlphabet, path_src)
        cf.build()
        self.assertGreater(len(cf.ngrams_collector.suffixes), 5)
