import backtrader as bt
import math
from utils.logger import Logger
from utils.pending_cash import pending_cash

class AbstractStrategy(bt.Strategy):

	"""
	Clase que define la logica comun que comparten las estrategias, incluyendo
	el registro de operaciones y evolucion del portfolio en CSV, y el control
	de posiciones por activo.

	Las clases concretas deben implementar:
		- condition_for_buy()
		- condition_for_sell()
	"""

	def log(self, action, status, ticker, price, size, dt=None):
		dt = dt or self.datas[0].datetime.date(0)

		Logger.write_csv(
			[dt.isoformat(), str(self), action, status, ticker, f'{price:.2f}', int(size), f'{self.broker.get_value():.2f}'],
	)

	def __init__(self):
		"""
		Inicializa la estrategia con un diccionario de posiciones por datafeed.
			
		Cada instancia mantiene su propia estructura de posiciones, para permitir
		distinguir las compras segun la estrategia que la genero.
		"""

		self.strategy_position = { name : 0 for name in self.getdatanames() }

	def condition_for_sell(self, data_name):
		"""
		Verifica si la estrategia debe vender.
		 
		La condicion la deben implementar las estrategias concretas.
		
		Args:
			data_name (str) - Nombre del datafeed.
		
		Returns: 
			bool: True si la estrategia debe vender.
		"""
		pass

	def condition_for_buy(self, data_name):
		"""
		Verifica si la estrategia debe comprar.
		 
		La condicion la deben implementar las estrategias concretas.
		
		Args:
			data_name (str) - Nombre del datafeed.
		
		Returns: 
			bool: True si la estrategia debe comprar.
		"""
		pass

	def get_size_to_buy(self, current_price):

		"""
		Calcula la cantidad de acciones a comprar en base al 10% del valor de la cartera.

		Verifica que haya suficiente liquidez para realizar la compra.
		Si no hay efectivo suficiente, devuelve 0.

		Args:
			current_price (float) - Precio actual de cierre.

		Returns:
			int: Cantidad de acciones a comprar.
		"""
		
		cash_for_buy = self.broker.get_value() * 0.1

		# Al total liquido que tengo en este momento le resto el dinero pendiente
		current_cash = self.broker.get_cash() - pending_cash.get_amount()

		if (current_cash < cash_for_buy):
			return 0
		
		return int(cash_for_buy / current_price)
	
	def notify_order(self, order):

		"""
		Notifica si existe un cambio en el estado de la orden.

		Si la orden fue aceptada o enviada, se ignora.
		Si la orden fue completada, se actualiza la posicion de la estrategia, se registra un log y se libera el dinero reservado.
		Si la orden fue rechazada o cancelada, se registra un log.

		Args:
			order (object) - Objeto de la orden.
		"""

		if order.status in [order.Submitted, order.Accepted]:
			return
		
		if order.status in [order.Completed]:
			if order.isbuy():
				self.strategy_position[order.data._name] += order.executed.size
				self.log('BUY', 'EXECUTED', order.data._name, order.executed.price, order.executed.size)

				# Libero el dinero reservado una vez que se ejecuto la compra
				pending_cash.release(order.ref)
			elif order.issell():
				self.strategy_position[order.data._name] = 0
				self.log('SELL', 'EXECUTED', order.data._name, order.executed.price, order.executed.size)

		if order.status in [order.Canceled, order.Margin, order.Rejected]:
			if (order.isbuy()):
				action = 'BUY'

				# Libero el dinero reservado si la operacion no se lleva a cabo
				pending_cash.release(order.ref)
			else:
				action = 'SELL'
			self.log(action, "FAILED", order.data._name, 0, 0)

	def next(self):
		"""
		Ejecuta la logica de compra/venta para cada uno de los activos en cada paso.

		Verifica condiciones de compra y venta, gestiona posiciones y crea ordenes.
		"""

		# Itera sobre cada uno de los datafeeds
		for name in self.getdatanames():

			data = self.getdatabyname(name)
			
			current_price = data.close[0]

			position = self.strategy_position.get(name)

			# Verifica si la estrategia debe comprar
			if (self.condition_for_buy(name) and position == 0):
				
				size = self.get_size_to_buy(current_price)

				if (size > 0):
					order = self.buy(data=data, size=size)

					# Reservo el dinero (funcion techo para tener cierto margen) con su referencia
					pending_cash.reserve(order.ref, math.ceil(size * current_price))
					self.log('BUY', 'CREATE', name, current_price, size)

			# Verifica si la estrategia debe vender
			elif (self.condition_for_sell(name) and position > 0):
				self.sell(data=data, size=position)
				self.log('SELL', 'CREATE', name, current_price, position)