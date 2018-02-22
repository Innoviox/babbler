from _io import TextIOWrapper
from string import punctuation
import random

class Markov:
    def __init__(self, text=None, n=2, start_same = False, split=None):
        self.n = round(n) + 1
        self.start_same = start_same
        self.split = split
        self.text = self._parse_text(text)
        self.ngrams, self.starts = self._generate_ngrams()

    def _generate(self, length):
        if self.start_same:
            curr = [None] * self.n
        else:
            curr = random.choice(self.starts)

        for i in range(length):
            next = random.choice(self.ngrams[str(curr)])
            curr.pop(0)
            curr.append(next)
            yield next

    def generate(self, length=500):
        return ' '.join(self._generate(length))

    def _generate_ngrams(self):
        ngrams, starts = {}, []
        curr = [None] * self.n
        for i in range(len(self.text) - 1):
            curr.pop(0)
            curr.append(self.text[i])
            key = str(curr)
            if key not in ngrams:
                ngrams[key] = []
            ngrams[key].append(self.text[i + 1])
            if self.text[i] in '!.?':
                starts.append(self.text[i: i + self.n])
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
        _text = _text.split(self.split)
        if self.start_same:
            _text = [None] * self.n + _text

        parsed = []
        for word in _text:
            parsed.append(word.strip(punctuation))
            if word.endswith(tuple(punctuation)):
                parsed.append(word.strip(word.strip(punctuation)))
        return list(filter(bool, parsed))


def generate(text=None, n=2, start_same = False, split=' '):
    return Markov(text=text, n=n, start_same=start_same).generate()