from ..src import distance_matrix, symbol, euclidean_operator
import pandas as pd

class TestDistanceMatrix:
    def test_add_same(self):
        operator = euclidean_operator.EuclideanOperator()
        matrix = distance_matrix.DistanceMatrix(operator)
        sym1 = symbol.Symbol(pd.Series([1, 0]))
        sym2 = symbol.Symbol(pd.Series([1, 0]))
        matrix.add(sym1)
        matrix.add(sym2)
        assert matrix.distance(sym1, sym2) == 0.0

    def test_add(self):
        operator = euclidean_operator.EuclideanOperator()
        matrix = distance_matrix.DistanceMatrix(operator)
        sym1 = symbol.Symbol(pd.Series([1, 0]))
        sym2 = symbol.Symbol(pd.Series([0, 1]))
        matrix.add(sym1)
        matrix.add(sym2)
        assert matrix.distance(sym1, sym2) == 1.4142135623730951

    def test_missing(self):
        operator = euclidean_operator.EuclideanOperator()
        matrix = distance_matrix.DistanceMatrix(operator)
        sym1 = symbol.Symbol(pd.Series([1, 0]))
        sym2 = symbol.Symbol(pd.Series([0, 1]))
        matrix.add(sym1)
        assert matrix.distance(sym1, sym2) == None

    def test_add_multiple(self):
        operator = euclidean_operator.EuclideanOperator()
        matrix = distance_matrix.DistanceMatrix(operator)
        sym1 = symbol.Symbol(pd.Series([1, 0]))
        sym2 = symbol.Symbol(pd.Series([0, 1]))
        sym3 = symbol.Symbol(pd.Series([0.5, 1]))
        sym4 = symbol.Symbol(pd.Series([0.5, 0.5]))
        matrix.add(sym1)
        matrix.add(sym2)
        matrix.add(sym3)
        matrix.add(sym4)
        assert matrix.distance(sym1, sym2) == 1.4142135623730951
        assert matrix.distance(sym2, sym1) == 1.4142135623730951
        assert matrix.distance(sym1, sym3) == 1.1180339887498949
        assert matrix.distance(sym1, sym4) == 0.70710678118654757
        assert matrix.distance(sym2, sym2) == 0.0
        assert matrix.distance(sym2, sym3) == 0.5
        assert matrix.distance(sym2, sym4) == 0.70710678118654757
        assert matrix.distance(sym3, sym4) == 0.5