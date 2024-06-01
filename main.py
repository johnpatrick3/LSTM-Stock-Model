#import requests
import pandas as pd
#from selenium.webdriver.common.by import By
#from utils.data_collector import DataParser
import time
import numpy as np
#import datetime
import tensorflow as tf
import keras
#from utils import browser, stock_urls


stock_values = pd.read_csv("C:/Users/johnp/OneDrive/Documents/AAPL_test.csv")
#print(stock_values.shape)


# Section3
# The below code section is meant to accomplish the following tasks:
#       1) Separate parsed data into train and test subsets for model training and testing
#           - training set is first 900 elements while the test set is the remaining elements
#       2) Reformat data so that projected Y values can be made using a series of X values
#           - Number of X values used to predict Y values will be based on Tx variable (100 X values (days) to predict 50 Y value (days))
#           - We will be using 150 days of DiffLogOpen values to predict 50 days of DiffLogOpen values in the future
#

train = stock_values.iloc[:1060] # First 1059 values of 1259 total values
test = stock_values.iloc[1060:] # Last 200 values of 1259 total values

train_period = len(train)
test_period = len(stock_values) - train_period

train_indicator = (stock_values.index <= train.index[-1]) # List of True / False values indicating whether stock_values index is part of training set
test_indicator = (stock_values.index > train.index[-1]) # List of True / False values indicating whether stock_values index is part of test set

series = stock_values['DiffLogOpen'].dropna().to_numpy()
print(series.shape)
print(series[0:5])

Tx = 150 #2
Ty = 50 #2
X = np.array([series[t:t+Tx] for t in range(len(series) - Tx-Ty+1)]).reshape(-1, Tx, 1) #2
Y = np.array([series[t+Tx:t+Tx+Ty] for t in range(len(series) - Tx-Ty+1)]).reshape(-1, Ty) #2
N = len(X) #2

print(f'X: {X.shape}, Y: {Y.shape}, N: {N}')

Xtrain, Ytrain = X[:-1], Y[:-1]
Xtest, Ytest = X[-1:], Y[-1:]

train_indicator[:Tx] = False
print(f"Xtrain.shape: {Xtrain.shape}, Xtest.shape: {Xtest.shape}, series.shape: {series.shape}, Ytrain.shape: {Ytrain.shape}")

#Code Section below is the creation of the LSTM model using
num_features = 1
# Put create a keras input vector of shape 150,1
inputs = keras.Input(shape=(Tx, num_features))

# Create an LSTM layer with 16 units/neurons
# Input our keras input vector
x = keras.layers.LSTM(16, return_sequences=False)(inputs)

# Create a Dense layer that takes in the output of the LSTM layer to obtain output
# Used to change the dimensionality from 16 to 1
outputs = keras.layers.Dense(Ty)(x)

model = keras.Model(inputs,outputs)
model.summary()

callbacks = [keras.callbacks.ModelCheckpoint("LSTM_Multi_output_v3.keras",save_best_only=True)]

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
history = model.fit(Xtrain, Ytrain, epochs=20, validation_data=(Xtest,Ytest), callbacks=callbacks)

model = keras.models.load_model("LSTM_Multi_output_v3.keras")
train_predictions = model.predict(Xtrain)
test_predictions = model.predict(Xtest)

#print(train_predictions.shape)
#print(test_predictions.shape)

print("predicted 50 day log return from last date: {}".format(np.sum(test_predictions)))
print("actual 50 day log return from last date: {}".format(sum(stock_values['DiffLogOpen'][-50:])))

    
    

 






