from incremental_transformer import IncrementalTransformer
import numpy as np

# todo, objekt, ktory bude pouzivat transofrmer na to aby na zaklade neho spocital predikciu
# mozno na toto nebude treba samostatnu triedu, ale bude to sucast transformera, pripadne ako nejaky mixin. V pythone funguje multiple inheritance
# todo, bude treba pridat metody na vyhodnocovanie chyby predikcie
# todo, na zaciatku to mozem napasovat na energodata a potom zovseobecnit
# todo, vzdy po tizdny treba updatovat koeficienty normalizacie aby sa odstranili sezonne vplyvy vacsie ako 1 tyzden

class Predictor:
    def __init__(self, transformer):
        self.transformer = transformer

    def _search_part(self, part):
        min_dist = float("inf")
        search_result = None
        for key_symbol in self.transformer.distance_matrix.distances.keys():
            dist = self.transformer.distance_operator.distance(key_symbol.series[0:(len(part))], part)
            if dist < min_dist:
                min_dist = dist
                search_result = key_symbol.series
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