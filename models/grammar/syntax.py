import typing


class Sentence:
    def __init__(self, *args):
        from models.grammar.morphology import Word
        self.words: typing.List[Word]
        self.words += list(args)
