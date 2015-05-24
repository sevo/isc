import pandas as pd
import numpy as np
from ..src import euclidean_operator

def test_operator():
    operator = euclidean_operator.EuclideanOperator()
    series1 = pd.Series([1.0, 0.5, 1.0, 0.5])
    series2 = pd.Series([1.0, 1.0, 1.0, 1.0])
    assert operator.distance(series1, series2) == np.sqrt(0.5)
