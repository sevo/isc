from . import symbol_alphabet
from .. import symbol as s

class ForgettingAlphabet(symbol_alphabet.SymbolAlphabet):
    
    def __init__(self, distance_operator, limit_distance=0.0, counter_number=100):
        symbol_alphabet.SymbolAlphabet.__init__(self, distance_operator, limit_distance)
        self.distances = {}
        self.counter_number = counter_number
        self.counters = {}
    
    def size(self):
        """Returns size of the alphabet"""
        return len(self.counters)

    def symbols(self):
        """Returns a list of stored symbols"""
        return self.counters.keys()

    def distance(self, a, b):
        """Returns distacne between symbols"""
        if (a in self.distances and b in self.distances[a]):
            return self.distances[a][b]
        elif (b in self.distances and a in self.distances[b]):
            return self.distances[b][a]
        else:
            return None
            
    def _find_symbol(self, normalized, symbol_shift):
        """returns a tuple: (similar_symbol, closest_symbol). Similar symbol has distance < limit_distance, closest_symbol is the similar_symbol or has minimal distance among all symbols in alphabet"""
        for key_symbol in self.distances.keys():
            if key_symbol.symbol_shift == symbol_shift: 
                if  self.distance_operator.distance(key_symbol.series, normalized) < self.limit_distance:
                    return key_symbol
        return None
        
    def _add(self, normalized, symbol_shift, label=None):
        new_symbol = s.Symbol(normalized, symbol_shift=symbol_shift, label=label)
        self.counters[new_symbol] = 1
        
        new_distances = {new_symbol: 0.0}
        for other_symbol in self.distances.keys():
            new_distances[other_symbol] = self.distance_operator.distance(normalized, other_symbol.series)
        self.distances[new_symbol] = new_distances
        return new_symbol
        
    def _remove(self, symbol):
        """Removes a symbols from counters and from distance matrix"""
        self.counters.pop(symbol, None)
        
        for key_symbol, other_distances in self.distances.iteritems():
            other_distances.pop(symbol, None)
        self.distances.pop(symbol, None)
        
    def get_similar(self, normalized, symbol_shift, label=None):
        """Returns similar symbol from the alphabet"""
        similar_symbol = self._find_symbol(normalized, symbol_shift)
        if similar_symbol:
            self.counters[similar_symbol] = self.counters[similar_symbol] + 1
            return similar_symbol
        elif len(self.counters) < self.counter_number: # there is space in the alphabet, add the symbol then 
            return self._add(normalized, symbol_shift)
        else:
            # no match found, no room left, we have to lower counters and possibly delete items from alphabet
            symbol_list = self.counters.keys() 
            for key_symbol in symbol_list:
                self.counters[key_symbol] = self.counters[key_symbol] - 1
                if self.counters[key_symbol] <= 0:
                    self._remove(key_symbol)
            return None
            
    def get_closest(self, normalized, symbol_shift=0):
        try:
            return min(filter(lambda symbol: symbol.symbol_shift == symbol_shift, self.distances.keys()), key=lambda symbol: self.distance_operator.distance(symbol.series, series))
        except ValueError:
            return None
    
    