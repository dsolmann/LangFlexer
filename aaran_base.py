from copy import copy

from aaran_grammar import verb, _go_verbify, _k_verbify_alt, _k_verbify, _a_nounify, noun
from aaran_morphemes import _belong, _go, _long, _big, _end
from aaran_phonology import p, a
from models.grammar.morphology import Word, Morpheme
from models.grammar.morphology.aspects import RootAspect

belong = Word(_belong, part_of_speech=verb)

go = Word(_go, part_of_speech=verb)

flow = Word(_go, _long)
flow.overridden_meaning = "flow"
flow.pos = noun

word_continue = flow + _go_verbify
word_continue.overridden_meaning = "continue"

flow_verb = copy(flow) + _k_verbify_alt
flow_verb.pos = verb
flow_verb.overridden_meaning = "flow"

to_be = _k_verbify + belong
to_be.overridden_meaning = "be"

being = to_be + _a_nounify
being.overridden_meaning = "being"

mind = Word(
    Morpheme(p + a, aspects=[RootAspect("mind")]),
    part_of_speech=noun
)

person = _big + mind + being
person.overridden_meaning = "person"
person.pos = noun

life = being+flow
life.overridden_meaning = "life"


end = Word(_end)
end.pos = noun

to_end = go+end
to_end.overridden_meaning = "end"
to_end.pos = verb

to_end_continously = word_continue+end
to_end_continously.overridden_meaning = "be ending"
to_end_continously.pos = verb
