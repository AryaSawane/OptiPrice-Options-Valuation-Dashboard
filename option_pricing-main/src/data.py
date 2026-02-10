import yfinance as yf
import numpy as np
import streamlit as st


class DataHandler:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.data = None
        self.S = None   # latest stock price

  def get_stock_data(self):
    try:
        # use last few days instead of period="1d"
        self.data = yf.download(
            self.ticker,
            start="2026-02-01",   # or: datetime.today() - timedelta(days=7)
            end=None,
            progress=False
        )

        if self.data.empty:
            st.error(f"No data found for the ticker: {self.ticker}")
            self.S = None
            return None

        if "Close" in self.data.columns and not self.data["Close"].empty:
            self.S = float(self.data["Close"].iloc[-1])
            return self.S
        else:
            st.error(f"'Close' price data is not available for {self.ticker}.")
            self.S = None
            return None

    except Exception as e:
        st.error(f"Error fetching stock data for {self.ticker}: {e}")
        self.S = None
        return None

    def calculate_historical_volatility(self, start_date: str, end_date: str, window: int = 252):
        """
        Calculate annualised historical volatility based on historical data
        between start_date and end_date (YYYY-MM-DD).
        """
        try:
            self.data = yf.download(
                self.ticker,
                start=start_date,
                end=end_date,
                progress=False,
            )

            if self.data.empty:
                st.error(f"No historical data found for the ticker: {self.ticker}")
                return None

            if "Close" in self.data.columns and not self.data["Close"].empty:
                # Daily returns
                self.data["Returns"] = self.data["Close"].pct_change()

                # Annualised historical volatility
                historical_volatility = self.data["Returns"].std() * np.sqrt(252)
                return float(historical_volatility)
            else:
                st.error(f"'Close' price data is not available for {self.ticker}.")
                return None

        except Exception as e:
            st.error(f"Error calculating historical volatility for {self.ticker}: {e}")
            return None
