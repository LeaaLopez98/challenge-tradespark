import csv
import os

class Logger:

	FILE = 'output.csv'
	header = ['date', 'strategy', 'action', 'status', 'ticker', 'price', 'size', 'portfolio value']

	@staticmethod
	def delete_csv():
		if os.path.isfile(Logger.FILE):
			os.remove(Logger.FILE)

	@staticmethod
	def write_csv(row):
		file_exists = os.path.isfile(Logger.FILE)
		with open(Logger.FILE, 'a', newline='') as file:
			writer = csv.writer(file)
			if not file_exists:
				writer.writerow(Logger.header)

			writer.writerow(row)