from aaran_grammar import noun, adj
from aaran_phonology import a_high, a_low, r
from aaran_morphemes import _water, _place, _place_alt
from models.grammar.morphology import Word

water = Word(_water, part_of_speech=noun)
place = Word(_place)

river = water + _place_alt
river.overridden_meaning = "river"

river_alt = water + _place_alt
river_alt.overridden_meaning = "river"

river_alt.overridden_spelling = a_high + a_low + r
river.link_alter(river_alt)

water_adj = water + adj
