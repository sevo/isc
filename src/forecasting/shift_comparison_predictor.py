import pdb

class ShiftComparisonPredictor:
    def __init__(self, transformer):
        self.transformer = transformer

    def _search_part(self, part, symbol_shift):
        # todo, obavam sa, ze tie patterny niesu normalizovane a ja sa snazim porovnavat normalizovany casovy rad s nenormalizovanym
        # todo teraz som tu narychlo pridal normalizaciu, ale nejak chybne, kedze mi to porovnava ako keby pole. Treba overit ake typy mi to vracia a ci to mozem priamo hodit do distance operatora
        min_dist = float("inf")
        norm_part, part_shift, part_multiple = self.transformer.normalization.normalize(part)
        search_result = None
        for key_symbol in self.transformer.symbol_alphabet.distances.keys():
            if key_symbol.symbol_shift == symbol_shift:
                dist = self.transformer.distance_operator.distance(key_symbol.series[0:(len(norm_part))], norm_part)
                if dist < min_dist:
                    min_dist = dist
                    search_result = key_symbol
        # pdb.set_trace()
        return search_result

    def predict(self, pattern_order=0):
        """
        Predicts normalized shape of the time series. It still has to be denormalized to be used
        :param pattern_order: which pattern should we use for prediction 0 for first, 1 for second, ...
        :return: sequence of values in the symbol as Panadas series
        """
        if len(self.transformer.pattern_queue) > pattern_order:
            symbol_part = self.transformer.pattern_queue[pattern_order]
            symbol_shift = ((self.transformer.counter - (self.transformer.window_size - self.transformer.step_size)) % self.transformer.window_size) / self.transformer.step_size
            # symbol_shift = ((self.transformer.counter) % self.transformer.window_size) / self.transformer.step_size
            return self._search_part(symbol_part, symbol_shift)
        else:
            return None