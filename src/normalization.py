import numpy as np

class Normalization:

    @classmethod
    def base_normalization(cls, series, shift, scale):
        """
        generic time series normalization
        :param series: time series
        :param shift: shift to normalize by
        :param scale: scale to normalize by
        :return: [normalized series, shift, scale]
        """
        return [(series - shift)/scale, shift, scale]

    def __init__(self):
        """
        the normalization object is used when we do not want to determine normalization coefficients for every
        time series, but rather to have common coefficients for multiple time series
        """
        self.normalize = self._normalize
        self.shift = 0
        self.scale = 1

    def set_coefficients(self, shift, scale):
        """
        set coefficients manually
        :param shift: shift
        :param scale: scale
        """
        self.shift = shift
        self.scale = scale

    def train_coefficients(self, series):
        """
        trains coefficients from time series
        :param series: time series
        """
        self.shift, self.scale = self.__class__.coefficients(series)

    def _normalize(self, series):
        """
        normalization using stored coefficients
        :param series: time series
        :return: [normalized series, shift, scale]
        """
        return self.__class__.base_normalization(series, self.shift, self.scale)

    @classmethod
    def coefficients(cls, series):
        """
        :param series: time series
        :return: [shift, scale]
        """
        return [0, 1]

    @classmethod
    def normalize(cls, series):
        """
        normalization with coefficient estimation
        :param series: time series
        :return: [normalized value, scale shift, scale multiple ]
        """
        shift, scale = cls.coefficients(series)
        return cls.base_normalization(series, shift, scale)

class ZNormalization(Normalization):

    @classmethod
    def coefficients(cls, series):
        """
        :param series: time series
        :return: [shift, scale]
        """
        mean_value = np.mean(series)
        std_value = np.std(series)
        return [mean_value, std_value]

class MaxNormalization(Normalization):

    @classmethod
    def coefficients(cls, series):
        """
        :param series: time series
        :return: [shift, scale]
        """
        min_value = np.min(series)
        max_value = np.max(series)
        return [min_value, max_value - min_value]
