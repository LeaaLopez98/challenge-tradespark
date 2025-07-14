import backtrader as bt
import backtrader.indicators as btind

class GoldenCross(bt.Strategy):
	
	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		
		self.short_sma = {}
		self.long_sma = {}

		for name in self.getdatanames():
			self.short_sma[name] = btind.SMA(self.getdatabyname(name).close, period=10)
			self.long_sma[name] = btind.SMA(self.getdatabyname(name).close, period=30)
	
	def next(self):
		
		for name in self.getdatanames():
			
			data = self.getdatabyname(name)
			
			current_price = data.close[0]

			position = self.getposition(data)
			
			if (self.short_sma.get(name)[0] > self.long_sma.get(name)[0] and not position):
				
				cash_for_buy = self.broker.get_value() * 0.1

				current_cash = self.broker.get_cash()

				if (current_cash >= cash_for_buy):
					amount_to_buy = int(cash_for_buy / current_price)

					if (amount_to_buy > 0):
						self.buy(data=data, size=amount_to_buy)
						self.log('BUY CREATE, %.2f' % current_price)

			elif (self.long_sma.get(name)[0] > self.short_sma.get(name)[0] and position):
				self.sell(data=data, size=position.size)
				self.log('SELL CREATE, %.2f' % current_price)