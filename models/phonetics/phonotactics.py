from models.phonetics.phonemes import Consonant, Vowel
import typing


class EmptyNucleusError(Exception):
    pass


class SyllabicPart:
    bindings: typing.List[typing.List[Consonant] or typing.List[Vowel]]

    def __init__(self, *args):
        self.bindings = list(args)


class Coda(SyllabicPart):
    pass


class Nucleus(SyllabicPart):
    def __init__(self, *args):
        super().__init__(*args)
        if not self.bindings:
            raise EmptyNucleusError


class Onset(SyllabicPart):
    pass


class Syllable:
    phonemes: list

    def __init__(self, *phonemes):
        self.phonemes = list(phonemes)

    def check(self, phonotactics):
        pass


class SyllableStructure:
    onset: Onset
    nucleus: Nucleus
    coda: Coda

    def __init__(self, onset, nucleus, coda):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda
