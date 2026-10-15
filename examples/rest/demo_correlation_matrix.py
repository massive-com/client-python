"""
This script computes and visualizes the correlation matrix of a selected set of
stocks using Massive's API. This script is for educational purposes only and is
not intended to provide investment advice. The examples provided analyze the
correlation between different stocks from diverse sectors, as well as within
specific sectors.

Blog: https://massive.com/blog/finding-correlation-between-stocks/
Video: https://www.youtube.com/watch?v=q0TgaUGWPFc

Before running this script, there are 4 prerequisites:

1) Dependencies: Ensure that the following Python libraries are installed in
   your environment:
   - pandas
   - numpy
   - seaborn
   - matplotlib.pyplot
   - massive's python-client library

   You can likely run:
   pip install pandas numpy seaborn matplotlib massive-api-client

2) API Key: You will need a Massive API key to fetch the stock data. This can
   be set manually in the script below, or you can set an environment variable
   'MASSIVE_API_KEY'.

   setx MASSIVE_API_KEY "<your_api_key>"   <- windows
   export MASSIVE_API_KEY="<your_api_key>" <- mac/linux

3) Select Stocks: You need to select the stocks you're interested in analyzing.
   Update the 'symbols' variable in this script with your chosen stock symbols.

4) Select Date Range: You need to specify the date range for the historical
   data that you want to fetch. Update the 'start_date' and 'end_date'
   variables in this script accordingly.

Understanding stock correlation is important when building a diverse portfolio,
as it can help manage risk and inform investment strategies. It's always
essential to do your own research or consult a financial advisor for
personalized advice when investing.
"""

import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import seaborn as sns  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from massive import RESTClient

# Less likely to be correlated due to being in different sectors and are
# exposed to different market forces, economic trends, and price risks.
# symbols = ["TSLA", "PFE", "XOM", "HD", "JPM", "AAPL", "KO", "UNH", "LMT", "AMZN"]

# Here we have two groups, one with 5 technology stocks and another with 5 oil
# stocks. These two groups are likely to be highly correlated within their
# respective sectors but are expected to be less correlated between sectors.
# symbols = ["AAPL", "MSFT", "GOOG", "ADBE", "CRM", "XOM", "CVX", "COP", "PSX", "OXY"]

# Likely to be highly correlated due to being in the technology sector,
# specifically in the sub-industry of Semiconductors:
symbols = ["INTC", "AMD", "NVDA", "TXN", "QCOM", "MU", "AVGO", "ADI", "MCHP", "NXPI"]

# Date range you are interested in
start_date = "2022-04-01"
end_date = "2023-05-10"


def fetch_stock_data(symbols, start_date, end_date):
    stocks = []

    # client = RESTClient("XXXXXX") # hardcoded api_key is used
    client = RESTClient()  # MASSIVE_API_KEY environment variable is used

    try:
        for symbol in symbols:
            aggs = client.get_aggs(
                symbol,
                1,
                "day",
                start_date,
                end_date,
            )
            df = pd.DataFrame(aggs, columns=["timestamp", "close"])

            # Filter out rows with invalid timestamps
            df = df[df["timestamp"] > 0]

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)

            df.rename(columns={"close": symbol}, inplace=True)
            stocks.append(df)
    finally:
        pass

    merged_stocks = pd.concat(stocks, axis=1)
    return merged_stocks


def calculate_daily_returns(stock_data):
    daily_returns = stock_data.pct_change().dropna()
    return daily_returns


def compute_correlation_matrix(daily_returns):
    correlation_matrix = daily_returns.corr()
    return correlation_matrix


def plot_correlation_heatmap(correlation_matrix):
    plt.figure(figsize=(8, 8))
    ax = sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    plt.title("Correlation Matrix Heatmap", y=1.08)
    plt.show()


def main():
    stock_data = fetch_stock_data(symbols, start_date, end_date)
    daily_returns = calculate_daily_returns(stock_data)
    correlation_matrix = compute_correlation_matrix(daily_returns)

    print("Correlation Matrix:")
    print(correlation_matrix)

    plot_correlation_heatmap(correlation_matrix)


if __name__ == "__main__":
    main()
