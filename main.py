import backtrader as bt
import datetime
from price_crossover import PriceCrossover
from golden_cross import GoldenCross

cerebro = bt.Cerebro()

data = bt.feeds.YahooFinanceCSVData(
  dataname='datafeeds/AAPL.csv',
  fromdate=datetime.datetime(2021, 1, 1),
  todate=datetime.datetime(2021, 12, 31),
  reversed=False
)

cerebro.broker.setcash(100000)

cerebro.adddata(data)

cerebro.addstrategy(PriceCrossover)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())