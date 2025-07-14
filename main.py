import backtrader as bt
import datetime
from price_crossover import PriceCrossover
from golden_cross import GoldenCross

cerebro = bt.Cerebro()

datafeeds = ['AAPL', 'GOOG', 'MSFT', 'TSLA']

for d in datafeeds:
  data = bt.feeds.YahooFinanceCSVData(
    dataname=f'datafeeds/{d}.csv',
    fromdate=datetime.datetime(2021, 1, 1),
    todate=datetime.datetime(2021, 12, 31),
    reversed=False
  )
  cerebro.adddata(data)

cerebro.broker.setcash(100000)

#cerebro.addstrategy(PriceCrossover)
cerebro.addstrategy(GoldenCross)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())