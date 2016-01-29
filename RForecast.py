import rpy2.robjects as robjects
import numpy as np
import pandas as pd
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
    predict_f <- function(i, series){
        x <- ts(series[1:i], frequency=96)
        m <- HoltWinters(x, beta = FALSE)
        fc <- forecast.HoltWinters(m, h=48)
        return(fc$mean)
    }
    ''')
predict_function = robjects.globalenv['predict_f']
r_series = robjects.globalenv['series']


filename = "../data/01_zilina_suma.csv"
data = pd.DataFrame.from_csv(filename, index_col=[0,1])

week = 96*7
symbol_length = 96
step = 48
test_data = data.SUM_of_MNOZSTVO[:(week*3)]

i = week
length = len(test_data)
prediction_file = open('prediction.csv', 'a')
target_file = open('target.csv', 'a')
smape_file = open('smape.csv','a')
rmse_file = open('rmse.csv','a')    
while(i <= length - (step * 2)):
    print(i)
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