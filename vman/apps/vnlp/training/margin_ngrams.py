from typing import Dict, List, Tuple

from vman.apps.vnlp.training.alphabet import Alphabet
from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard


class MarginNgram:
    def __init__(self,
                 text: str,
                 direct: int,
                 dic_occurs: int = 0,
                 modified_count: int = 0):
        self.text = text
        self.direct = direct
        self.dic_occurs = dic_occurs
        self.modified_count = modified_count

    def __repr__(self):
        ps = 'prefix' if self.direct else 'suffix'
        return f'{self.text} ({ps}, {self.dic_occurs})'


class MarginNgramsCollector:
    def __init__(self,
                 alphabet: Alphabet,
                 dictionary: DetailedDictionary):
        self.alphabet = alphabet
        self.dictionary = dictionary
        self.unique_words = {w.word for w in dictionary.words}
        self.prefixes = []  # type: List[MarginNgram]
        self.suffixes = []  # type: List[MarginNgram]

    def build(self):
        prefixes = {}
        suffixes = {}
        for word in self.dictionary.words:  # type: WordCard
            for i in range(self.alphabet.prefix_min, self.alphabet.prefix_max + 1):
                reminder = len(word.word) - i
                if reminder < self.alphabet.prefix_min:
                    break
                prefix = word.word[:i]
                pref_count = prefixes.get(prefix) or 0
                prefixes[prefix] = pref_count + 1  # word.count
            for i in range(self.alphabet.suffix_min, self.alphabet.suffix_max + 1):
                reminder = len(word.word) - i
                if reminder < self.alphabet.prefix_min:
                    break
                suffix = word.word[-i:]
                suffix_count = suffixes.get(suffix) or 0
                suffixes[suffix] = suffix_count + 1  # word.count

        # remove rare cases
        threshold = 0.01
        min_count = int(self.dictionary.words_total * threshold)
        for sfx in prefixes:
            if prefixes[sfx] >= min_count:
                self.prefixes.append(MarginNgram(sfx, 1, prefixes[sfx]))
        for sfx in suffixes:
            if suffixes[sfx] >= min_count:
                self.suffixes.append(MarginNgram(sfx, -1, suffixes[sfx]))

        self.prefixes.sort(key=lambda p: -len(p.text) * 1000 - p.dic_occurs)
        self.suffixes.sort(key=lambda p: -len(p.text) * 1000 - p.dic_occurs)
        self.filter_by_orig_morph()
        self.prefixes = [p for p in self.prefixes if p.modified_count > 1]
        self.suffixes = [p for p in self.suffixes if p.modified_count > 1]

    def filter_by_orig_morph(self):
        src = [self.prefixes, self.suffixes]
        directions = [1, -1]
        for collection, direct in zip(src, directions):
            for item in collection:
                for word in self.dictionary.words:  # type: WordCard
                    if direct == 1:  # prefix
                        if not word.word.startswith(item.text):
                            continue
                        word_root = word.word[len(item.text):]
                        if len(word_root) < self.alphabet.root_min:
                            continue
                        if word_root in self.unique_words:
                            item.modified_count += 1
                    else:  # suffix
                        if not word.word.endswith(item.text):
                            continue
                        word_root = word.word[:len(item.text)]
                        if len(word_root) < self.alphabet.root_min:
                            continue
                        if word_root in self.unique_words:
                            item.modified_count += 1





