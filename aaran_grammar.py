from copy import copy
from models.grammar.morphology.aspects import POSAspect
from aaran_phonology import t, a, k, l, a_low, o
from models.grammar.morphology import PartOfSpeech, Morpheme

# ============= Grammar ============= #
verb = PartOfSpeech("VERB")
noun = PartOfSpeech("NOUN")
adjective = PartOfSpeech("ADJ")

# ========== GRM Morphemes ========== #

_go_verbify = Morpheme(t + a, aspects=[POSAspect(verb)])
_k_verbify = Morpheme(k, aspects=[POSAspect(verb)])

_k_verbify_alt = copy(_k_verbify)
_k_verbify_alt.phoneme_cluster_association = k + a
_k_verbify_alt.link(_k_verbify)

_a_nounify = Morpheme(a, aspects=[POSAspect(noun)])
adj = Morpheme(l + a_low + o, aspects=[POSAspect(adjective)])
