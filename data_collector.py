import datetime
import pandas as pd

class DataParser():

    def __init__(self, data_string) -> None:
        self.data_string = data_string
        self.parsed_data = pd.DataFrame([],columns=["Date", "Open", "Close"])

    def parse_data(self):
       temp_list = []
       
       temp_list.append(self.data_string)
      

       