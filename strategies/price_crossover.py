from strategies.abstract_strategy import AbstractStrategy
import backtrader.indicators as btind

class PriceCrossover(AbstractStrategy):

	params = (
		('period', 10),
	)

	def __init__(self):

		super().__init__()

		self.sma = { name: btind.SMA(self.getdatabyname(name).close, period=self.params.period) for name in self.getdatanames() }

	def condition_for_buy(self, datafeed):
		return self.getdatabyname(datafeed).close[0] > self.sma.get(datafeed)[0]

	def condition_for_sell(self, datafeed):
		return self.getdatabyname(datafeed).close[0] < self.sma.get(datafeed)[0]
	
	def __str__(self):
		return f'PriceCrossover, period={self.params.period}'