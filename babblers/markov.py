from _io import TextIOWrapper

class Markov:
    def __init__(self, text=None, n=1, start_same = False, split=' '):
        if text == None:
            self.text = None
        elif isinstance(text, TextIOWrapper):
            with text as file:
                self.text = file.read()
        elif isinstance(text, str):
            try:
                with open(text) as file:
                    self.text = file.read()
            except FileNotFoundError:
                self.text = text
        else:
            raise TypeError("Text must be TextIOWrapper or str, not {0}".format(type(text)))

        self.n = round(n)
        self.start_same = start_same
        self.split = split
        self.text = self.text.split(self.split)
        if start_same:
            for _ in range(n):
                self.text.insert(0, None)


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

def generate(text=None, n=1, start_same = False, split=' '):
    return Markov(text=text, n=n, start_same=start_same).generate()