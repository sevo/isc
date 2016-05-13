class SimpleComparisonPredictor:
    def __init__(self, transformer):
        self.transformer = transformer

    def _search_part(self, part):
        min_dist = float("inf")
        search_result = None
        for key_symbol in self.transformer.symbol_alphabet.distances.keys():
            dist = self.transformer.distance_operator.distance(key_symbol.series[0:(len(part))], part)
            if dist < min_dist:
                min_dist = dist
                search_result = key_symbol
        return search_result

    def predict(self, pattern_order=0):
        """
        Predicts normalized shape of the time series. It still has to be denormalized to be used
        :param pattern_order: which pattern should we use for prediction 0 for first, 1 for second, ...
        :return: sequence of values in the symbol as Panadas series
        """
        if len(self.transformer.pattern_queue) > pattern_order:
            symbol_part = self.transformer.pattern_queue[pattern_order]
            return self._search_part(symbol_part)
        else:
            return None