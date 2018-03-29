from .. import scaled_symbol
import math

class OneNNMarkov:
    def __init__(self, transformer, markov_degree = 1):
        self.transformer = transformer
        self.markov_degree = markov_degree
        self.previous = []
        self.transitions = {}
        
    def _get_transition_probability(self, label):
        def get_probability(prev_tuple, label):
            if prev_tuple in self.transitions:
                trans = self.transitions[prev_tuple]
                trans_sum = sum(trans.values())
                trans_count = trans[label] if label in trans else 0
                return trans_count / trans_sum    
            else:
                return 0
        
        return max( get_probability(tuple(self.previous[x:]), label) for x in range(len(self.previous)))
        
    def _get_closest(self, series, symbol_shift=0):
        normalized, _, _ = self.transformer.normalization.normalize(series)
        closest = None
        min_dist = float('inf')
        
        try:
            closest = min(
                filter(
                    lambda symbol: symbol.symbol_shift == symbol_shift, 
                    self.transformer.symbol_alphabet.symbols()
                    ), 
                key=lambda symbol: self.transformer.symbol_alphabet.distance_operator.distance(symbol.series, series) / (1+self._get_transition_probability(symbol.label))
                # key=lambda symbol: self.transformer.symbol_alphabet.distance_operator.distance(symbol.series, series) / (1+math.log(1+self._get_transition_probability(symbol.label)))
            )
            return closest
        except ValueError:
            return None
    
            
    def add(self, series, label):
        self.transformer.transform(series, label=label)
        
        self._add_transition(label)
        
        self.previous.append(label)
        if len(self.previous) > self.markov_degree:
            self.previous.pop(0)
            
            
    def _add_transition(self, label):
        prev_tuple = tuple(self.previous)
        if prev_tuple not in self.transitions:
            self.transitions[prev_tuple] = {}
        self.transitions[prev_tuple][label] = self.transitions[prev_tuple][label] + 1 if label in self.transitions[prev_tuple] else 1
        
    
        
    def classify(self, series, symbol_shift=0):
        closest = self._get_closest(series, symbol_shift)
        return closest.label if closest else None
        
        
    def word_end(self):
        self.previous = []