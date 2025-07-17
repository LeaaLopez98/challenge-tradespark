import backtrader.indicators as btind
from strategies.abstract_strategy import AbstractStrategy 

class GoldenCross(AbstractStrategy):
	"""
	Implementa una estrategia Golden Cross con medias moviles simples (SMA).

	Compra cuando la SMA de 10 cruza por encima de la de 30, y vende cuando ocurre lo contrario.
	"""

	def __init__(self):

		"""
		Inicializa la estrategia creando dos indicadores SMA para cada datafeed:
		una de corto plazo (periodo 10) y otra de largo plazo (periodo 30).

		Estos indicadores se usan para determinar las señales de compra y venta
		basadas en el cruce entre las dos SMAs.
		"""
		
		super().__init__()

		self.short_sma = {}
		self.long_sma = {}

		for name in self.getdatanames():
			self.short_sma[name] = btind.SMA(self.getdatabyname(name).close, period=10)
			self.long_sma[name] = btind.SMA(self.getdatabyname(name).close, period=30)
	
	def condition_for_buy(self, data_name):
		"""
		Args:
			data_name (str): Nombre del datafeed.

		Returns:
			bool: True si la SMA de corto plazo cruza por encima de la SMA de largo plazo.
		"""

		short_sma = self.short_sma.get(data_name)
		long_sma = self.long_sma.get(data_name)

		return short_sma[0] > long_sma[0] and short_sma[-1] < long_sma[-1]
	
	def condition_for_sell(self, data_name):
		"""
		Args:
			data_name (str): Nombre del datafeed.

		Returns:
			bool: True si la SMA de largo plazo cruza por encima de la SMA de corto plazo.
		"""

		short_sma = self.short_sma.get(data_name)
		long_sma = self.long_sma.get(data_name)

		return long_sma[0] > short_sma[0] and long_sma[-1] < short_sma[-1]
	
	def __str__(self):
		return 'GoldenCross'
