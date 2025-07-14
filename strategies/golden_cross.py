import backtrader.indicators as btind
from strategies.abstract_strategy import AbstractStrategy 

class GoldenCross(AbstractStrategy):
	
	def __init__(self):
		
		super().__init__()

		self.short_sma = {}
		self.long_sma = {}

		for name in self.getdatanames():
			self.short_sma[name] = btind.SMA(self.getdatabyname(name).close, period=10)
			self.long_sma[name] = btind.SMA(self.getdatabyname(name).close, period=30)
	
	def condition_for_buy(self, data_name):
		return self.short_sma.get(data_name)[0] > self.long_sma.get(data_name)[0]
	
	def condition_for_sell(self, data_name):
		return self.long_sma.get(data_name)[0] > self.short_sma.get(data_name)[0]
	
	def __str__(self):
		return 'GoldenCross Strategy'
