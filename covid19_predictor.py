import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from sklearn.linear_model import LinearRegression

from scripts.utils import cacular_factores_de_contagio, calcular_casos_futuros_posibles, calculate_the_most_probable_cases, calculate_worst_case_scenario, read_data, training

days, dates, case_history = read_data()
case_history = np.array(case_history)
quarantines = np.array(case_history)[:,1]

contagions_factor = cacular_factores_de_contagio(case_history)

labels = contagions_factor
model = LinearRegression()

inputs = np.concatenate([[days], [quarantines]], axis=0)
inputs = np.transpose(inputs)

model, model_median, model_mean = training(model, inputs[1:], labels)

probable_future_cases = calculate_the_most_probable_cases(model, model_median,
                                                          model_mean, 
                                                          case_history[:,0][-1],
                                                          inputs[-1])


worst_contagion_factors, future_dates = calculate_worst_case_scenario(model_median, inputs[1:], labels, dates[-1])
worst_future_cases = calcular_casos_futuros_posibles(worst_contagion_factors, 
                                                     case_history[-1][0])


    
print("En Bolivia:")
for wfc, pfc, date in zip(worst_future_cases, 
                          probable_future_cases, 
                          future_dates):
    print(' Fecha:', date,
          ' |Casos probables para este dia:', 
          np.round(pfc).astype('int'),
          ' |Casos probables para este dia (en el peor escenario):', 
          np.round(wfc).astype('int'))


_, model_median, _ = training(model, inputs[1:], labels)

# adding 10 days
start_day = inputs[-1][0] + 1
new_inputs = np.arange(start_day, start_day + 10)
new_inputs = np.concatenate([[new_inputs], np.ones((1, len(new_inputs)))])
new_inputs = np.transpose(new_inputs)

inputs = np.concatenate([inputs, new_inputs])


outputs = model.predict(inputs)
outputs = outputs * np.int32(outputs > 0) + 1e-5
outputs1 = model_median.predict(inputs)
outputs1 = outputs1 * np.int32(outputs1 > 0) + 1e-5
outputs2 = model_mean.predict(inputs)
outputs2 = outputs2 * np.int32(outputs2 > 0) + 1e-5

for _ in range(10):
    new_date = dates[-1] + timedelta(days=1)
    dates.append(new_date)

plt.figure(figsize=(15,20))
plt.xlabel('Days')
plt.ylabel('Contagion factor')
plt.subplot(2,1,1)
plt.plot(dates[1:22], labels, '#F00', label="factor de contagios Registrados")
plt.plot(dates, outputs, '#FA0', label="Linear regresion")
plt.plot(dates, outputs1, '#00A', label="Median linear regresion")
plt.plot(dates, outputs2, '#A0A', label="Mean linear regresion")
plt.plot(future_dates,
          worst_contagion_factors, 
          color='#A00', label="El peor escenario con mayor probabilidad en los proximos 10 Dias")
plt.ylim([-0.2, 2.5])
plt.grid(True)
plt.legend()
plt.subplot(2,1,2)
plt.plot(dates[:22], case_history[:,0], label="Historial Casos registrados")

plt.plot(future_dates, worst_future_cases, 
         label="Casos posibles en los siguientes 10 dias (peor escenario con mayor probabilidad)")

plt.plot(future_dates, probable_future_cases, 
         label="Casos posibles en los siguientes 10 dias")
plt.grid(True)
plt.legend()
plt.show()

