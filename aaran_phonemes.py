from models.phonetics.phonemes import Consonant, Vowel
from models.phonetics.phonotactics import SyllableStructure, Syllable, SylPart
from copy import copy, deepcopy
from models.grammar.morphology import Morpheme, PartOfSpeech, Word
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

aaran.set_syllable_structure(typical_syllable)

# ============= Grammar ============= #
verb = PartOfSpeech("VERB")
noun = PartOfSpeech("NOUN")
adjective = PartOfSpeech("ADJ")

# ============= Lexicon ============= #
_water = Morpheme(a_high+a_low, aspects=[RootAspect("water")])
water = Word(_water, part_of_speech=noun)

_place_1 = Morpheme(e+r+e, aspects=[RootAspect("place")])
_place_2 = Morpheme(r+e, aspects=[RootAspect("place")])
_place_2.link(_place_1)

place = Word(_place_1)

river = water+_place_2
river.overridden_meaning = "river"

river_alt = water+_place_2
river_alt.overridden_spelling = a_high+a_low+r

river.link_alter(river_alt)

_belong = Morpheme(a_high+n, aspects=[RootAspect("belong")])
belong = Word(_belong, part_of_speech=verb)

_go = Morpheme(t+a, aspects=[RootAspect("go")])
_go_verbify = Morpheme(t+a, aspects=[POSAspect(verb)])
_go.link(_go_verbify)

go = Word(_go, part_of_speech=verb)

_long = Morpheme(n+a, aspects=[RootAspect("long")])
_big = Morpheme(n+a, aspects=[RootAspect("big")])
_long.link(_big)

flow = Word(_go, _long)
flow.overridden_meaning = "flow"
flow.pos = noun

word_continue = flow+_go_verbify
word_continue.overridden_meaning = "continue"

adj = Morpheme(l+a_low+o, aspects=[POSAspect(adjective)])
water_adj = water+adj

_k_verbify = Morpheme(k, aspects=[POSAspect(verb)])
_k_verbify_alt = copy(_k_verbify)
_k_verbify_alt.phoneme_cluster_association = k+a
_k_verbify_alt.link(_k_verbify)

flow_verb = copy(flow)+_k_verbify_alt
flow_verb.pos = verb
flow_verb.overridden_meaning = "flow"

to_be = _k_verbify+belong
to_be.overridden_meaning = "be"

_a_nounify = Morpheme(a, aspects=[POSAspect(noun)])

being = to_be+_a_nounify
being.overridden_meaning = "being"

mind = Word(
    Morpheme(p+a, aspects=[RootAspect("mind")]),
    part_of_speech=noun
)

person = _big+mind+being
person.overridden_meaning = "person"
person.pos = noun

life = being+flow
life.overridden_meaning = "life"

_end = Morpheme(v+u+l, aspects=[RootAspect("end")])
end = Word(_end)
end.pos = noun

to_end = go+end
to_end.overridden_meaning = "end"
to_end.pos = verb

to_end_continously = word_continue+end
to_end_continously.overridden_meaning = "be ending"
to_end_continously.pos = verb

aaran.add_words(
    water, river, water_adj,
    place, person,
    belong, go,
    word_continue, flow, flow_verb, to_be,
    being, life,
    end, to_end, to_end_continously
)


# TODO:
# 1. Phonotactic checks (partially working, problems with coda syllable splitting)
# 2. Head-first/Head-last (partially)
# 3. Word Order
# 4. Tonality

if __name__ == '__main__':
    aaran.compile(True)
    aaran.print_info()
    print("--------")
    for i in aaran.words:
        print("Word:", str(i))
        print("Meaning:", i.get_aprx_meaning())
        print("Original Phonology: ", i.trace_phonology())
        morph, POS = i.trace_meaning()
        print(f"Morpheme Substratum: {morph}; POS: {POS.pos if POS else i.pos if i.pos else ''}")
        print("Syllables:", '-'.join(map(str, i.syllabic_separator(aaran.phonotactics_binding))))
        print("--------")
