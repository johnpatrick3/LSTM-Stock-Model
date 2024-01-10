import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
import numpy as np
import datetime
#import tensorflow as tf
from utils import browser, stock_urls

browser.get(stock_urls['apple'])

i = 0
while i < 50:
    browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    i += 1

elements = browser.find_elements(By.XPATH, "//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table/tbody")
elements = elements[0].text.split('\n')[1:-1]

parsed_data = pd.DataFrame([],columns=["Date", "Open"])

for elementValue in elements:
  
    stock_values = elementValue[13:].split(' ')
    temp_dict = {}
    if not ("Dividend" in stock_values or "Stock" in stock_values):
        
        temp_dict["Date"] = datetime.datetime.strptime(elementValue[:12], '%b %d, %Y')
        temp_dict["Open"] = float(stock_values[0])
        parsed_data = pd.concat([parsed_data,pd.DataFrame([temp_dict])], ignore_index=True)
    

parsed_data['LogOpen'] = np.log(parsed_data['Open'])
parsed_data['DiffLogOpen'] = parsed_data['LogOpen'].diff(1)

train = parsed_data.iloc[:901]
test = parsed_data.iloc[901:]

train_period = 900
test_period = len(parsed_data) - train_period
print(f"test_period: {test_period}")

train_indicator = (parsed_data.index <= train.index[-1])
test_indicator = (parsed_data.index > train.index[-1])

series = parsed_data['DiffLogOpen'].dropna().to_numpy()

Tx = 100
Ty = 1
X = np.array([series[t:t+Tx] for t in range(len(series) - Tx-Ty+1)]).reshape(-1, Tx, 1)
Y = np.array([series[t+Tx+Ty-1] for t in range(len(series) - Tx-Ty+1)]).reshape(-1, Ty)
N = len(X)

Xtrain, Ytrain = X[:-test_period], Y[:-test_period]
Xtest, Ytest = X[-test_period:], Y[-test_period:]

print(f"Xtrain.shape: {Xtrain.shape}, Xtest.shape: {Xtest.shape}, series.shape: {series.shape}, X.shape: {X.shape}")

#Code Section below is the creation of the LSTM model using









