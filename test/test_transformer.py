from ..src import transformer
from ..src import normalization
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

    def test_reusable_normalization(self):
        sequence = pd.Series([1,2,3,4,5,6,1,2,3,4,5,6])
        norm = normalization.ZNormalization()
        norm.train_coefficients(sequence)
        trans = transformer.Transformer(3,1,0.1, normalization=norm)
        symbols = trans.transform(sequence)
        assert len(symbols) == 10
        # pdb.set_trace()
        assert trans.distance_matrix.size() == 6
        assert [symbol.scale_shift for symbol in symbols] == [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5]

