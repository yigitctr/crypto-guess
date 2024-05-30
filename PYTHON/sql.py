import sqlite3
import pandas as pd

# SQLite veritabanını oluşturun
conn = sqlite3.connect('crypto_prices.db')
c = conn.cursor()

# Bitcoin fiyat tablosunu oluşturun
c.execute('''
    CREATE TABLE IF NOT EXISTS bitcoin_prices (
        date TEXT PRIMARY KEY,
        price REAL
    )
''')

# CSV dosyasından veriyi yükleyin
df = pd.read_csv('bitcoin_prices.csv')

# Veriyi veritabanına aktarın
df.to_sql('bitcoin_prices', conn, if_exists='replace', index=False)

# Değişiklikleri kaydedin ve bağlantıyı kapatın
conn.commit()
conn.close()
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# SQLite veritabanına bağlanın
conn = sqlite3.connect('crypto_prices.db')
query = 'SELECT * FROM bitcoin_prices'

# Veriyi okuyun
data = pd.read_sql(query, conn, parse_dates=['date'], index_col='date')

# Bağlantıyı kapatın
conn.close()

# Veriyi inceleyin
print(data.head())

# Zaman serisi verisini görselleştirin
plt.figure(figsize=(10, 6))
plt.plot(data['price'], label='Bitcoin Price')
plt.title('Bitcoin Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# ARIMA modeli ile zaman serisi analizi
# ARIMA(p,d,q) parametrelerinin belirlenmesi (bu parametreler için grid search yapılabilir)
p = 5
d = 1
q = 2

# SARIMAX modelini oluşturun ve eğitin
model = SARIMAX(data['price'], order=(p, d, q))
results = model.fit()

# Modelin özetini yazdırın
print(results.summary())

# Gelecekteki fiyatları tahmin edin
forecast_steps = 30  # 30 gün ileriye tahmin yapıyoruz
forecast = results.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=data.index[-1], periods=forecast_steps + 1, closed='right')
forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)

# Tahminleri görselleştirin
plt.figure(figsize=(10, 6))
plt.plot(data['price'], label='Observed')
plt.plot(forecast_series, label='Forecast', color='red')
plt.title('Bitcoin Price Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()


import sqlite3
import pandas as pd

# SQLite veritabanını oluşturun
conn = sqlite3.connect('crypto_prices.db')
c = conn.cursor()

# Bitcoin fiyat tablosunu oluşturun
c.execute('''
    CREATE TABLE IF NOT EXISTS bitcoin_prices (
        date TEXT PRIMARY KEY,
        price REAL
    )
''')

# CSV dosyasından veriyi yükleyin
df = pd.read_csv('bitcoin_prices.csv')

# Veriyi veritabanına aktarın
df.to_sql('bitcoin_prices', conn, if_exists='replace', index=False)

# Değişiklikleri kaydedin ve bağlantıyı kapatın
conn.commit()
conn.close()

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX


conn = sqlite3.connect('crypto_prices.db')
query = 'SELECT * FROM bitcoin_prices'


data = pd.read_sql(query, conn, parse_dates=['date'], index_col='date')


conn.close()


print(data.head())


plt.figure(figsize=(10, 6))
plt.plot(data['price'], label='Bitcoin Price')
plt.title('Bitcoin Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()


p = 5
d = 1
q = 2


model = SARIMAX(data['price'], order=(p, d, q))
results = model.fit()


print(results.summary())


forecast_steps = 30  
forecast = results.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=data.index[-1], periods=forecast_steps + 1, closed='right')
forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)


plt.figure(figsize=(10, 6))
plt.plot(data['price'], label='Observed')
plt.plot(forecast_series, label='Forecast', color='red')
plt.title('Bitcoin Price Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
