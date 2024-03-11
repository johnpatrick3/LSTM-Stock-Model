from selenium import webdriver
#
# Dictonary of websites containing roughly last 5 years of historical financial data from yahoo finance
# These values will be scraped using selenium to obtain historical prices to then be used as model input
#
stock_urls = {'apple': 'https://finance.yahoo.com/quote/AAPL/history?period1=345427200&period2=1710115200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'microsoft': 'https://finance.yahoo.com/quote/MSFT/history?period1=1536278400&period2=1705881600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'coke': 'https://finance.yahoo.com/quote/KO/history?period1=1536278400&period2=1705881600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'tesla': 'https://finance.yahoo.com/quote/TSLA/history?period1=1536278400&period2=1705881600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'nvidia': 'https://finance.yahoo.com/quote/NVDA/history?period1=1536278400&period2=1705881600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'google': 'https://finance.yahoo.com/quote/GOOG/history?period1=1536278400&period2=1705881600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'meta': 'https://finance.yahoo.com/quote/META/history?period1=1536278400&period2=1705881600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'proctor & gamble': 'https://finance.yahoo.com/quote/PG/history?period1=1536278400&period2=1705881600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true',
              'amazon': 'https://finance.yahoo.com/quote/AMZN/history?period1=1536278400&period2=1705881600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
}

#headers = "Mozilla/5.0 (Linux; Android 11; 100011886A Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Safari/537.36"

#options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
#options.add_argument(f'user-agent={headers}')

browser = webdriver.Chrome()