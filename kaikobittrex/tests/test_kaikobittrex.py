#!/usr/bin/env python

import unittest

from StringIO import StringIO
from kaikobittrex import Index


class TestIndex(unittest.TestCase):

    def setUp(self):
        data = StringIO("\n".join((
          "Bittrex/2GIVEBTC/2016_10/Bittrex_2GIVEBTC_trades_2016_10_01.csv.gz",
          "Bittrex/2GIVEBTC/2016_10/Bittrex_2GIVEBTC_trades_2016_10_02.csv.gz",
          "Bittrex/2GIVEBTC/2016_10/Bittrex_2GIVEBTC_trades_2016_10_03.csv.gz",
          "Bittrex/XZCBTC/2016_12/Bittrex_XZCBTC_trades_2016_12_05.csv.gz",
          "Bittrex/MAIDBTC/2017_08/Bittrex_MAIDBTC_trades_2017_08_02.csv.gz",
        )))

        self.index = Index(data)

    def test_index(self):
        index = self.index

        self.assertTrue(2016 in index.index)
        self.assertTrue(2017 in index.index)

        self.assertTrue(10 in index.index[2016])
        self.assertTrue(12 in index.index[2016])
        self.assertTrue(8 in index.index[2017])

        self.assertTrue(1 in index.index[2016][10])
        self.assertTrue(2 in index.index[2016][10])
        self.assertTrue(3 in index.index[2016][10])
        self.assertTrue(5 in index.index[2016][12])
        self.assertTrue(2 in index.index[2017][8])

        self.assertTrue(['2GIVEBTC'] == index.index[2016][10][1])
        self.assertTrue(['2GIVEBTC'] == index.index[2016][10][2])
        self.assertTrue(['2GIVEBTC'] == index.index[2016][10][3])
        self.assertTrue(['XZCBTC'] == index.index[2016][12][5])
        self.assertTrue(['MAIDBTC'] == index.index[2017][8][2])

        self.assertTrue(index.pairs_map['2givebtc'].base == '2GIVE')
        self.assertTrue(index.pairs_map['2givebtc'].quote == 'BTC')
        self.assertTrue(index.pairs_map['xzcbtc'].base == 'XZC')
        self.assertTrue(index.pairs_map['xzcbtc'].quote == 'BTC')
        self.assertTrue(index.pairs_map['maidbtc'].base == 'MAID')
        self.assertTrue(index.pairs_map['maidbtc'].quote == 'BTC')

    def test_parse_line(self):
        line = "35728026,bt,maidbtc,1503014482990,0.00009897,500,false"
        record = self.index.parse_line(line)
        self.assertTrue(record.id == 35728026)
        self.assertTrue(record.exchange == 'bt')
        self.assertTrue(record.symbol == 'maidbtc')
        self.assertTrue(record.date == 1503014482990)
        self.assertTrue(abs(record.price - 0.00009897) < 0.0001)
        self.assertTrue(abs(record.amount - 500) < 0.0001)
        self.assertTrue(record.sell is False)
        self.assertTrue(record.datetime.year == 2017)
        self.assertTrue(record.datetime.month == 8)
        self.assertTrue(record.datetime.day == 17)
        self.assertTrue(record.datetime.hour == 20)
        self.assertTrue(record.datetime.minute == 1)
        self.assertTrue(record.datetime.second == 22)
        self.assertTrue(record.datetime.microsecond == 990000)
        self.assertTrue(record.pair.base == "MAID")
        self.assertTrue(record.pair.quote == "BTC")

if __name__ == '__main__':
    unittest.main()
