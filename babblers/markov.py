from _io import TextIOWrapper
from string import punctuation
import random

class Markov:
    def __init__(self, text=None, n=1, start_same = False, split=' '):
        self.text = self._parse_text(text)
        self.n = round(n)
        self.start_same = start_same
        self.split = split
        self.ngrams, self.starts = self._generate_ngrams()

    def generate(self, length=500):
        babbled = ''
        if self.start_same:
            curr = [None] * self.n
        else:
            curr = random.choice(self.starts)

        for i in range(length):
            next = random.choice(self.ngrams[curr])
            curr.remove(0)
            curr.append(next)
            babbled += next + " "
        return babbled

    def _generate_ngrams(self):
        ngrams, starts = {}, []
        curr = [None] * self.n
        for i in range(len(self.text) - 1):
            curr.remove(0)
            curr.append(self.text[i])
            if curr not in ngrams:
                ngrams[curr] = []
            ngrams[curr].append(self.text[i + 1])
            if self.text[i] in '!.?':
                starts.append(self.text[i+1:i+n])
        return ngrams, starts

    def _parse_text(self, text):
        if text == None:
            _text = None
        elif isinstance(text, TextIOWrapper):
            with text as file:
                _text = file.read()
        elif isinstance(text, list):
            pass
        elif isinstance(text, str):
            try:
                with open(text) as file:
                    _text = file.read()
            except FileNotFoundError:
                _text = text
        else:
            _text = ''
            for file in text:
                _text += self._parse_text(file)
        # raise TypeError("Text must be TextIOWrapper, str, not {0}".format(type(text)))

        _text = _text.split(self.split)
        if self.start_same:
            _text = [None] * self.n + _text

        parsed = []
        for word in _text:
            parsed.append(word.strip(punctuation))
            if word.endswith(tuple(punctuation)):
                parsed.append(word.strip(word.strip(punctuation)))
        return parsed


def generate(text=None, n=1, start_same = False, split=' '):
    return Markov(text=text, n=n, start_same=start_same).generate()