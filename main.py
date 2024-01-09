import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import numpy as np
import datetime
from tensorflow import keras

stock_urls = {'apple': 'https://finance.yahoo.com/quote/AAPL/history?period1=1536192000&period2=1693958400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'microsoft': 'https://finance.yahoo.com/quote/MSFT/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'coke': 'https://finance.yahoo.com/quote/KO/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'tesla': 'https://finance.yahoo.com/quote/TSLA/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'nvidia': 'https://finance.yahoo.com/quote/NVDA/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'google': 'https://finance.yahoo.com/quote/GOOG/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'meta': 'https://finance.yahoo.com/quote/META/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'proctor & gamble': 'https://finance.yahoo.com/quote/PG/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'amazon': 'https://finance.yahoo.com/quote/AMZN/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

#viable_browser_options = {1: "Chrome",
#                          2: "Safari",
#                          3: "Firefox"}

#while True:
#    user_browser_selection = input("Enter the number corresponding to your browser of choice: (1) Chrome, (2) Safari, (3) Firefox")
#
#    try:
#        user_browser_selection = int(user_browser_selection)
#
#    except ValueError:
#        print("Value entered is not a valid input option")
#    
#    if user_browser_selection not in viable_browser_options.keys():
#        raise Exception("User did not enter the number corresponding to one of the viable browser options (1, 2, or 3) ")
#        continue
#    else:
#        break
#

#match user_browser_selection:
#    case 1:
#        browser = webdriver.Chrome()
#    case 2:
#        browser = webdriver.Safari()
#    case 3:
#        browser = webdriver.Firefox()

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
browser = webdriver.Chrome(options=options)
browser.get(stock_urls['apple'])
i = 0
while i < 100:
    browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    i += 1

elements = browser.find_elements(By.XPATH, "//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table")
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









