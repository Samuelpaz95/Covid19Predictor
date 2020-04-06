import json
import os
import numpy as np
from matplotlib import pyplot as plt
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data/cases_history.json')
FILE = open(DATA_PATH)
DATA = json.load(FILE)


def read_data(country:str):
    cases = DATA[country]
    dates = list(cases.keys())
    daily_cases = list(cases.values())
    return daily_cases, dates

def calculate_contagions_factor(daily_cases):
    contagions_factor = [] 
    for n in range(len(daily_cases) - 1):
        # EP variable
        ep = (daily_cases[n + 1]/daily_cases[n]) - 1
        contagions_factor.append(ep)
    return np.array(contagions_factor)

def calculate_posibility_range(model, contagions_factor, last_date, last_case):
    inputs = np.arange(1, len(contagions_factor) + 1).reshape(-1, 1)
    
    max_contagions_factor = contagions_factor.copy()
    min_contagions_factor = contagions_factor.copy()
    max_future_cases = [last_case]
    max_future_contagions_factor = [contagions_factor[-1]]
    min_future_cases = [last_case]
    min_future_contagions_factor = [contagions_factor[-1]]
    max_last_case = last_case
    min_last_case = last_case
    
    dates = [last_date]
    _input = len(contagions_factor) + 1
    for _ in range(10):
        out_median, out_mean = model.predict([[_input]])
        
        min_CF = min_contagions_factor_no_zero(contagions_factor)
        
        max_output = max(out_median, out_mean)
        max_output *= int(max_output > 0) 
        max_output += min_CF * int(max_output == 0)
        min_output = min(out_median, out_mean)
        min_output *= int(min_output > 0)
        min_output += min_CF * int(min_output == 0)
        
        max_last_case = max_last_case * (max_output + 1)
        min_last_case = min_last_case * (min_output + 1)
        
        max_future_contagions_factor.append(max_output)
        min_future_contagions_factor.append(min_output)
        
        max_future_cases.append(max_last_case)
        min_future_cases.append(min_last_case)
        
        max_contagions_factor = np.concatenate([contagions_factor, 
                                                [np.max([out_median, out_mean])]])
        min_contagions_factor = np.concatenate([contagions_factor, 
                                                [np.min([out_median, out_mean])]])
        
        _date = str.split(dates[-1], '-')
        _date = date(int(_date[-1]), int(_date[0]), int(_date[1]))
        _date = _date + timedelta(days=1)
        dates.append(_date.strftime('%m-%d-%Y'))
        
        _input += 1
        inputs = np.concatenate([inputs, [[_input]]])
        model.training(inputs, contagions_factor, lote=10)
        
    return (max_future_cases, max_contagions_factor, 
           min_future_cases, min_contagions_factor), dates

def predict_future_cases(model, contagions_factor, last_date, last_case):
    
    inputs = np.arange(1, len(contagions_factor) + 1).reshape(-1, 1)
    contagions_factor = contagions_factor.copy()
    
    new_future_cases = [last_case]
    dates = [last_date]
    new_future_contagions_factor = [contagions_factor[-1]]
    
    _input = len(contagions_factor) + 1
    
    for _ in range(10):
        out_median, out_mean = model.predict([[_input]])
            
        probability_range = abs(out_median - out_mean) / 2
        random_range = np.random.random() * 2 - 1
        probability_range = random_range * probability_range
        
        min_CF = min_contagions_factor_no_zero(contagions_factor)
        probable_output = np.mean([out_median, out_mean]) + probability_range
        probable_output *= np.float64(probable_output > 0 and probable_output > min_CF)
        
        probable_output += min_CF * int(probable_output == 0)
        
        last_case = last_case * (probable_output[0] + 1)
        
        new_future_contagions_factor.append(probable_output[0])
        new_future_cases.append(last_case)
        _date = str.split(dates[-1], '-')
        _date = date(int(_date[-1]), int(_date[0]), int(_date[1]))
        _date = _date + timedelta(days=1)
        dates.append(_date.strftime('%m-%d-%Y'))
        contagions_factor = np.concatenate([contagions_factor, probable_output])
        
        _input += 1
        inputs = np.concatenate([inputs, [[_input]]])
        model.training(inputs, contagions_factor, lote=10)
        
    return new_future_cases, dates, new_future_contagions_factor

def min_contagions_factor_no_zero(contagions_factor):
    contagions_factor = contagions_factor[contagions_factor > 0]
    return min(contagions_factor)