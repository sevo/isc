from .. import scaled_symbol

class OneNN:
    def __init__(self, transformer):
        self.transformer = transformer
        
    def _get_closest(self, series, symbol_shift=0):
        normalized, _, _ = self.transformer.normalization.normalize(series)
        closest = self.transformer.symbol_alphabet.get_closest(normalized, symbol_shift)
        return closest
    
            
    def add(self, series, label):
        self.transformer.transform(series, label=label)
    
        
    def classify(self, series, symbol_shift=0):
        closest = self._get_closest(series, symbol_shift)
        return closest.label if closest else None
        
    def word_end(self):
        pass