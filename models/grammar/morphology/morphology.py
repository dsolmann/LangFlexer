import typing

from models.grammar.syntax import Sentence
from models.phonetics.phonemes import PhonemeCluster, Phoneme, Vowel
from models.phonetics.phonotactics import Syllable, SyllableStructure


class NoRootException(Exception):
    pass


class Word:
    morphemes: list
    overridden_meaning: typing.Optional[str]
    overridden_spelling: typing.Optional[PhonemeCluster]
    alternates: list
    _str = ""

    def __init__(self, *args, part_of_speech=None):
        args: typing.List[Morpheme] = list(args)
        self.morphemes = list(args)
        self.alternates = []
        self.pos = part_of_speech
        self.overridden_meaning = None
        self.overridden_spelling = None
        if not self.compile_morphology(False):
            print(f'WARNING: Word "{"".join(map(str, args))}" do not have any roots. Consider adding one.')

    def link_alter(self, other):
        self.alternates.append(other)
        other.alternates.append(self)

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

    def syllabic_separator(self, phonotactics: SyllableStructure = None) -> typing.List[Syllable]:
        phonemes = self.phonemer()
        # print(phonemes)
        vowels = []
        for n, i in enumerate(phonemes):
            if isinstance(i, Vowel):
                vowels.append(n)
        # vowels.reverse()
        # print(vowels)
        syllables = []
        for i in vowels:
            if i > 0 and i-1 not in vowels:
                syllable = phonemes[i - 1:i + 1]
            else:
                syllable = [phonemes[i]]
            # print("Syl:", syllable)
            syllables.append(Syllable(PhonemeCluster.from_sounds(syllable)))

        return syllables

    def phonemer(self) -> typing.List[Phoneme]:
        z = []
        for i in self.morphemes:
            z += i.phoneme_cluster_association.vec

        return z

    def __str__(self):
        return self.trace_phonology() if not self.overridden_spelling \
            else "".join(map(str, self.overridden_spelling.vec))

    def __add__(self, other):
        if type(other) is Word:
            new_word = Word(*self.morphemes, *other.morphemes)
            new_word.pos = self.pos or other.pos  # FIXME: Check Head-Last or Head-First
            return new_word
        elif type(other) is Morpheme:
            new_word = Word(*self.morphemes, other)
            return new_word
        else:
            raise TypeError

    def trace_meaning(self):
        pos_already = None
        from models.grammar.morphology.aspects import POSAspect
        final_str = ""
        for i in self.morphemes:
            final_str += f'{i.trace()}+'
            for j in i.aspects:
                if isinstance(j, POSAspect):
                    pos_already = j
        return final_str[:-1], pos_already

    def trace_phonology(self):
        if self._str != "":
            return self._str
        try:
            self.compile_morphology()
            return self._str
        except NoRootException:
            print("WARNING: Your Word still does not have a Root. And you are trying to compile it. That's bad.")
            return ''.join(map(str, self.morphemes))

    def get_aprx_meaning(self, head_last_order=True):
        pos_already = None
        if not self.overridden_meaning:
            f_str, pos_already = self.trace_meaning()
        else:
            f_str = self.overridden_meaning
        if head_last_order and self.pos and (pos_already and pos_already.pos != self.pos):
            f_str += f"+{self.pos}"

        # TODO: Some word order magic...

        return f_str


class PartOfSpeech(object):
    short_doc: str = ""
    name = ""

    def __init__(self, name, short_doc=""):
        self.name = name
        self.short_doc = short_doc

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__str__()} POS>"


class Morpheme:
    aspects: list
    phoneme_cluster_association: PhonemeCluster
    variations: list

    def __init__(self, phoneme, aspects: list = None, variations=[]):
        if aspects is not None:
            self.aspects = aspects
        else:
            self.aspects = []
            print("WARNING: You've not assigned any aspects to your morpheme.")

        def fix_types(a):
            if isinstance(a, PhonemeCluster):
                return a
            elif isinstance(a, Phoneme):
                return PhonemeCluster.from_sounds([a])
            else:
                raise Exception("Hey! YOU ARE WRONG.")

        phoneme = fix_types(phoneme)
        self.phoneme_cluster_association: PhonemeCluster = phoneme
        self.variations: typing.List[Morpheme] = variations

    def __str__(self):
        return str(self.phoneme_cluster_association)

    def __add__(self, other):
        if type(other) is Morpheme:
            return Word(self, other)
        elif type(other) is Word:
            new_word = Word(self, *other.morphemes)
            return new_word
        else:
            raise TypeError(f"You're trying to connect Morpheme with {type(other)}")

    def trace(self):
        def sep(x):
            return x.short_doc + "+"

        return "".join(map(sep, self.aspects))[:-1]

    def __repr__(self):
        return f"<Morpheme {str(self)}>"

    def link(self, other):
        self.variations.append(other)
        other.variations.append(self)

    def as_word(self):
        return Word(self)
