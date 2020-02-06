from models.phonetics.phonemes import Phoneme, PhonemeCluster, Vowel
import typing


class InvalidNucleus(Exception):
    pass


class InvalidCoda(Exception):
    pass


class InvalidOnset(Exception):
    pass


class SylPart:
    optional: bool

    def __init__(self, bindings: typing.List[Phoneme], optional=False):
        self.bindings = bindings
        self.optional = optional


class SyllableStructure:
    onset: typing.List[SylPart]
    onset_opts: int
    nucleus: typing.List[SylPart]
    nucleus_opts: int = 0
    coda: typing.List[SylPart]
    coda_opts: int

    def __init__(self, onset=None, nucleus=None, coda=None):
        self.onset_opts = 0
        self.coda_opts = 0

        self.onset = onset if onset else []
        if self.onset:
            for i in self.onset:
                if i.optional:
                    self.onset_opts += 1

        self.nucleus = nucleus

        self.coda = coda if coda else []
        if self.coda:
            for i in self.coda:
                if i.optional:
                    self.coda_opts += 1


class Syllable:
    phoneme_cluster: PhonemeCluster
    nucleus: PhonemeCluster or None
    onset: PhonemeCluster or None
    coda: PhonemeCluster or None

    def __init__(self, *phonemes):
        self.phoneme_cluster = PhonemeCluster.from_sounds(list(phonemes))
        self.coda = None
        self.nucleus = None
        self.onset = None

    def __str__(self):
        return str(self.phoneme_cluster)

    def __repr__(self):
        return f"<Syllable ['{self.__str__()}']>"

    def check(self, phonotactics: SyllableStructure):
        nucleus_index = None
        for j, i in enumerate(self.phoneme_cluster.vec):
            if isinstance(i, Vowel):
                if i in phonotactics.nucleus[0].bindings:
                    self.nucleus = PhonemeCluster.from_sounds([i])
                    nucleus_index = j
                    break

        onset = self.phoneme_cluster.vec[:nucleus_index]
        coda = self.phoneme_cluster.vec[nucleus_index + 1:]

        if coda:
            for index, binding in enumerate(phonotactics.coda):
                if coda[index] not in binding.bindings:
                    raise InvalidCoda(f"Coda [{coda[index]}] is not allowed.")

        if len(coda) > len(phonotactics.coda):
            raise InvalidCoda("Too many Codas.")
        elif len(coda) < len(phonotactics.coda) - phonotactics.coda_opts:
            raise InvalidCoda("Not enough Codas.")

        if onset:
            for index, binding in enumerate(phonotactics.onset):
                if onset[index] not in binding.bindings:
                    raise InvalidOnset(f"Onset [{onset[index]}] is not allowed.")

        if len(onset) > len(phonotactics.onset):
            raise InvalidOnset("Too many Onsets.")
        elif len(onset) < len(phonotactics.onset) - phonotactics.onset_opts:
            raise InvalidOnset("Not enough Onsets.")

        self.onset = onset
        self.coda = coda

        return
