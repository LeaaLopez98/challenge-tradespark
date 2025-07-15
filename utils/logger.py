import csv
import os

class Logger:

	FILE = 'output/logs.csv'
	header = ['date', 'strategy', 'action', 'status', 'ticker', 'price', 'size', 'portfolio value']

	@staticmethod
	def delete_csv():
		if os.path.isfile(Logger.FILE):
			os.remove(Logger.FILE)

	@staticmethod
	def write_csv(row):

		dir_path = os.path.dirname(Logger.FILE)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path, exist_ok=True)
			
		file_exists = os.path.isfile(Logger.FILE)
		with open(Logger.FILE, 'a', newline='') as file:
			writer = csv.writer(file)
			if not file_exists:
				writer.writerow(Logger.header)

			writer.writerow(row)