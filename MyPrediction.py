from src import incremental_transformer as it
from src import shift_comparison_predictor as shift_pred
from src import simple_comparison_predictor as simple_pred
import pandas as pd
from src import normalization as norm
import numpy as np
import os
import pdb

def smape(prediction, target):
    return np.mean(np.abs(target - prediction) / np.abs(target + prediction)) * 200

def rmse(prediction, target):
    return np.sqrt(((prediction - target) ** 2).mean())

for csv_file in  os.listdir("../agg_data"):
    filename = "../agg_data/" + csv_file
    data = pd.DataFrame.from_csv(filename, index_col=[0,1])

    week = 96*7
    symbol_length = 96
    step = 48

    test_data = data.SUM_of_MNOZSTVO#[:(week*85)]

    normalization = norm.ZNormalization()
    normalization.train_coefficients(test_data[0:week])
    trans = it.IncrementalTransformer(symbol_length, step, 0.5, normalization=normalization)
    symbols = trans.transform(test_data[0:(week-step)])
    predictor = shift_pred.ShiftComparisonPredictor(trans)

    i = week
    length = len(test_data)
    prediction_file = open('my_prediction_'+csv_file, 'a')
    target_file = open('my_target_'+csv_file, 'a')
    smape_file = open('my_smape_'+csv_file,'a')
    rmse_file = open('my_rmse_'+csv_file,'a')
    while(i <= length - (step * 2)):
        print(csv_file, i)
        symbols = trans.transform(test_data[(i-step):i])        
        prediction = predictor.predict()
        pom = (prediction.series[step:] * normalization.scale) + normalization.shift
        target = test_data[i:(i+step)]
        # pdb.set_trace()
        pd.Series(target).to_csv(target_file, header=False)
        pd.Series(pom).to_csv(prediction_file, header=False)
        pd.Series(rmse(pom, target)).to_csv(rmse_file, header=False)
        pd.Series(smape(pom, target)).to_csv(smape_file, header=False)        
        if(i % week == 0):
            normalization.train_coefficients(test_data[(i-week):i])
        i+=step
    prediction_file.close()
    target_file.close()
    smape_file.close()
    rmse_file.close()
