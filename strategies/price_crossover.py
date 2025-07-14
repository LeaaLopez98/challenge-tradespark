from strategies.abstract_strategy import AbstractStrategy
import backtrader.indicators as btind

class PriceCrossover(AbstractStrategy):

	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	params = (
		('period', 10),
	)

	def __init__(self):
		self.sma = { name: btind.SMA(self.getdatabyname(name).close, period=self.params.period) for name in self.getdatanames() }

	def condition_for_buy(self, datafeed):
		return self.getdatabyname(datafeed).close[0] > self.sma.get(datafeed)[0]

	def condition_for_sell(self, datafeed):
		return self.getdatabyname(datafeed).close[0] < self.sma.get(datafeed)[0]