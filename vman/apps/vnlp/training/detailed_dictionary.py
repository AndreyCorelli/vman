import os
import codecs
from typing import List, Dict


class WordCard:
    def __init__(self, word: str, count: int = 1, root: str = ''):
        self.word = word
        self.root = root
        self.count = count

    def __repr__(self):
        return f'{self.word} [{self.count}]'


class DetailedDictionary:
    def __init__(self):
        self.words = []  # type:List[WordCard]
        self.words_total = 0

    @classmethod
    def read_from_corpus(cls, corpus_path: str):  # DetailedDictionary
        dd = DetailedDictionary()
        files = [f for f in os.listdir(corpus_path)]
        word_count = {}  # type: Dict[str, int]
        for file_name in files:
            full_path = os.path.join(corpus_path, file_name)
            if not os.path.isfile(full_path):
                continue
            cls.read_file(full_path, word_count)

        for w in word_count:
            dd.words_total += 1
            dd.words.append(WordCard(w, word_count[w]))
        dd.words.sort(key=lambda w: w.word)
        #dd.words.sort(key=lambda w: -w.count)
        return dd

    @classmethod
    def read_file(cls, file_path: str, word_count: Dict[str, int]):
        with codecs.open(file_path, 'r', encoding='utf-8') as fr:
            text = fr.read()
        words = text.split(' ')
        for w in words:
            if not w:
                continue
            count = word_count.get(w) or 0
            word_count[w] = count + 1