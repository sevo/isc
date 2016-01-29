import distance_matrix, euclidean_operator, symbol
import normalization as norm
import numpy as np

class IncrementalTransformer:
    def __init__(self, window_size, step_size, limit_distance,
                 normalization=norm.ZNormalization,
                 distance_operator=euclidean_operator.EuclideanOperator()):
        self.limit_distance = limit_distance
        self.window_size = window_size
        self.step_size = step_size
        self.distance_operator = distance_operator
        self.distance_matrix = distance_matrix.DistanceMatrix(distance_operator)
        self.normalization = normalization
        self.pattern_queue = [] # queue of started symbols
        self.counter = 0 # processed values counter

    def get_similar(self, series, symbol_shift=0):
        """
        Returns most similar symbol from the dictionary. If no symbol closer than limit_distance exists, it creates one
        :param series: symbol time series
        :return: most similar symbol from the dictionary or new one
        """
        normalized, scale_shift, scale_multiple = self.normalization.normalize(series)
        for key_symbol in self.distance_matrix.distances.keys():
            if key_symbol.symbol_shift == symbol_shift and self.distance_operator.distance(key_symbol.series, normalized) < self.limit_distance:
                new_symbol = symbol.Symbol(key_symbol.series, scale_shift, scale_multiple, key_symbol.id, key_symbol.symbol_shift)
                return new_symbol
        new_symbol = symbol.Symbol(normalized, scale_shift, scale_multiple, symbol_shift=symbol_shift)
        self.distance_matrix.add(new_symbol)
        return new_symbol

    def add(self, point):
        """
        Adds one point to the transformed time series.
        :param point: one time series point
        :return: new symbol if the added point finishes started symbol or None if not
        """
        if self.counter % self.step_size == 0:
            self.pattern_queue.append([])

        for pattern in self.pattern_queue:
            pattern.append(point)

        self.counter += 1

        if (self.counter - self.window_size) >= 0 and (self.counter - self.window_size) % self.step_size == 0:
            symbol_shift = (self.counter % self.window_size) / self.step_size
            pattern = self.pattern_queue.pop(0)
            return self.get_similar(pattern, symbol_shift)
        else:
            return None

    def transform(self, whole_series):
        """
        transforms whole time series into symbols. It builds on previously transformed time series
        :param whole_series: time series
        :return: array of new symbols
        """
        symbol_series = []

        for point in whole_series:
            new_symbol = self.add(point)
            if new_symbol is not None:
                symbol_series.append(new_symbol)

        return symbol_series

    def reconstruct(self, symbols):
        result = np.array([])
        for symbol in symbols:
            result = np.concatenate((result, symbol.denormalized_series()))
        return result

