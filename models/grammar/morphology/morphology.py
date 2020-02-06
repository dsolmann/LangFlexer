import typing

from models.grammar.syntax import Sentence
from models.phonetics.phonemes import PhonemeCluster, Phoneme, Vowel
from models.phonetics.phonotactics import Syllable


class NoRootException(Exception):
    pass


class Word:
    morphemes: list
    _str = ""

    def __init__(self, *args):
        from models.grammar.morphology.aspects import RootAspect

        args: typing.List[Morpheme] = list(args)
        self.morphemes = list(args)
        if not self.compile_morphology(False):
            print(f'WARNING: Word "{"".join(map(str, args))}" do not have any roots. Consider adding one.')

    def compile_morphology(self, raise_exception=True):
        from models.grammar.morphology.aspects import RootAspect

        for i in self.morphemes:
            if any(isinstance(x, RootAspect) for x in i.aspects):
                self._str = "".join(map(str, self.morphemes))
                return True
        if raise_exception:
            raise NoRootException
        else:
            return False

    def syllabic_separator(self) -> typing.List[Syllable]:
        phonemes = self.phonemer()
        # print(phonemes)
        vowels = []
        for n, i in enumerate(phonemes):
            if isinstance(i, Vowel):
                vowels.append(n)
        # print(vowels)
        syllables = []
        for i in vowels:
            syllable = [phonemes[i]]
            # print(syllable)
            for j in range(i-1, -1, -1):
                # print("HOP", phonemes[j])
                if isinstance(phonemes[j], Vowel):
                    break
                else:
                    syllable.insert(0, phonemes[j])
            syllables.append(Syllable(PhonemeCluster.from_sounds(syllable)))

        return syllables

    def phonemer(self) -> typing.List[Phoneme]:
        z = []
        for i in self.morphemes:
            z += i.phoneme_cluster_association.vec

        return z

    def __str__(self):
        if self._str != "":
            return self._str

        try:
            self.compile_morphology()
            return self._str
        except NoRootException:
            print("WARNING: Your Word still does not have a Root. And you are trying to compile it. That's bad.")
            return ''.join(map(str, self.morphemes))

    def __add__(self, other):
        if type(other) is Word:
            return Sentence(self, other)
        elif type(other) is Morpheme:
            self.morphemes.append(other)
            return self
        else:
            raise TypeError

    def trace(self):
        final_str = ""
        for i in self.morphemes:
            final_str += f'{i.trace()}+'
        return final_str[:-1]


class PartOfSpeech(object):
    short_doc: str = ""
    name = ""

    def __init__(self, name, short_doc=""):
        self.name = name
        self.short_doc = short_doc


class Morpheme:
    aspects: list
    phoneme_cluster_association: PhonemeCluster

    def __init__(self, phoneme, aspects=None):
        if aspects is not None:
            self.aspects = aspects
        else:
            self.aspects = []
            print("WARNING: You've not assigned any aspects to your morpheme.")
        self.phoneme_cluster_association: PhonemeCluster = phoneme

    def __str__(self):
        return str(self.phoneme_cluster_association)

    def __add__(self, other):
        if type(other) is Morpheme:
            return Word(self, other)
        elif type(other) is Word:
            other.morphemes.insert(0, self)
            return other
        else:
            raise TypeError

    def trace(self):
        def sep(x):
            return x.short_doc + "+"

        return "".join(map(sep, self.aspects))[:-1]

    def __repr__(self):
        return f"<Morpheme {str(self)}>"

    def as_word(self):
        return Word(self)
