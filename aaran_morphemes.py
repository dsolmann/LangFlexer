from aaran_phonology import a_high, a_low, e, r, n, t, a, v, u, l
from models.grammar.morphology import Morpheme
from models.grammar.morphology.aspects import RootAspect
from aaran_grammar import _go_verbify

_water = Morpheme(a_high + a_low, aspects=[RootAspect("water")])
_place = Morpheme(e + r + e, aspects=[RootAspect("place")])
_place_alt = Morpheme(r + e, aspects=[RootAspect("place")])
_belong = Morpheme(a_high + n, aspects=[RootAspect("belong")])
_go = Morpheme(t + a, aspects=[RootAspect("go")])
_long = Morpheme(n + a, aspects=[RootAspect("long")])
_big = Morpheme(n + a, aspects=[RootAspect("big")])
_end = Morpheme(v + u + l, aspects=[RootAspect("end")])

_place_alt.link(_place)
_go.link(_go_verbify)
_long.link(_big)

