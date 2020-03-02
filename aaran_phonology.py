from models.phonetics.phonemes import Consonant, Vowel
from models.phonetics.phonotactics import SyllableStructure, SylPart

# ===========  Phonology   ========== #

p = Consonant("p", False)
b = Consonant("b", True)
t = Consonant("t", False)
d = Consonant("d", True)
k = Consonant("k", False)
g = Consonant("g", True)

p.set_voice_pair(b)
t.set_voice_pair(d)
k.set_voice_pair(g)


n = Consonant("n", True)
r = Consonant("r", True)
l = Consonant("l", False)
v = Consonant("v", False)

i = Vowel("i")
e = Vowel("e")
o = Vowel("o")
u = Vowel("u")
a = Vowel("a")

eu = Vowel("eu", cluster=True)
au = Vowel("au", cluster=True)

oo = Vowel("ö")
aa = Vowel("ä")

a_high = Vowel("á")
a_low = Vowel("ă")
o_low = Vowel("ŏ")

# =========== Phonotactics ========== #

typical_syllable = SyllableStructure(
    [SylPart([p, b, t, d, k, g, r, n, l, v, r], optional=True)],
    [SylPart(Vowel.instances)],
    [SylPart([n, l], optional=True)]
)
