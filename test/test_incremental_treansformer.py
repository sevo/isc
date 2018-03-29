from ISC import incremental_transformer as it
import normalization
import pandas as pd
import pdb

class TestIncrementalTransformer:
    def test_simple(self):
        sequence = pd.Series([1,2,3,4,5,6,1,2,3,4,5,6])
        trans = it.IncrementalTransformer(3,1,0.1)
        symbols = trans.transform(sequence)
        assert len(symbols) == 10
        assert trans.symbol_alphabet.size() == 5
        assert [symbol.scale_shift for symbol in symbols] == [2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 3.0, 4.0, 5.0]

    def test_reusable_normalization(self):
        sequence = pd.Series([1,2,3,4,5,6,1,2,3,4,5,6])
        norm = normalization.ZNormalization()
        norm.train_coefficients(sequence)
        trans = it.IncrementalTransformer(3,1,0.1, normalization=norm)
        symbols = trans.transform(sequence)
        assert len(symbols) == 10
        # pdb.set_trace()
        assert trans.symbol_alphabet.size() == 6
        assert [symbol.scale_shift for symbol in symbols] == [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5]

    def test_incremental_transformation(self):
        sequence = pd.Series([1,2,3,4,5,6,1,2,3,4,5,6])
        trans = it.IncrementalTransformer(3,3,0.1)
        symbols = trans.transform(sequence)
        symbol = trans.add(1)
        assert symbol is None
        symbol = trans.add(2)
        assert symbol is None
        symbol = trans.add(3)
        assert symbol is not None
        assert symbol.scale_multiple == symbols[0].scale_multiple
        assert symbol.scale_shift == symbols[0].scale_shift
