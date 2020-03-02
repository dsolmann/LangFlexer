from aaran_base import belong, go, flow, word_continue, flow_verb, to_be, being, person, life, end, to_end, \
    to_end_continously

from aaran_nature import water, place, river, river_alt, water_adj
from aaran_phonology import typical_syllable
from models.grammar.language import Language

# =========== A:Ra Lang  ========== #

aaran = Language("Aaran")
aaran.set_syllable_structure(typical_syllable)
aaran.add_words(
    water, river, water_adj, river_alt,
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

    for i in aaran.words:
        print(i.get_aprx_meaning(), "-", str(i))

    for i in aaran.morphemes:
        print(*map(str, i.aspects), "-", str(i))
    print("-----")
    for i in aaran.words:
        print(i.trace_meaning()[0], i.get_aprx_meaning(), str(i), sep="\t")
