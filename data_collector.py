import requests
from bs4 import BeautifulSoup
import pandas as pd

stock_urls = {'apple': 'https://finance.yahoo.com/quote/AAPL/history?period1=1536192000&period2=1693958400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'microsoft': 'https://finance.yahoo.com/quote/MSFT/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'coke': 'https://finance.yahoo.com/quote/KO/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'tesla': 'https://finance.yahoo.com/quote/TSLA/history?period1=1536278400&period2=1694044800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'


}