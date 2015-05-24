import distance_matrix, euclidean_operator, symbol
import normalization as norm

class Tranformer:
    def __init__(self, window_size, step_size, limit_distance,
                 normalization=norm.ZNormalization,
                 distance_operator=euclidean_operator.EuclideanOperator()):
        self.limit_distance = limit_distance
        self.window_size = window_size
        self.step_size = step_size
        self.distance_operator = distance_operator
        self.distance_matrix = distance_matrix.DistanceMatrix(distance_operator)
        self.normalization = normalization

    # obtains sequence of values and returns the closest symbol. If no such symbol exists, creates new one
    def get_similar(self, series):
        normalized, scale_shift, scale_multiple = self.normalization.normalize(series)
        for key_symbol in self.distance_matrix.distances.keys():
            if self.distance_operator.distance(key_symbol.series, normalized) < self.limit_distance:
                new_symbol = symbol.Symbol(normalized, scale_shift, scale_multiple, key_symbol.id)
                return new_symbol
        new_symbol = symbol.Symbol(normalized, scale_shift, scale_multiple)
        self.distance_matrix.add(new_symbol)
        return new_symbol

    def transform(self, whole_series):
        symbol_series = []
        pattern_queue = [] # pattern_queue.pop(0) # removes and returns first element

        counter = 0
        for point in whole_series:
            if counter % self.step_size == 0:
                pattern_queue.append([])

            for pattern in pattern_queue:
                pattern.append(point)

            counter += 1

            if (counter - self.window_size) >= 0 and (counter - self.window_size) % self.step_size == 0:
                pattern = pattern_queue.pop(0)
                symbol_series.append(self.get_similar(pattern))

        return symbol_series