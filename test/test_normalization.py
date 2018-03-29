import normalization
import numpy as np

def test_z_normalization():
    series = np.array([3, 4, 5])
    normalized, scale_shift, scale_multiple = normalization.ZNormalization.normalize(series)
    assert all(normalized == np.array([-1.2247448713915889, 0, 1.2247448713915889]))
    assert scale_shift == 4
    assert scale_multiple == 0.81649658092772603

def test_max_normalization():
    series = np.array([3, 4, 5])
    normalized, scale_shift, scale_multiple = normalization.MaxNormalization.normalize(series)
    assert all(normalized == np.array([0, 0.5, 1]))
    assert scale_shift == 3
    assert scale_multiple == 2

def test_instance_z_normalization():
    series = np.array([3, 4, 5])
    norm = normalization.ZNormalization()
    norm.train_coefficients(series)
    normalized, scale_shift, scale_multiple = norm.normalize(series)
    assert all(normalized == np.array([-1.2247448713915889, 0, 1.2247448713915889]))
    assert scale_shift == 4
    assert scale_multiple == 0.81649658092772603

def test_instance_max_normalization():
    series = np.array([3, 4, 5])
    norm = normalization.MaxNormalization()
    norm.train_coefficients(series)
    normalized, scale_shift, scale_multiple = norm.normalize(series)
    assert all(normalized == np.array([0, 0.5, 1]))
    assert scale_shift == 3
    assert scale_multiple == 2
