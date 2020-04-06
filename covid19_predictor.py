import sys
from datetime import date as Date
from matplotlib import pyplot as plt
from scripts import *

cases_predictor = ModelPredictor()
def main(args:list):
    if args[0] == 'update':
        update_data()
    else:
        country = args[0]
        daily_cases, dates = read_data(country)
        contag_factor = calculate_contagions_factor(daily_cases)
        
        
        inputs = np.arange(1,len(contag_factor) + 1).reshape(-1,1)
        cases_predictor.training(inputs, contag_factor, lote=10)
        
        median_predictions, mean_predictions = cases_predictor.predict(inputs)
        
        fut_cases, fut_dates, fut_contag_factor = predict_future_cases(
            
            model=cases_predictor.copy(),
            contagions_factor=contag_factor, 
            last_date=dates[-1], 
            last_case=daily_cases[-1]
        )
        
        (max_future_cases, max_contagions_factor, 
        min_future_cases, min_contagions_factor), _ = calculate_posibility_range(
            
            model=cases_predictor.copy(),
            contagions_factor=contag_factor, 
            last_date=dates[-1], 
            last_case=daily_cases[-1]
        )
        
        print_estimations(max_future_cases, 
                        min_future_cases, 
                        fut_cases, country, fut_dates)
        
        # Ploting
        plt.figure(figsize=(15,10))
        plt.xlabel('Days')
        plt.ylabel('Contagion factor')
        plt.subplot(2,1,1)
        plt.plot(dates[1:], contag_factor, label="Contagions_factor")
        plt.plot(fut_dates, fut_contag_factor, label="Expected future contagion factor")
        plt.plot(dates[1:], mean_predictions, label="Mean Predictions")
        plt.plot(dates[1:], median_predictions, label="Median Predictions")
        plt.xticks(rotation=60, ha='right')
        plt.grid(True)
        plt.legend()
        plt.subplot(2,1,2)
        plt.plot(dates, daily_cases, label="Daily cases")
        plt.plot(fut_dates, fut_cases, label="Expected future daily cases")
        plt.plot(fut_dates, min_future_cases, label="Min. Future daily cases")
        plt.plot(fut_dates, max_future_cases, label="Max. Future daily cases")
        #plt.fill_between(fut_dates, 
        #                 max_future_cases, 
        #                 min_future_cases)
        plt.xticks(rotation=60, ha='right')
        plt.grid(True)
        plt.legend()
        plt.show()
        
def print_estimations(max_future_cases, min_future_cases, future_cases,
                      country, dates):
    print("En", country)
    print("Format date: (mm-dd-yyyy)")
    print("Numero de infectados:")
    for max_case, min_case, fut_case, date in zip(max_future_cases, 
                                            min_future_cases,
                                            future_cases,
                                            dates):
        print("Fecha:", date)
        print("\nNumero de Infectados Probable entre:",
              int(np.around(min_case)), '-', int(np.around(max_case)),
              "\nEl mas probable:", int(fut_case))
        print("------------------------------------------------------")

if __name__ == "__main__":
    main(sys.argv[1:])