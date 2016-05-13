class ScaledSymbol:
    def __init__(self, unscaled_symbol, scale_shift=None, scale_multiple=None):
        self.unscaled = unscaled_symbol
        self.scale_shift = scale_shift or 0
        self.scale_multiple = scale_multiple or 1
        
    # def normalize(self, normalization_class):
    #     if(self.scale_multiple == 1 and self.scale_shift == 0):
    #         self.series, self.scale_shift, self.scale_multiple = normalization_class.normalize(self.unscaled.series)

    def denormalized_series(self):
        return self.denormalize(self.unscaled.series)
        
    def denormalize(self, series):
        return (series * self.scale_multiple) + self.scale_shift