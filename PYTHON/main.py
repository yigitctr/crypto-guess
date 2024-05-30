import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX


data = pd.read_csv('bitcoin_prices.csv', parse_dates=['Date'], index_col='Date')


print(data.head())


plt.figure(figsize=(10, 6))
plt.plot(data['Price'], label='Bitcoin Price')
plt.title('Bitcoin Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()


p = 5
d = 1
q = 2


model = SARIMAX(data['Price'], order=(p, d, q))
results = model.fit()

print(results.summary())


forecast_steps = 30  
forecast = results.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=data.index[-1], periods=forecast_steps + 1, closed='right')
forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)


plt.figure(figsize=(10, 6))
plt.plot(data['Price'], label='Observed')
plt.plot(forecast_series, label='Forecast', color='red')
plt.title('Bitcoin Price Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
