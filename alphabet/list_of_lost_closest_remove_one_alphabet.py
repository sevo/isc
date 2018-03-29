from . import symbol_alphabet
from .. import symbol as s
from collections import OrderedDict
from operator import itemgetter

class ListOfLostAlphabet(symbol_alphabet.SymbolAlphabet):
    """
    ListOfLost approach returning closest symbol if no space is left for new symbols and removing only one symbol if the alphabet is full. 
    This caused, that counters can go to negative numbers, but should ease the problem of removing very young symbols before they have time to grow.
    
    However, I have to store the order of symbols as they came.
    """
    
    def __init__(self, distance_operator, limit_distance=0.0, counter_number=100):
        symbol_alphabet.SymbolAlphabet.__init__(self, distance_operator, limit_distance)
        self.distances = {}
        self.counter_number = counter_number
        self.counters = OrderedDict()
    
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
            
    def match(self, symbol):
        """Returns True if symbol is in alphabet else False"""
        if symbol in self.symbols():
            return symbol
        for test_symbol in self.symbols():
            if symbol.id in test_symbol.list_of_lost:
                return test_symbol
        return None
            
    def _find_symbol(self, normalized, symbol_shift):
        """returns a tuple: (similar_symbol, closest_symbol). Similar symbol has distance < limit_distance, closest_symbol is the similar_symbol or has minimal distance among all symbols in alphabet"""
        closest = None
        min_distance = float('inf')
        for key_symbol in self.distances.keys():
            if key_symbol.symbol_shift == symbol_shift: 
                actual_distance = self.distance_operator.distance(key_symbol.series, normalized)
                if actual_distance < min_distance:
                    closest = key_symbol
                    min_distance = actual_distance
                if  actual_distance < self.limit_distance:
                    return (key_symbol, closest)
        return (None, closest)
        
    def _add(self, normalized, symbol_shift ,label=None):
        new_symbol = s.ListOfLostSymbol(normalized, symbol_shift=symbol_shift, label=label)
        self.counters[new_symbol] = 1
        
        new_distances = {new_symbol: 0.0}
        for other_symbol in self.distances.keys():
            new_distances[other_symbol] = self.distance_operator.distance(normalized, other_symbol.series)
        self.distances[new_symbol] = new_distances
        return new_symbol
        
    def _remove(self, symbol):
        """Removes a symbols from counters and from distance matrix"""
        # todo, treba dorobit aby sa spajali zahodene symboli k najpodobnejsiemu z abecedy
        self.counters.pop(symbol, None)
        
        min_dist = float('inf')
        closest_symbol = None
        for key_symbol, other_distances in self.distances.iteritems():
            if symbol.label == key_symbol.label and symbol.symbol_shift == key_symbol.symbol_shift and symbol in other_distances and other_distances[symbol] < min_dist:
                min_dist = other_distances[symbol]
                closest_symbol = key_symbol
        closest_symbol.swallow(symbol)
        
        for _, other_distances in self.distances.iteritems():
            other_distances.pop(symbol, None)
        self.distances.pop(symbol, None)
        
    def get_similar(self, normalized, symbol_shift, label=None):
        """Returns similar symbol from the alphabet"""
        similar_symbol, closest_symbol = self._find_symbol(normalized, symbol_shift)
        if similar_symbol:
            self.counters[similar_symbol] = self.counters[similar_symbol] + 1
            return similar_symbol
        elif len(self.counters) == self.counter_number:
            # no match found, no room left, we have to lower counters and possibly delete item from alphabet
            for key_symbol in self.counters.keys(): # no symbols are removed, they are only decremented
                self.counters[key_symbol] = self.counters[key_symbol] - 1
                
            least_frequent = sorted(self.counters.iteritems(), key=itemgetter(1)) # self.counters is ordered by the time they first came and sorted is stable sorting. sorted list then shows the least frequent item and if there are more like this one, then the oldest is the first one
            if(len(least_frequent) > 0 and least_frequent[0][1] <= 0):
                self._remove(least_frequent[0][0])
        if len(self.counters) < self.counter_number: # there is space in the alphabet, add the symbol then 
            return self._add(normalized, symbol_shift, label)
        else: # nothing helped, return closest
            return closest_symbol
    
    def get_closest(self, normalized, symbol_shift=0):
        try:
            return min(filter(lambda symbol: symbol.symbol_shift == symbol_shift, self.counters.keys()), key=lambda symbol: self.distance_operator.distance(symbol.series, series))
        except ValueError:
            return None