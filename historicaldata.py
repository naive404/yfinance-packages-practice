import yfinance as yf
import pandas as pd

class HistoricalData:
    def __init__(self, ticker, period, interval):
        self.ticker = ticker
        self.period = period
        self.interval = interval

        self.historical_data = pd.DataFrame()
        self.metrics = pd.DataFrame()
        self.EMA_cache = pd.DataFrame()

        # Fetch historical data for the given time period and interval
        stock_data = yf.Ticker(self.ticker)

        # Example: Fetch data for the last 7 days with a 1-hour interval
        historical_data = stock_data.history(period=f"{self.period}", interval=f"{self.interval}")

        # Display the historical data
        historical_data.to_csv(f"C:/Users/twu/Desktop/data/{self.ticker}.csv")
        print(historical_data)
        self.historical_data = historical_data

    def SMA_EMA(self, min = 7):
        # Calculate Simple Moving Average (SMA) for the last 7 periods
        self.min = min
        self.metrics['SMA'] = self.historical_data['Close'].rolling(window=self.min).mean()

        # Calculate Exponential Moving Average (EMA) for the last 7 periods
        self.EMA_cache[f'EMA{min}'] = self.historical_data['Close'].ewm(span=self.min, adjust=False).mean()
        self.metrics[f'EMA{min}']  = self.EMA_cache[f'EMA{min}']
        # Display the updated dataframe
        print(self.metrics)

    def MACD(self, short_window = 12, long_window = 26, signal_window = 9):
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.EMA_cache[f'EMA{short_window}'] = self.historical_data['Close'].ewm(span=self.short_window, adjust=False).mean()
        self.EMA_cache[f'EMA{long_window}'] = self.historical_data['Close'].ewm(span=self.long_window, adjust=False).mean()
        self.metrics[f'MACD{signal_window}'] = self.EMA_cache['EMA12'] - self.EMA_cache['EMA26']
        self.metrics['Signal_Line'] = self.metrics[f'MACD{signal_window}'].ewm(span=self.signal_window, adjust=False).mean()
        print(self.metrics[[f'MACD{signal_window}', 'Signal_Line']])

    def calculate_rsi(self, window=14):
        # Calculate price changes

        delta = self.historical_data['Close'].diff()

        # Calculate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate average gains and losses
        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()

        # Calculate the RS and RSI
        rs = avg_gain / avg_loss
        self.metrics[f'RSI{window}'] = 100 - (100 / (1 + rs))

        # Calculate RSI and add it to the DataFrame

        # Display the updated dataframe
        print(self.metrics[[f'RSI{window}']])