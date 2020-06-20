import os
from unittest import TestCase

from vman.apps.vnlp.training.alphabet import EnAlphabet
from vman.apps.vnlp.training.corpus_features import CorpusFeatures
from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard
from vman.apps.vnlp.training.margin_ngrams import MarginNgramsCollector, MarginNgram
from vman.corpus.corpus_data import RAW_CORPUS_ROOT


class TestCorpusFeatures(TestCase):
    def test_corpus_features(self):
        path_src = os.path.join(RAW_CORPUS_ROOT, 'en')
        cf = CorpusFeatures('en', EnAlphabet, path_src)
        cf.build()
        self.assertGreater(len(cf.ngrams_collector.suffixes), 5)

    def test_find_morphs(self):
        cf = CorpusFeatures('en', EnAlphabet, '')
        cf.dictionary = DetailedDictionary()
        cf.dictionary.words = [
            WordCard('deprived', 10),
            WordCard('prived', 6),
            WordCard('deprive', 5)
        ]
        cf.dictionary.words_total = len(cf.dictionary.words)
        cf.all_words = {d.word for d in cf.dictionary.words}
        cf.ngrams_collector = MarginNgramsCollector(cf.alphabet, cf.dictionary)
        cf.ngrams_collector.prefixes.append(MarginNgram('de', 1, 3, 1))
        cf.ngrams_collector.prefixes.append(MarginNgram('in', 1, 2, 1))
        cf.ngrams_collector.suffixes.append(MarginNgram('ion', -1, 3, 1))
        cf.ngrams_collector.suffixes.append(MarginNgram('d', -1, 4, 1))
        cf.find_dict_morphs()
        wrd = cf.dictionary.words[0]
        self.assertGreater(len(wrd.root), 0)

