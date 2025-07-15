from strategies.abstract_strategy import AbstractStrategy
import backtrader.indicators as btind

class PriceCrossover(AbstractStrategy):

	params = (
		('period', 10),
	)

	def __init__(self):

		"""
		Inicializa la estrategia y crea indicadores SMA para cada datafeed
    	usando el período definido en el parametro 'period'.
		"""

		super().__init__()

		self.sma = { name: btind.SMA(self.getdatabyname(name).close, period=self.params.period) for name in self.getdatanames() }

	def condition_for_buy(self, data_name):
		"""
		Compara el precio actual con el SMA para determinar si la estrategia debe comprar.
		
		Args:
			data_name (str) - Nombre del datafeed.
		
		Returns: 
			bool: True si la estrategia debe comprar.
		"""
		return self.getdatabyname(data_name).close[0] > self.sma.get(data_name)[0]

	def condition_for_sell(self, data_name):
		"""
		Compara el precio actual con el SMA para determinar si la estrategia debe vender.
		
		Args:
			data_name (str) - Nombre del datafeed.
		
		Returns: 
			bool: True si la estrategia debe vender.
		"""
		return self.getdatabyname(data_name).close[0] < self.sma.get(data_name)[0]
	
	def __str__(self):
		return f'PriceCrossover({self.params.period})'