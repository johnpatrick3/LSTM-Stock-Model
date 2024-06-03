from selenium import webdriver
#
# Dictonary of websites containing roughly last 5 years of historical financial data from yahoo finance
# These values will be scraped using selenium to obtain historical prices to then be used as model input.
# Dictonary can be expanded for additional stocks and accompany Yahoo Finance Website URLs.
#
stock_urls = {'apple': 'https://finance.yahoo.com/quote/AAPL/history/?period1=1559329399&period2=1717182192'
}

#headers = "Mozilla/5.0 (Linux; Android 11; 100011886A Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Safari/537.36"

#options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
#options.add_argument(f'user-agent={headers}')

browser = webdriver.Chrome()