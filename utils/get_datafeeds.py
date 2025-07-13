import yfinance as yf
from datetime import datetime

if __name__ == '__main__':

	datafeeds = ['AAPL', 'GOOG', 'MSFT', 'TSLA']

	for d in datafeeds:
		data = yf.download(
			tickers=d,
			start=datetime(2021, 1, 1),
			end=datetime(2021, 12, 31),
			multi_level_index=False,
			auto_adjust=False	
		)
		data = data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
		data.to_csv(f'{d}.csv', float_format='%.6f')