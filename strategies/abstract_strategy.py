import backtrader as bt

class AbstractStrategy(bt.Strategy):
	
	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

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
			bool: True si la estrategia debe vender.
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
		current_cash = self.broker.get_cash()

		if (current_cash < cash_for_buy):
			return 0

		return int(cash_for_buy / current_price)
	
	def notify_order(self, order):

		"""
		Notifica el estado de la orden.

		Si la orden fue aceptada o enviada, se ignora.
		Si la orden fue completada, se actualiza la posicion de la estrategia y se imprime un log.
		Si la orden fue rechazada o cancelada, se imprime un log.

		Args:
			order (object) - Objeto de la orden.
		"""

		if order.status in [order.Submitted, order.Accepted]:
			return
		
		if order.status in [order.Completed]:
			if order.isbuy():
				self.strategy_position[order.data._name] += order.executed.size
				self.log('STRATEGY %s, BUY EXECUTED FOR %s, PRICE: %.2f, SIZE: %.2f' % (str(self), order.data._name, order.executed.price, order.executed.size))
			elif order.issell():
				self.strategy_position[order.data._name] = 0
				self.log('STRATEGY %s, SELL EXECUTED FOR %s, PRICE: %.2f, SIZE: %.2f' % (str(self), order.data._name, order.executed.price, order.executed.size))

		if (order.status in [order.Canceled, order.Margin, order.Rejected]):
			self.log('Order Canceled/Margin/Rejected')

	def next(self):
		"""
		Ejecuta la lógica de compra/venta para cada activo en cada paso.

		Verifica condiciones de compra y venta, gestiona posiciones y crea órdenes.
		"""

		# Itera por todos los datafeeds
		for name in self.getdatanames():

			data = self.getdatabyname(name)
			
			current_price = data.close[0]

			position = self.strategy_position.get(name)

			# Verifica si la estrategia debe comprar
			if (self.condition_for_buy(name) and position == 0):
				
				size = self.get_size_to_buy(current_price)

				if (size > 0):
					self.buy(data=data, size=size)
					self.log('STRATEGY %s, BUY CREATE FOR %s, PRICE: %.2f, SIZE: %.2f' % (str(self), name, current_price, size))

			# Verifica si la estrategia debe vender
			elif (self.condition_for_sell(name) and position > 0):
				self.sell(data=data, size=position)
				self.log('STRATEGY %s, SELL CREATE FOR %s, PRICE: %.2f, SIZE: %.2f' % (str(self), name, current_price, position))