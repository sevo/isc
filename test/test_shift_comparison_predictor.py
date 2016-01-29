from ..src import transformer
from ..src import shift_comparison_predictor as pred
import pandas as pd
import pdb

class TestPredictor:
    def test_simple(self):
        sequence = pd.Series([1,2,3,4,5,6,1,2,3,4,5,6])
        trans = transformer.Transformer(4,2,0.1)
        symbols = trans.transform(sequence)
        predictor = pred.ShiftComparisonPredictor(trans)
        prediction = predictor.predict()
        # pdb.set_trace()
        assert (prediction.series == symbols[1].series).all()