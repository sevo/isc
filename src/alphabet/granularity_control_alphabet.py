import symbol_alphabet
import symbol as s
from collections import OrderedDict
import operator

class LastUpdatedOrderedDict(OrderedDict):
    """Store items in the order the keys were last added"""
    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)

class GranularityAlphabet():
    def __init__(self, distance_operator, limit_distance=0.0, counter_number=100):
        self.distance_operator = distance_operator
        self.limit_distance = limit_distance
        self.counter_number = counter_number
        self.counters = {}
    
    def _find_symbol(self, normalized, symbol_shift):
        """returns a tuple: (similar_symbol, closest_symbol). Similar symbol has distance < limit_distance, closest_symbol is the similar_symbol or has minimal distance among all symbols in alphabet"""
        for key_symbol in self.counters.keys():
            if key_symbol.symbol_shift == symbol_shift: 
                actual_distance = self.distance_operator.distance(key_symbol.series, normalized)
                if  actual_distance < self.limit_distance:
                    return key_symbol
        return None
    
    def _add(self, normalized, symbol_shift):
        new_symbol = s.Symbol(normalized, symbol_shift=symbol_shift)
        self.counters[new_symbol] = 1
        return new_symbol
    
    def add_ascended(self, symbol, count):
        """
        Add symol from coarser alphabet to freed place.
        This method can be called only if symbols were removed from the alphabet and we want to replace them by the most frequent from coarser granularity alphabet
        """
        self.counters[symbol] = count
        
    def remove(self, symbol):
        """Removes a symbols from counters and from distance matrix"""
        """Can be called from get_similar method of this alphabet or when ascending symbol to finer alphabet"""
        return self.counters.pop(symbol, None)
        
    def get_similar(self, normalized, symbol_shift):
        """Returns a quadruplet, (similar symbol from the alphabet, closest symbol, distance of the closest symbol list of symbols removed from the alphabet)"""
        # todo, treba porozmyslat, ci sa nema znizovat pocetnost inym cislom ako 1. Podla mna to ale teraz nieje potrebne
        similar_symbol = self._find_symbol(normalized, symbol_shift)
        if similar_symbol:
            self.counters[similar_symbol] = self.counters[similar_symbol] + 1
            return (similar_symbol, [])
        elif len(self.counters) < self.counter_number: # there is space in the alphabet, add the symbol then 
            return (self._add(normalized, symbol_shift), [])
        else:
            # no match found, no room left, we have to lower counters and possibly delete items from alphabet
            symbol_list = self.counters.keys() 
            removed = []
            for key_symbol in symbol_list:
                self.counters[key_symbol] = self.counters[key_symbol] - 1
                if self.counters[key_symbol] <= 0:
                    self.remove(key_symbol)
                    removed.append(key_symbol)
            return (None, removed)

class GranularityControlAlphabet(symbol_alphabet.SymbolAlphabet):

    def __init__(self, distance_operator, limit_distance=[1.0, 2.0], counter_number=[100,100]):
        """limit_distance and counter_number are lists of attributes of multiple granularity alphabets ordered from finer to coarser granularity"""
        symbol_alphabet.SymbolAlphabet.__init__(self, distance_operator, limit_distance)
        self.distances = LastUpdatedOrderedDict()
        self.distance_cache_size = 1000
        # alphabets ordered from finer to coarser granularity
        self.alphabets = [GranularityAlphabet(distance_operator, limit_distance=limit_distance[i], counter_number=counter_number[i]) for i in range(len(limit_distance))]
    
    def size(self):
        """Returns size of the alphabet"""
        return sum([len(alphabet.counters) for alphabet in self.alphabets])

    def symbols(self):
        """Returns a list of stored symbols"""
        return reduce(lambda x, y: x+y, [alphabet.counters.keys() for alphabet in self.alphabets])

    def distance(self, a, b):
        """Returns distacne between symbols"""
        if (a,b) in self.distances:
            return self.distances[(a,b)]
        elif (b,a) in self.distances:
            return self.distances[(b,a)]
        else:
            if len(self.distances > self.distance_cache_size): #if the cache is full, delete half the cashed distances
                keys_to_remove = self.distances.keys()[:(len(self.distances)/2)]
                for key in keys_to_remove:
                    self.distances.pop(key, None)
            self.distances[(a,b)] = self.distance_operator.distance(a.series, b.series)
            return self.distances[(a,b)]
        
    def get_similar(self, normalized, symbol_shift):
        """Returns similar symbol from the alphabet"""
        
        old_removed = []
        previous_alphabet = None
        for alphabet in self.alphabets:
            similar_symbol, removed = alphabet.get_similar(normalized, symbol_shift)
            if old_removed:
                sorted_counters = sorted(alphabet.counters.items(), key=operator.itemgetter(1), reverse=True)
                for i in range(len(old_removed)):
                    new_count_value = 1
                    if i < len(sorted_counters): # to be sure that we have enough symbols in coarser alphabet to be moved to the finer one
                        counter = sorted_counters[i]
                        new_count_value = counter[1] / 2
                        alphabet.remove(counter[0])
                        previous_alphabet.add_ascended(counter[0], new_count_value)
                    alphabet.add_ascended(old_removed[i], new_count_value) # add_ascended is a little bad name as this symbol is in fact descending #cize ten povodny pocet si rozdelia. alebo by tu skor mala byt hodnota 1. To by sa ale mohlo velmi lahko stat, ze nieco prejde z tej najfrekventovnejsej skupiny uplne prec
            old_removed, previous_alphabet = removed, alphabet
            
            if similar_symbol: 
                return similar_symbol
                
        return None
            
            
    # pohladaj symbol v abecede. Ak tam je, tak zvys counter
    # ak tam nieje, tak zniz vsetky countre a priprav sa na presuvanie
    # chod na dalsiu abecedu, pohladaj symbol, ak je, tak zvys counter a ak nie, tak zniz countre a priprav sa na mozne presuvanie
    
    # ak z vyzsej abecedy prisli nejake odstranene symboly, tak sa do tejto abecedy da rovnaky pocet vlozit, pretoze sa im uvolnilo miesto. 
    # To znamena, ze sa vymenia za tie najfrekventovanejsie z tejto abecedy.
    # pri pripajani do vyzsej abecedy pouzivaj povodne county
    