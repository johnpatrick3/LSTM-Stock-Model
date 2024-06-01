import datetime
import pandas as pd
import numpy as np

class DataParser():

    #
    # Inputs:  data_list -> List of daily stock data points for the past 5 years. 
    #                       Each list item is a string containing the date and historical stock data like 'Open','Close', etc.  
    # Variables: parsed_data -> empty data-frame that will be populated with Date and Open values from the data_list variable
    #
    def __init__(self, data_list) -> None:
        self.data_list = data_list
        self.parsed_data = pd.DataFrame(columns=["Date", "Open"])

    #
    # Purpose: Extract Date and Open values from each element in data_list. Append to the parsed_data dictonary          
    #   
    def parse_data(self):
       
        for elementValue in self.data_list:

            stock_values = elementValue.split(' ')
            
            if (len(stock_values[1]) == 2):
                stock_values[1] = stock_values[1].zfill(3) 
            
            
            if not ("Dividend" in stock_values or "Stock" in stock_values):
                new_row = {"Date": datetime.datetime.strptime(' '.join(stock_values[0:3]), '%b %d, %Y'),"Open": float(stock_values[3])}
                self.parsed_data = pd.concat([self.parsed_data,pd.DataFrame([new_row])], ignore_index=True)

    #
    # Purpose: Format parsed_data dictonary to add a column with the Log of the Open value and the Diff between LogOpen for each row
    #
    def format_data(self):
        self.parsed_data = self.parsed_data.iloc[::-1]
        self.parsed_data['LogOpen'] = np.log(self.parsed_data['Open'])
        self.parsed_data['DiffLogOpen'] = self.parsed_data['LogOpen'].diff(1)
        