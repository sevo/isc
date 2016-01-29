class Symbol:
    max_index = 0

    @classmethod
    def next_index(cls):
        cls.max_index = cls.max_index+1
        return cls.max_index

    def __init__(self, series, id=None, symbol_shift=None):
        self.series = series
        self.id = id or self.__class__.next_index()
        self.symbol_shift = symbol_shift

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
