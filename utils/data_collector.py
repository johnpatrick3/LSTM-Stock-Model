import datetime
import pandas as pd
import numpy as np

class DataParser():

    def __init__(self, data_list) -> None:
        self.data_list = data_list
        self.parsed_data = pd.DataFrame(columns=["Date", "Open"])

    def parse_data(self):
       
        for elementValue in self.data_list:

            stock_values = elementValue[13:].split(' ')
    
            if not ("Dividend" in stock_values or "Stock" in stock_values):
                new_row = {"Date": datetime.datetime.strptime(elementValue[:12], '%b %d, %Y'),"Open": float(stock_values[0])}
                self.parsed_data = pd.concat([self.parsed_data,pd.DataFrame([new_row])], ignore_index=True)
               
    def format_data(self):
        
        self.parsed_data['LogOpen'] = np.log(self.parsed_data['Open'])
        self.parsed_data['DiffLogOpen'] = self.parsed_data['LogOpen'].diff(1)
        