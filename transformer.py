from .alphabet import distance_matrix
from . import euclidean_operator, scaled_symbol
from . import normalization as norm

class Transformer:
    def __init__(self, window_size, step_size, limit_distance,
                 normalization=norm.ZNormalization,
                 distance_operator=euclidean_operator.EuclideanOperator(), symbol_alphabet=None):
        """
        :param window_size: symbol length
        :param step_size: step between two symbols
        :param limit_distance: limit distance of symbol time series from the cluster centre
        :param normalization: normalization
        :param distance_operator: distance operator used for symbol comparison
        :return:
        """
        self.limit_distance = limit_distance
        self.window_size = window_size
        self.step_size = step_size
        self.distance_operator = distance_operator
        self.symbol_alphabet = symbol_alphabet or distance_matrix.DistanceMatrix(distance_operator, limit_distance)
        self.normalization = normalization
        self.pattern_queue = []

    def get_similar(self, series, symbol_shift=0):
        """
        Returns most similar symbol from the dictionary. If no symbol closer than limit_distance exists, it creates one
        :param series: symbol time series
        :return: most similar symbol from the dictionary or new one
        """
        normalized, scale_shift, scale_multiple = self.normalization.normalize(series)
        unscaled_symbol = self.symbol_alphabet.get_similar(normalized, symbol_shift)
        if unscaled_symbol:
            return scaled_symbol.ScaledSymbol(unscaled_symbol, scale_shift, scale_multiple)
        else:
            return None

    def transform(self, whole_series):
        """
        transforms time series into sequence of symbols
        :param whole_series: time series to be transformed
        :return: symbol sequence
        """
        symbol_series = []
        self.pattern_queue = [] # pattern_queue.pop(0) # removes and returns first element

        self.counter = 0
        for point in whole_series:
            if self.counter % self.step_size == 0:
                self.pattern_queue.append([])

            for pattern in self.pattern_queue:
                pattern.append(point)

            self.counter += 1

            if (self.counter - self.window_size) >= 0 and (self.counter - self.window_size) % self.step_size == 0:
                symbol_shift = (self.counter % self.window_size) / self.step_size
                pattern = self.pattern_queue.pop(0)
                symbol_series.append(self.get_similar(pattern, symbol_shift))

        return symbol_series