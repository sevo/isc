from ..src import normalization
import pandas as pd

def test_z_normalization():
    series = pd.Series([3, 4, 5])
    normalized, scale_shift, scale_multiple = normalization.ZNormalization.normalize(series)
    assert normalized.equals(pd.Series([-1.2247448713915889, 0, 1.2247448713915889]))
    assert scale_shift == 4
    assert scale_multiple == 0.81649658092772603

def test_max_normalization():
    series = pd.Series([3, 4, 5])
    normalized, scale_shift, scale_multiple = normalization.MaxNormalization.normalize(series)
    assert normalized.equals(pd.Series([0, 0.5, 1]))
    assert scale_shift == 3
    assert scale_multiple == 2