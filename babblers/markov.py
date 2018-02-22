from _io import TextIOWrapper
from string import punctuation

class Markov:
    def __init__(self, text=None, n=1, start_same = False, split=' '):
        self.text = self._parse_text(text)
        self.n = round(n)
        self.start_same = start_same
        self.split = split
        self.ngrams = self._generate_ngrams()

    def generate(self):
        pass

    def _generate_ngrams(self):
        ngrams = {}
        curr = [None] * self.n
        for i in range(len(self.text) - 1):
            curr.remove(0)
            curr.append(self.text[i])
            if curr not in ngrams:
                ngrams[curr] = []
            ngrams[curr].append(self.text[i + 1])
        return ngrams

    def _parse_text(self, text):
        if text == None:
            _text = None
        elif isinstance(text, TextIOWrapper):
            with text as file:
                _text = file.read()
        elif isinstance(text, str):
            try:
                with open(text) as file:
                    _text = file.read()
            except FileNotFoundError:
                _text = text
        else:
            raise TypeError("Text must be TextIOWrapper or str, not {0}".format(type(text)))

        _text = _text.split(self.split)
        if self.start_same:
            _text = [None] * self.n + _text

        parsed = []
        for word in _text:
            if word.endswith(tuple(punctuation)):
                parsed.append(word.strip(punctuation))
                parsed.append(word.strip(word.strip(punctuation)))
        return parsed


def generate(text=None, n=1, start_same = False, split=' '):
    return Markov(text=text, n=n, start_same=start_same).generate()