import sys
sys.path.append("..")

from . import symbol_alphabet
import symbol

class DistanceMatrix(symbol_alphabet.SymbolAlphabet):
    def __init__(self, distance_operator, limit_distance=0.0):
        symbol_alphabet.SymbolAlphabet.__init__(self, distance_operator, limit_distance)
        self.distances = {}

    def size(self):
        return len(self.distances)

    def symbols(self):
        return self.distances.keys()

    def _add(self, symbol):
        new_distances = {symbol: 0.0}
        for other_symbol in self.distances.keys():
            new_distances[other_symbol] = self.distance_operator.distance(symbol.series, other_symbol.series)
        self.distances[symbol] = new_distances

    def distance(self, a, b):
        if (a in self.distances and b in self.distances[a]):
            return self.distances[a][b]
        elif (b in self.distances and a in self.distances[b]):
            return self.distances[b][a]
        else:
            return None
            
            
    def get_similar(self, normalized, symbol_shift, label=None):
        for key_symbol in self.distances.keys():
            if key_symbol.symbol_shift == symbol_shift and self.distance_operator.distance(key_symbol.series, normalized) < self.limit_distance:
                new_symbol = symbol.Symbol(key_symbol.series, key_symbol.id, key_symbol.symbol_shift, label=key_symbol.label)
                return new_symbol
        new_symbol = symbol.Symbol(normalized, symbol_shift=symbol_shift, label=label)
        self._add(new_symbol)
        return new_symbol
        
    def get_closest(self, series, symbol_shift=0):
        # closest = None
        # min_dist = float('inf')
        # for symbol in filter(lambda symbol: symbol.symbol_shift == symbol_shift, self.distances.keys()):
        #     new_dist = self.distance_operator.distance(symbol.series, series)
        #     if new_dist < min_dist:
        #         min_dist = new_dist
        #         closest = symbol
        # return closest
        
        try:
            return min(filter(lambda symbol: symbol.symbol_shift == symbol_shift, self.distances.keys()), key=lambda symbol: self.distance_operator.distance(symbol.series, series))
        except ValueError:
            return None


