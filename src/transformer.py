import distance_matrix, euclidean_operator, symbol
import normalization as norm

class Transformer:
    def __init__(self, window_size, step_size, limit_distance,
                 normalization=norm.ZNormalization,
                 distance_operator=euclidean_operator.EuclideanOperator()):
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
        self.distance_matrix = distance_matrix.DistanceMatrix(distance_operator)
        self.normalization = normalization
        self.pattern_queue = []

    def get_similar(self, series):
        """
        Returns most similar symbol from the dictionary. If no symbol closer than limit_distance exists, it creates one
        :param series: symbol time series
        :return: most similar symbol from the dictionary or new one
        """
        normalized, scale_shift, scale_multiple = self.normalization.normalize(series)
        for key_symbol in self.distance_matrix.distances.keys():
            if self.distance_operator.distance(key_symbol.series, normalized) < self.limit_distance:
                new_symbol = symbol.Symbol(normalized, scale_shift, scale_multiple, key_symbol.id)
                return new_symbol
        new_symbol = symbol.Symbol(normalized, scale_shift, scale_multiple)
        self.distance_matrix.add(new_symbol)
        return new_symbol

    def transform(self, whole_series):
        """
        transforms time series into sequence of symbols
        :param whole_series: time series to be transformed
        :return: symbol sequence
        """
        symbol_series = []
        self.pattern_queue = [] # pattern_queue.pop(0) # removes and returns first element

        counter = 0
        for point in whole_series:
            if counter % self.step_size == 0:
                self.pattern_queue.append([])

            for pattern in self.pattern_queue:
                pattern.append(point)

            counter += 1

            if (counter - self.window_size) >= 0 and (counter - self.window_size) % self.step_size == 0:
                pattern = self.pattern_queue.pop(0)
                symbol_series.append(self.get_similar(pattern))

        return symbol_series