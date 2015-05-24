import numpy as np

class ZNormalization:

    # returns [normalized value, scale shift, scale multiple ]
    @classmethod
    def normalize(cls, series):
        mean_value = np.mean(series)
        std_value = np.std(series)
        return [(series - mean_value) / std_value, mean_value, std_value]

class MaxNormalization:

    # returns [normalized value, scale shift, scale multiple ]
    @classmethod
    def normalize(cls, series):
        min_value = np.min(series)
        max_value = np.max(series)
        return [(series - min_value) / (max_value - min_value), min_value, max_value-min_value]
