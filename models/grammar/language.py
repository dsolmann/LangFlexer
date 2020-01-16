import typing

from models.phonetics.phonotactics import SyllableStructure
from models.phonetics.phonemes import PhonemeCluster
from models.grammar.morphology.morphology import Word, Morpheme


def check_phonotactics(phonotactics: SyllableStructure, phoneme_cluster: PhonemeCluster):
    return True


class Language:
    name: str
    morphemes: typing.List[Morpheme]
    words: typing.List[Word]
    phonotactics_binding: SyllableStructure

    def __init__(self, name):
        self.name = name

    def add_morphemes(self, *morph: Morpheme):
        for i in morph:
            if not check_phonotactics(self.phonotactics_binding, i.phoneme_cluster_association):
                print(f"Morpheme {str(i)} is not phonotactics compliant. Consider revising it.")
        self.morphemes += morph

    def add_words(self, *words):
        self.words += words
