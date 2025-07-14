import backtrader as bt

class AbstractStrategy(bt.Strategy):
	
	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		self.strategie_position = { name : 0 for name in self.getdatanames() }

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
	
	def notify_order(self, order):

		if order.status in [order.Submitted, order.Accepted]:
			return
		
		if order.status in [order.Completed]:
			if order.isbuy():
				self.strategies_position[order.data._name] += order.executed.size
				self.log('STRATEGY %s, BUY EXECUTED FOR %s, PRICE: %.2f, SIZE: %.2f' % (str(self), order.data._name, order.executed.price, order.executed.size))
			elif order.issell():
				self.strategies_position[order.data._name] = 0
				self.log('STRATEGY %s, SELL EXECUTED FOR %s, PRICE: %.2f, SIZE: %.2f' % (str(self), order.data._name, order.executed.price, order.executed.size))

		if (order.status in [order.Canceled, order.Margin, order.Rejected]):
			self.log('Order Canceled/Margin/Rejected')

	def next(self):
		for name in self.getdatanames():

			data = self.getdatabyname(name)
			
			current_price = data.close[0]

			position = self.strategie_position.get(name)

			if (self.condition_for_buy(name) and position == 0):
				
				size = self.get_size_to_buy(current_price)

				if (size > 0):
					self.buy(data=data, size=size)
					self.log('STRATEGY %s, BUY CREATE FOR %s, PRICE: %.2f, SIZE: %.2f' % (str(self), name, current_price, size))

			elif (self.condition_for_sell(name) and position > 0):
				self.sell(data=data, size=position)
				self.log('STRATEGY %s, SELL CREATE FOR %s, PRICE: %.2f, SIZE: %.2f' % (str(self), name, current_price, position))