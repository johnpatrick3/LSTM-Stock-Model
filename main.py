import requests
import pandas as pd
from selenium.webdriver.common.by import By
from utils.data_collector import DataParser
import time
import numpy as np
import datetime
import tensorflow as tf
import keras
from utils import browser, stock_urls

# Section 1
# The below code section is meant to accomplish the following tasks:
#       1) Run a GET API call on the Yahoo Finance website for the historical apple stock information
#       2) Continuously scroll down on webpage so that the complete financial stock information table can be loaded onto the webpage.
#       3) Extract the historical financial data and save to a list called elements for further parsing 
#
browser.get(stock_urls['apple']) #1

for _ in range(75):
    browser.execute_script("window.scrollBy(0,document.body.scrollHeight)") #2


elements = browser.find_elements(By.XPATH, "//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table/tbody") #3
elements = elements[0].text.split('\n')[1:-1] #3

# Section2
# The below code section is meant to accomplish the following tasks:
#       1) Create a DataParser object that takes in the daily stock price data
#       2) Parse the stock price data so that the Date and Open value are stored in the objects parsed_data Dataframe
#       3) Format the data to add a LogOpen and DiffLogOpen column within the objects parsed_data Dataframe
#
stock_values = DataParser(elements) #1
stock_values.parse_data() #2
stock_values.format_data() #3

# Section3
# The below code section is meant to accomplish the following tasks:
#       1) Separate parsed data into train and test subsets for model training and testing
#           - training set is first 900 elements while the test set is the remaining elements
#       2) Reformat data so that projected Y values can be made using a series of X values
#           - Number of X values used to predict Y will be based on Tx variable (100 X values to predict 1 Y value)
#           - Number of predicted Y values for Tx number of X values will be Ty (1)
#
train = stock_values.parsed_data.iloc[:901] #1
test = stock_values.parsed_data.iloc[901:] #1
#print(f'train: {train}')

train_period = 900
test_period = len(stock_values.parsed_data) - train_period
#print(f"test_period: {test_period}")

train_indicator = (stock_values.parsed_data.index <= train.index[-1])
test_indicator = (stock_values.parsed_data.index > train.index[-1])
#print(f'train_indicator: {train_indicator}')

series = stock_values.parsed_data['DiffLogOpen'].dropna().to_numpy()

Tx = 100 #2
Ty = 1 #2
X = np.array([series[t:t+Tx] for t in range(len(series) - Tx-Ty+1)]).reshape(-1, Tx, 1) #2
Y = np.array([series[t+Tx+Ty-1] for t in range(len(series) - Tx-Ty+1)]).reshape(-1, Ty) #2
N = len(X) #2
#print(f'X: {X}')
#print(f'Y: {Y}')

Xtrain, Ytrain = X[:-test_period], Y[:-test_period]
Xtest, Ytest = X[-test_period:], Y[-test_period:]

#print(f"Xtrain.shape: {Xtrain.shape}, Xtest.shape: {Xtest.shape}, series.shape: {series.shape}, X.shape: {X.shape}")

#Code Section below is the creation of the LSTM model using
num_features = 1
# Put create a kears input vector of shape 100,1
inputs = keras.Input(shape=(Tx, num_features))

# Create an LSTM layer with 16 units/neurons
# Input our keras input vector
x = keras.layers.LSTM(16)(inputs)

# Create a Dense layer that takes in the output of the LSTM layer to obtain output
# Used to change the dimensionality from 16 to 1
outputs = keras.layers.Dense(1)(x)

model = keras.Model(inputs,outputs)

callbacks = [keras.callbacks.ModelCheckpoint("LSTM_output.keras",save_best_only=True)]

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

history = model.fit(Xtrain, Ytrain, epochs=20, validation_data=(Xtest,Ytest), callbacks=callbacks)

model = keras.models.load_model("LSTM_output.keras")
train_predictions = model.predict(Xtrain).flatten()
test_predictions = model.predict(Xtest).flatten()

print(test_predictions[-1:])
print(stock_values.parsed_data.tail())

if __name__ == '__main__':
    model = keras.models.load_model("LSTM_output.keras")
    train_predictions = model.predict(Xtrain).flatten()
    test_predictions = model.predict(Xtest).flatten()
    
    stock_values.parsed_data['Lag_LogAAPL'] = stock_values.parsed_data['LogOpen'].shift(1)
    lag = stock_values.parsed_data['Lag_LogAAPL'] 






