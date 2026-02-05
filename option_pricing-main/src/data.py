import yfinance as yf
import numpy as np

class DataHandler:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None
        self.S = None

    def get_stock_data(self):
        """
        Fetch latest stock data from Yahoo Finance.
        """
        try:
            self.data = yf.download(self.ticker, period="1d", progress=False)
            if self.data.empty:
                raise ValueError(f"No data found for the ticker: {self.ticker}")
            
            if 'Close' in self.data.columns and not self.data['Close'].empty:
                self.S = float(self.data['Close'].iloc[-1])  # <--- Converted to float
                print('Current Stock Price:', self.S)
            else:
                raise ValueError(f"'Close' price data is not available for {self.ticker}.")

        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None


    def calculate_historical_volatility(self, start_date, end_date, window=252):
        """
        Calculate the historical volatility based on stock price data.

        Args:
            start_date (str): Start date for the historical data in "YYYY-MM-DD" format.
            end_date (str): End date for the historical data in "YYYY-MM-DD" format.
            window (int): Rolling window for volatility calculation (default is 252 trading days = 1 year).

        Returns:
            float: Annualised historical volatility.
        """
        try:
            self.data = yf.download(self.ticker, start=start_date, end=end_date, progress=False)
            if self.data.empty:
                raise ValueError(f"No historical data found for the ticker: {self.ticker}")
            
            if 'Close' in self.data.columns and not self.data['Close'].empty:
                # Calculate daily returns
                self.data['Returns'] = self.data['Close'].pct_change()
                # Calculate annualised historical volatility
                historical_volatility = self.data['Returns'].std() * np.sqrt(252)
                return historical_volatility
            else:
                raise ValueError(f"'Close' price data is not available for {self.ticker}.")
        
        except Exception as e:
            print(f"Error calculating historical volatility: {e}")
            return None
