import backtrader as bt
import backtrader.indicators as btind

class PriceCrossover(bt.Strategy):

	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		pass

	def next(self):
		pass