class Symbol:
    max_index = 0

    @classmethod
    def next_index(cls):
        cls.max_index = cls.max_index+1
        return cls.max_index

    def __init__(self, series, scale_shift=None, scale_multiple=None, id=None, symbol_shift=None):
        self.series = series
        self.id = id or self.__class__.next_index()
        self.scale_shift = scale_shift or 0
        self.scale_multiple = scale_multiple or 1
        self.symbol_shift = symbol_shift

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def normalize(self, normalization_class):
        if(self.scale_multiple == 1 and self.scale_shift == 0):
            self.series, self.scale_shift, self.scale_multiple = normalization_class.normalize(self.series)

    def denormalized_series(self):
        return (self.series * self.scale_multiple) + self.scale_shift