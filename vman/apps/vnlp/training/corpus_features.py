from typing import Optional, Set, Dict, List, Tuple

from vman.apps.vnlp.training.alphabet import Alphabet
from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard
from vman.apps.vnlp.training.margin_ngrams import MarginNgramsCollector, MarginNgram


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
        self.find_dict_morphs()

    def find_dict_morphs(self):
        all_words = {d.word for d in self.dictionary.words}
        for word in self.dictionary.words:  # type: WordCard
            # { root (word): [prefix?, suffix?] }
            possible_roots = []  # type: List[Tuple[str, List[MarginNgram]]]
            morph_collections = [self.ngrams_collector.prefixes, self.ngrams_collector.suffixes]
            for pref in self.ngrams_collector.prefixes:
                # possible root
                pos_rt = pref.chop_from_word(word.word, self.alphabet)
                if not pos_rt:
                    continue
                exists, ngr = self.word_morphs_exist(pos_rt, pref, morph_collections, all_words)
                if not exists:
                    continue
                modifiers = [pref, ngr] if ngr else [pref]
                possible_roots.append((pos_rt, modifiers,))
            morph_collections = [self.ngrams_collector.suffixes, self.ngrams_collector.prefixes]
            for sufx in self.ngrams_collector.suffixes:
                pos_rt = sufx.chop_from_word(word.word, self.alphabet)
                if not pos_rt:
                    continue
                exists, ngr = self.word_morphs_exist(pos_rt, sufx, morph_collections, all_words)
                if not exists:
                    continue
                modifiers = [ngr, sufx] if ngr else [sufx]
                possible_roots.append((pos_rt, modifiers,))

            if possible_roots:
                # the shortest root with more modifiers has priority
                possible_roots.sort(key=lambda r: len(r[1]) * 10 - len(r[0]))
                word.root = possible_roots[0][0]
                mod_by_dir = {r.direct: r.text for r in possible_roots[0][1]}
                word.prefix = mod_by_dir.get(1) or ''
                word.suffix = mod_by_dir.get(-1) or ''

    def word_morphs_exist(self,
                          word: str,
                          chopped: MarginNgram,
                          modifiers: List[List[MarginNgram]],
                          all_words: Set[str]) -> Tuple[bool, Optional[MarginNgram]]:
        if word in all_words:
            return True, None
        if not modifiers:
            return False, None

        for ngram in modifiers[0]:
            if ngram.text == chopped.text and ngram.direct == chopped.direct:
                continue
            mod_word = ngram.add_to_word(word)
            exists, ngr = self.word_morphs_exist(mod_word, ngram, modifiers[1:], all_words)
            if exists:
                return True, ngr
        return False, None

