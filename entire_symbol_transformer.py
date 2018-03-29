from .alphabet import distance_matrix
from . import euclidean_operator, scaled_symbol
from . import normalization as norm

class EntireSymbolTransformer:
    def __init__(self, limit_distance,
                 normalization=norm.NoNormalization,
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
        self.distance_operator = distance_operator
        self.symbol_alphabet = symbol_alphabet or distance_matrix.DistanceMatrix(distance_operator, limit_distance)
        self.normalization = normalization

    def get_similar(self, series, symbol_shift=0, label=None):
        """
        Returns most similar symbol from the dictionary. If no symbol closer than limit_distance exists, it creates one
        :param series: symbol time series
        :return: most similar symbol from the dictionary or new one
        """
        normalized, scale_shift, scale_multiple = self.normalization.normalize(series)
        unscaled_symbol = self.symbol_alphabet.get_similar(normalized, symbol_shift, label)
        if unscaled_symbol:
            return scaled_symbol.ScaledSymbol(unscaled_symbol, scale_shift, scale_multiple)
        else:
            return None

    def transform(self, series, symbol_shift=0, label=None):
        """
        transforms one symbol worth of time series into a symbol
        :param series: time series to be transformed
        :return: symbol
        """

        return self.get_similar(series, symbol_shift, label)