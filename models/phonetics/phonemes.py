import random
import typing
import weakref


class NoVoiceException(Exception):
    pass


class Phoneme:
    def __init__(self, spelling):
        self.spelling = spelling

    def __str__(self):
        return self.spelling


class PhonemeCluster:
    vec: typing.List[Phoneme]

    @staticmethod
    def from_sounds(sounds):
        a = PhonemeCluster()
        a.vec = []
        for i in sounds:
            if type(i) is PhonemeCluster:
                a.vec += i.vec
            elif type(i) is Vowel or Consonant:
                a.vec.append(i)
        return a

    def __add__(self, other):
        if type(other) is Consonant or type(other) is Vowel:
            self.vec.append(other)
            return self
        elif type(other) is PhonemeCluster:
            return PhonemeCluster.from_sounds(self.vec + other.vec)
        else:
            raise TypeError

    def __str__(self):
        return "".join(map(str, self.vec))


class Consonant(Phoneme):
    spelling: str
    voiced: bool = False
    rel_voiced = None
    rel_near = []
    instances = []

    def __init__(self, spelling, voiced, rel_voiced=None, rel_near=None):
        super().__init__(spelling)
        self.__class__.instances.append(weakref.proxy(self))
        self.rel_near = rel_near if rel_near else []
        self.voiced = voiced
        self.rel_voiced = rel_voiced

    def as_voiced(self):
        if self.voiced:
            return self
        elif self.rel_voiced:
            return self.rel_voiced
        else:
            raise NoVoiceException

    def set_voice_pair(self, other):
        self.rel_voiced: Consonant = other
        other.rel_voiced = self

    def as_unvoiced(self):
        if self.voiced:
            return self.rel_voiced
        elif self.rel_voiced:
            return self
        else:
            raise NoVoiceException

    def rand_mutate(self):
        return random.choice(self.rel_near)

    def __repr__(self):
        return f"<Consonant ['{self.spelling}']>"

    def __add__(self, other) -> PhonemeCluster:
        if type(other) is Consonant or type(other) is Vowel:
            return PhonemeCluster.from_sounds(sounds=[self, other])
        elif type(other) is PhonemeCluster:
            other.vec.append(self)
            return other
        else:
            raise TypeError


class Vowel(Phoneme):
    spelling: str
    default_longness: int = 1
    instances = []

    def __init__(self, spelling, default_longness=1, cluster=False):
        super().__init__(spelling)
        self.default_longness = default_longness
        self.cluster = cluster
        self.__class__.instances.append(weakref.proxy(self))

    def __repr__(self):
        return f"<Vowel{' cluster' if self.cluster else ''} ['{self.spelling*self.default_longness}']>"

    def __str__(self):
        return self.spelling*self.default_longness

    def __add__(self, other) -> PhonemeCluster:
        if type(other) is Consonant or type(other) is Vowel:
            return PhonemeCluster.from_sounds(sounds=[self, other])
        elif type(other) is PhonemeCluster:
            other.vec.append(self)
            return other
        else:
            raise TypeError

    def derivate_wl(self, new_longness):
        nc = Vowel(self.spelling)
        nc.default_longness = new_longness
        return nc
