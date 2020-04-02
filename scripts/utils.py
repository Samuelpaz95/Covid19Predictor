import json
import os
import numpy as np
from matplotlib import pyplot as plt
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data/bolivia.json')
FILE = open(DATA_PATH)
DATA = json.load(FILE)


def read_data():
    new_cases = DATA['case-history']
    days = []
    fechas = []
    case_history = []
    dates = DATA['init-date']
    day = 1
    fecha = date(dates['year'], dates['month'], dates['day'])
    for new_case in new_cases:
        case_history.append(new_cases[new_case])
        fechas.append(fecha)
        days.append(day)
        fecha = fecha + timedelta(days=1)
        day += 1
    return days, fechas, case_history

def cacular_factores_de_contagio(case_history):
    contagions_factor = []
    for n in range(len(case_history) - 1):
        contagions_factor.append((case_history[n + 1][0]/case_history[n][0]) - 1)
    return np.array(contagions_factor)

def training(model, inputs, labels):
    lote = 5
    model.fit(inputs[:lote], labels[:lote])
    weigths = []
    bias = []
    last_weight = model.coef_
    for i in range(0, len(labels) - lote):
        model.fit(inputs[i:lote+i], labels[i:lote+i])
        weigths.append(model.coef_)
        bias.append(model.intercept_)
    weigths = np.array(weigths)
    bias = np.array(bias)

    coef1 = np.median(weigths, axis=0)
    bias1 = np.median(bias, axis=0)
    model_median = LinearRegression()
    model_median.coef_ = coef1
    model_median.intercept_ = bias1

    coef2 = np.mean(weigths, axis=0)
    bias2 = np.mean(bias, axis=0)
    model_mean = LinearRegression()
    model_mean.coef_ = coef2
    model_mean.intercept_ = bias2

    coeficiente = (coef1 + coef2) / 2
    biasmean = (bias1 + bias2) / 2

    model.coef_ = coeficiente
    model.intercept_ = biasmean
    
    return model, model_median, model_mean

def calculate_worst_case_scenario(model, inputs, labels, start_date):
    outputs = model.predict(inputs)
    distance = np.mean(labels - outputs)
    date = start_date # + timedelta(days=1)
    worst_contagion_factor = [labels[-1]]
    future_dates = [date]
    for inp in np.arange(len(labels)+1, len(labels)+10):
        _input = [[inp, -1]]
        out = model.predict(_input)[0]
        labels = np.append(labels, out + distance)
        inputs = np.concatenate([inputs, _input], axis=0)
        _, model, _ = training(model, inputs, labels)
        worst_contagion_factor.append(out + distance)
        date = date + timedelta(days=1)
        future_dates.append(date)
        
        pass
    return np.array(worst_contagion_factor), future_dates

def calcular_casos_futuros_posibles(worst_contagion_factor,
                                    last_cases_registered):
    new_future_cases = [last_cases_registered]
    last_case = last_cases_registered
    for wcf in worst_contagion_factor:
        future_case = last_case * (wcf + 1)
        new_future_cases.append(future_case)
        last_case = future_case
    return np.array(new_future_cases)[:-1]

def calculate_the_most_probable_cases(model, median_model, mean_model, 
                                      last_cases_registered, last_input):
    new_future_cases = [last_cases_registered]
    
    inputs = np.arange(last_input[0], last_input[0] + 10)
    inputs = np.concatenate([[inputs], np.ones((1, len(inputs)))])
    inputs = np.transpose(inputs)
    
    out_median = median_model.predict(inputs)
    out_median = out_median * np.int32(out_median > 0)
    
    out_mean = mean_model.predict(inputs)
    out_mean = out_mean * np.int32(out_mean > 0)
    
    outputs = model.predict(inputs)
    outputs = outputs * np.int32(outputs > 0)
    
    outputs = np.concatenate([[out_median], [out_mean], [outputs]], axis=0)
    outputs = np.median(outputs, axis=0)
    
    last_case = last_cases_registered
    for out in outputs:
        future_case = last_case * (out + 1)
        new_future_cases.append(future_case)
        last_case = future_case
    
    return np.array(new_future_cases)[:-1]