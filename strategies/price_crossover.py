from strategies.abstract_strategy import AbstractStrategy
import backtrader.indicators as btind

class PriceCrossover(AbstractStrategy):
	"""
	Estrategia basada en cruce entre el precio de cierre y una media movil simple (SMA).

	Compra cuando el precio esta por encima de la SMA, y vende cuando cae por debajo.
	El periodo de la SMA es configurable mediante el parámetro 'period'.
	"""

	params = (
		('period', 10),
	)

	def __init__(self):

		"""
		Inicializa la estrategia y crea indicadores SMA para cada datafeed
    	usando el periodo definido en el parametro 'period'.
		"""

		super().__init__()

		self.sma = { name: btind.SMA(self.getdatabyname(name).close, period=self.params.period) for name in self.getdatanames() }

	def condition_for_buy(self, data_name):
		"""		
		Args:
			data_name (str) - Nombre del datafeed.
		
		Returns: 
			bool: True si el precio cruza por encima de la SMA.
		"""

		close = self.getdatabyname(data_name).close
		sma = self.sma.get(data_name)

		return close[0] > sma[0] and close[-1] < sma[-1]

	def condition_for_sell(self, data_name):
		"""		
		Args:
			data_name (str) - Nombre del datafeed.
		
		Returns: 
			bool: True si el precio cruza por debajo de la SMA.
		"""

		close = self.getdatabyname(data_name).close
		sma = self.sma.get(data_name)

		return close[0] < sma[0] and close[-1] > sma[-1] 
	
	def __str__(self):
		return f'PriceCrossover({self.params.period})'