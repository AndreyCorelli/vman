from typing import Optional

from vman.apps.vnlp.training.alphabet import Alphabet
from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary
from vman.apps.vnlp.training.margin_ngrams import MarginNgramsCollector


class CorpusFeatures:
    def __init__(self,
                 language: str,
                 alphabet: Alphabet,
                 corpus_path: str):
        self.language = language
        self.alphabet = alphabet
        self.corpus_path = corpus_path
        self.dictionary = None  # type: Optional[DetailedDictionary]
        self.ngrams_collector = None  # type: Optional[MarginNgramsCollector]

    def build(self):
        self.dictionary = DetailedDictionary.read_from_corpus(self.corpus_path)
        self.ngrams_collector = MarginNgramsCollector(self.alphabet, self.dictionary)
        self.ngrams_collector.build()
