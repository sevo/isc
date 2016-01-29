import rpy2.robjects as robjects
import numpy as np
import pandas as pd
import os
import pdb

def smape(prediction, target):
    return np.mean(np.abs(target - prediction) / np.abs(target + prediction)) * 200

def rmse(prediction, target):
    return np.sqrt(((prediction - target) ** 2).mean())

robjects.r('''
        library('forecast')
        library('stats')

        filename <- "../data/01_zilina_suma.csv"
        symbol_length <- 96
        step <- 48
        week <- symbol_length * 7
        data = read.csv(filename, header = TRUE)
        start_date <- strptime(data$DATUM[1], "%d/%m/%Y")
        end_date <- strptime(data$DATUM[length(data$DATUM)], "%d/%m/%Y")
        series <- ts(data$SUM_of_MNOZSTVO, start=as.numeric(start_date), frequency=96)
        ''')

robjects.r('''
    load_data <- function(filename){
        data = read.csv(filename, header = TRUE)
        start_date <- strptime(data$DATUM[1], "%d/%m/%Y")
        end_date <- strptime(data$DATUM[length(data$DATUM)], "%d/%m/%Y")
        series <- ts(data$SUM_of_MNOZSTVO, start=as.numeric(start_date), frequency=96)
        return(series)
    }
    ''')

robjects.r('''
    predict_f <- function(i, series){
        x <- ts(series[1:i], frequency=96)
        m <- HoltWinters(x)
        fc <- forecast.HoltWinters(m, h=48)
        return(fc$mean)
    }
    ''')
predict_function = robjects.globalenv['predict_f']
load_function = robjects.globalenv['load_data']


for csv_file in  os.listdir("../agg_data"):
    filename = "../agg_data/" + csv_file
    r_series = load_function(filename)


    data = pd.DataFrame.from_csv(filename, index_col=[0,1])

    week = 96*7
    symbol_length = 96
    step = 48
    test_data = data.SUM_of_MNOZSTVO#[:(week*3)]

    i = week
    length = len(test_data)
    prediction_file = open('prediction_'+csv_file, 'a')
    target_file = open('target_'+csv_file, 'a')
    smape_file = open('smape_'+csv_file,'a')
    rmse_file = open('rmse_'+csv_file,'a')    
    while(i <= length - (step * 2)):
        print(csv_file, i)
        prediction = predict_function(i, r_series)
        target = test_data[i:(i+step)]
        # pdb.set_trace()
        pd.Series(np.array(target)).to_csv(target_file, header=False)
        pd.Series(np.array(prediction)).to_csv(prediction_file, header=False)
        pd.Series(rmse(prediction, target)).to_csv(rmse_file, header=False)
        pd.Series(smape(prediction, target)).to_csv(smape_file, header=False)
        i+=step
        
    prediction_file.close()
    target_file.close()
    smape_file.close()
    rmse_file.close()