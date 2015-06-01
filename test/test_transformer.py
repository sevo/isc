from ..src import transformer
import pandas as pd
import pdb

class TestTransformer:
    def test_simple(self):
        sequence = pd.Series([1,2,3,4,5,6,1,2,3,4,5,6])
        trans = transformer.Transformer(3,1,0.1)
        symbols = trans.transform(sequence)
        assert len(symbols) == 10
        assert trans.distance_matrix.size() == 3
        assert [symbol.scale_shift for symbol in symbols] == [2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 3.0, 4.0, 5.0]

