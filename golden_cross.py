import backtrader as bt
import backtrader.indicators as btind

class GoldenCross(bt.Strategy):
	
	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		self.short_sma = btind.SMA(self.data0.close, period=10)
		self.long_sma = btind.SMA(self.data0.close, period=30)
	
	def next(self):
		
		current_price = self.data0.close[0]

		if (self.short_sma[0] > self.long_sma[0] and not self.position):
			
			cash_for_buy = self.broker.get_value() * 0.1

			current_cash = self.broker.get_cash()

			if (current_cash >= cash_for_buy):
				amount_to_buy = int(cash_for_buy / current_price)

				if (amount_to_buy > 0):
					self.buy(size=amount_to_buy)
					self.log('BUY CREATE, %.2f' % current_price)

		elif (self.long_sma[0] > self.short_sma[0] and self.position):
			self.sell(size=self.position.size)
			self.log('SELL CREATE, %.2f' % current_price)