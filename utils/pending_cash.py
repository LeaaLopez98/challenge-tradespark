class CashReservation:
	"""
	Clase para gestionar la reserva de fondos pendientes.
	"""

	def __init__(self):
		self.total_amount = 0
		self.references = {}

	def reserve(self, ref, amount):
		self.total_amount += amount
		self.references[ref] = amount

	def release(self, ref):
		self.total_amount -= self.references.get(ref)
		del self.references[ref]

	def get_amount(self):
		return self.total_amount
	
pending_cash = CashReservation()