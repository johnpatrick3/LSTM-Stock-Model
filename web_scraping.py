import requests
from selenium.webdriver.common.by import By
from utils.data_collector import DataParser
from utils import browser, stock_urls

# Section 1
# The below code section is meant to accomplish the following tasks:
#       1) Run a GET API call on the Yahoo Finance website for the historical apple stock information
#       2) Continuously scroll down on webpage so that the complete financial stock information table can be loaded onto the webpage.
#       3) Extract the historical financial data and save to a list called elements for further parsing 
#
browser.get(stock_urls['apple']) #1

#
# These two lines of code were to support the older version of Yahoo Finance
# in which the full table of historical financial data wouldn't be displayed
# unless the webpage was scrolled fully to the bottom.
# 
#for _ in range(75):
#    browser.execute_script("window.scrollBy(0,document.body.scrollHeight)") #2


elements = browser.find_elements(By.XPATH, "//*[@id=\"nimbus-app\"]/section/section/section/article/div[1]/div[3]/table") #3
elements = elements[0].text.split('\n')[3:] #3


# Section2
# The below code section is meant to accomplish the following tasks:
#       1) Create a DataParser object that takes in the daily stock price data
#       2) Parse the stock price data so that the Date and Open value are stored in the objects parsed_data Dataframe
#       3) Format the data to add a LogOpen and DiffLogOpen column within the objects parsed_data Dataframe
#
stock_values = DataParser(elements) #1
stock_values.parse_data() #2
stock_values.format_data() #3
stock_values.parsed_data.to_csv("C:/Users/johnp/OneDrive/Documents/AAPL_test.csv")