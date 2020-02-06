from models.phonetics.phonemes import Consonant, Vowel
from models.phonetics.phonotactics import SyllableStructure, Syllable, SylPart

from models.grammar.morphology import Morpheme, PartOfSpeech
from models.grammar.morphology.aspects import RootAspect, POSAspect
from models.grammar.language import Language

# =========== A:Ra Lang  ========== #

aaran = Language("Aaran")

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

n = Consonant("n", True)
r = Consonant("r", True)

i = Vowel("i")
e = Vowel("e")
o = Vowel("o")
u = Vowel("u")
a = Vowel("a")

eu = Vowel("eu", cluster=True)
au = Vowel("au", cluster=True)

oo = o.derivate_wl(2)
aa = a.derivate_wl(2)

# =========== Phonotactics ========== #

typical_syllable = SyllableStructure(
    [SylPart(Consonant.instances, optional=True)],
    [SylPart(Vowel.instances)],
    [SylPart([n, r], optional=True)]
)

aaran.set_syllable_structure(typical_syllable)

# ============= Grammar ============= #
verb = PartOfSpeech("VERB")
noun = PartOfSpeech("NOUN")

# ============= Lexicon ============= #
# 1. Root morphemes:
water = Morpheme(t+oo, aspects=[RootAspect("water"), POSAspect(noun)])
place = Morpheme(a+k+i, aspects=[RootAspect("place"), POSAspect(noun)])
go = Morpheme(d+eu, aspects=[RootAspect("go"), POSAspect(verb)])
tell = Morpheme(aa+r, aspects=[RootAspect("tell", "pronounce"), POSAspect(verb)])
# 2. Grammar morphemes:
verb_m_1 = Morpheme(p+a, aspects=[POSAspect(verb)])
noun_m_1 = Morpheme(a+n, aspects=[POSAspect(noun)])

aaran.add_morphemes(water, place, go, verb_m_1)

# 3. Creating words:
river = place + water + go
language = tell+noun_m_1

aaran.add_words(water, place, go, river, language)


# TODO:
# 1. Phonotactic checks (partially working, problems with coda syllable splitting)
# 2. Head-first/Head-last
# 3. Word Order
# 4. Tonality

if __name__ == '__main__':
    print(str(language))
    print(str(language.trace()))
    _dbg_a = language.syllabic_separator()
    print(_dbg_a)

    # water_word = water.as_word()
    # print(str(water_word))
    # print(str(water_word.trace()))
    # _dbg_b = water_word.syllabic_separator()
    # print(_dbg_b)

    # water_word.compile_morphology()
    # river.compile_morphology()

    aaran.compile()
    aaran.print_info()
