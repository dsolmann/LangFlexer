from models.grammar.morphology import PartOfSpeech


class MorphologicalAspect:
    name: str
    short_doc: str

    def __init__(self, name, short_doc=""):
        self.name = name
        self.short_doc = short_doc


class RootAspect(MorphologicalAspect):
    long_doc: str

    def __init__(self, short_doc, long_doc=""):
        super().__init__("Root", short_doc)
        self.long_doc = long_doc


class POSAspect(MorphologicalAspect):
    pos: PartOfSpeech

    def __init__(self, pos):
        self.pos = pos
        super().__init__("POSer", self.pos.name)