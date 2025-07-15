import backtrader as bt
import datetime
from utils.logger import Logger
from strategies.price_crossover import PriceCrossover
from strategies.golden_cross import GoldenCross

Logger.delete_csv()

cerebro = bt.Cerebro()

datafeeds = ['AAPL', 'GOOG', 'MSFT', 'TSLA']

# Agrega los datafeeds al cerebro
for d in datafeeds:
  data = bt.feeds.YahooFinanceCSVData(
    dataname=f'datafeeds/{d}.csv',
    fromdate=datetime.datetime(2021, 1, 1),
    todate=datetime.datetime(2021, 12, 31),
    reversed=False
  )
  cerebro.adddata(data)

# Setea el valor inicial del portfolio
cerebro.broker.setcash(100000)


# Agrega cada una de las estrategias
cerebro.addstrategy(PriceCrossover, period=10)
cerebro.addstrategy(PriceCrossover, period=30)
cerebro.addstrategy(GoldenCross)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())