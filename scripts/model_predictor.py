import numpy as np
from sklearn.linear_model import LinearRegression

class ModelPredictor:
    
    def __init__(self):
        self.median_model = LinearRegression()
        self.mean_model = LinearRegression()
        
    def training(self, inputs, labels, lote=5):
        model = LinearRegression()
        weigths = []
        bias = []
        for i in range(0, len(labels) - lote):
            model.fit(inputs[i:lote+i], labels[i:lote+i])
            weigths.append(model.coef_)
            bias.append(model.intercept_)
        weigths = np.array(weigths)
        bias = np.array(bias)

        coef1 = np.median(weigths, axis=0)
        bias1 = np.median(bias, axis=0)
        self.median_model.coef_ = coef1
        self.median_model.intercept_ = bias1

        coef2 = np.mean(weigths, axis=0)
        bias2 = np.mean(bias, axis=0)
        self.mean_model.coef_ = coef2
        self.mean_model.intercept_ = bias2
        
    def predict(self, inputs):
        median_predictions = self.median_model.predict(inputs)
        mean_predictions = self.mean_model.predict(inputs)
        return median_predictions, mean_predictions
    
    def copy(self):
        model = ModelPredictor()
        model.median_model.coef_ = self.median_model.coef_
        model.median_model.intercept_ = self.median_model.intercept_
        model.mean_model.coef_ = self.mean_model.coef_
        model.mean_model.intercept_ = self.mean_model.intercept_
        return model