from models.phonetics.phonemes import Consonant, Vowel
from models.phonetics.phonotactics import SyllableStructure, Coda, Nucleus, Onset, Syllable

from models.grammar.morphology import Morpheme, PartOfSpeech
from models.grammar.morphology.aspects import RootAspect, POSAspect

# ===========  Phonology   ========== #

p = Consonant("p", False)
b = Consonant("b", True)
p.set_voice_pair(b)

t = Consonant("t", False)
d = Consonant("d", True)
t.set_voice_pair(d)

k = Consonant("k", False)
g = Consonant("g", True)
k.set_voice_pair(g)

i = Vowel("i")
e = Vowel("e")
o = Vowel("o")
u = Vowel("u")
a = Vowel("a")

oo = o.derivate_wl(2)
aa = a.derivate_wl(2)

print(list(map(str, Vowel.instances)))

# =========== Phonotactics ========== #
typical_syllable = SyllableStructure(Onset(Consonant.instances, None), Nucleus(Vowel.instances), Coda())

# ============= Grammar ============= #
verb = PartOfSpeech("VERB")
noun = PartOfSpeech("NOUN")

# ============= Lexicon ============= #
# 1. Root morphemes:
water = Morpheme(t+oo, aspects=[RootAspect("water"), POSAspect(noun)])
place = Morpheme(a+k+i, aspects=[RootAspect("place"), POSAspect(noun)])
go = Morpheme(d+e+u, aspects=[RootAspect("go"), POSAspect(verb)])

# 2. Grammar morphemes:
verb_m_1 = Morpheme(p+a, aspects=[POSAspect(verb)])

# 3. Connecting words:
river = place + water + go

# TODO:
# 1. Phonotactic checks
# 2. Head-first/Head-last
# 3. Word Order

if __name__ == '__main__':
    print(str(river))
    print(str(river.trace()))
    ''' 
    > akitoodeu
    > place+NOUN+water+NOUN+go+VERB
    '''
