from ..src import symbol
from ..src import normalization
import pandas as pd
import copy

class TestEquivalence:
    def test_difference(self):
        sym1 = symbol.Symbol(pd.Series([1,2]))
        sym2 = symbol.Symbol(pd.Series([1,2]))
        assert (sym1 == sym2) == False

    def test_equivalence(self):
        sym1 = symbol.Symbol(pd.Series([1,2]))
        sym2 = copy.copy(sym1)
        assert (sym1 == sym2) == True

    def test_equivalence_using_fake_id(self):
        sym1 = symbol.Symbol(pd.Series([1,2]))
        sym2 = symbol.Symbol(pd.Series([1,2]))
        sym2.id = sym1.id
        assert (sym1 == sym2) == True


class TestNormalization:
    def test_normalization(self):
        sym = symbol.Symbol(pd.Series([3, 4, 5]))
        sym.normalize(normalization.MaxNormalization)
        assert sym.scale_multiple == 2
        assert sym.scale_shift == 3
        assert sym.series.equals(pd.Series([0, 0.5, 1]))

    def test_denormalization(self):
        sym = symbol.Symbol(pd.Series([3, 4, 5]))
        sym.normalize(normalization.MaxNormalization)
        result = sym.denormalized_series()
        assert result.equals(pd.Series([3.0, 4.0, 5.0]))
