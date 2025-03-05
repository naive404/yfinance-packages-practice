import yfinance as yf
import time
from historicaldata import HistoricalData as HD
# Define the stock symbol
ticker = "NVDA"
period = '7d'
interval = '1m'


HD(ticker, period, interval).calculate_rsi()



