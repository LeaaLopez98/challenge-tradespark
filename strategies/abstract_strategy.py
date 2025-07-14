import backtrader as bt

class AbstractStrategy(bt.Strategy):
	
	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		pass

	def condition_for_sell(self, data_name):
		pass

	def condition_for_buy(self, data_name):
		pass

	def get_size_to_buy(self, current_price):
		
		cash_for_buy = self.broker.get_value() * 0.1
		current_cash = self.broker.get_cash()

		if (current_cash < cash_for_buy):
			return 0

		return int(cash_for_buy / current_price)

	def next(self):
		for name in self.getdatanames():

			data = self.getdatabyname(name)
			
			current_price = data.close[0]

			position = self.getposition(data)

			if (self.condition_for_buy(name) and not position):
				
				size = self.get_size_to_buy(current_price)

				if (size > 0):
					self.buy(data=data, size=size)
					self.log('BUY CREATE FOR %s, PRICE: %.2f, SIZE: %.2f' % (name, current_price, size))

			elif (self.condition_for_sell(name) and position):
				self.sell(data=data, size=position.size)
				self.log('SELL CREATE FOR %s, PRICE: %.2f, SIZE: %.2f' % (name, current_price, position.size))