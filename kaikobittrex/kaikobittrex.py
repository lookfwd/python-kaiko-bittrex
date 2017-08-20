#!/usr/bin/env python

import csv
import datetime
import gzip
import os.path
import re

from collections import defaultdict
from collections import namedtuple
from itertools import permutations

# in the quote currency (on a BTCEUR pair, the price is provided in EUR)
# n the base currency (on a BTCEUR pair, the amount is in BTC)
Pair = namedtuple('Pair', "base, quote")


Record = namedtuple('Record', ("id, exchange, symbol, date, price, "
                               "amount, sell, datetime, pair"))


class Index(object):
    '''
    A class that provides an index to a Bittrex archive dataset. It provides
    validation and easier access to datapoints.
    '''

    def __init__(self, fileio):
        '''
        Loads an index to Bittrex data out of a csv input stream.
        '''
        self.index = defaultdict(
                                lambda: defaultdict(lambda: defaultdict(list)))
        self.pairs = []
        spamreader = csv.reader(fileio, dialect=csv.excel)
        for fname, in spamreader:
            year, month, day, pair = Index.parse_fname(fname)
            self.index[year][month][day].append(pair)
            self.pairs.append(pair)
        self._build_clean_pairs()

    @staticmethod
    def from_file(fname='index.csv'):
        '''
        To build 'index.csv' do:
        'find Bittrex -type f | grep -v ".DS_Store" > index.csv'
        '''
        with open(fname, 'rb') as csvfile:
            return Index(csvfile)

    def _build_clean_pairs(self):
        '''
        Traverses the index. Finds out all pairs and detects the base-coins out
        of them using a simple heuristic (assuming that any coin will be traded
        with BTC or ETH). It then generates a mapping from lowercase pair to
        a pair structure that has the quote and the base coin.
        '''
        clean = set()
        clean.add('BTC')
        clean.add('ETH')
        clean.add('DBTC')
        for pair in self.pairs:
            if 'ETH' in pair:
                clean.add(pair.replace('ETH', ''))
            if 'BTC' in pair:
                clean.add(pair.replace('BTC', ''))

        # Build a dict from pair string to pair
        pair_permutations = permutations(clean, 2)
        all_pairs = dict(("{}{}".format(*p), p) for p in pair_permutations)
        self.pairs_map = {}
        for pair in self.pairs:
            assert pair in all_pairs, "'{}' doesn't exist.".format(pair)
            self.pairs_map[pair.lower()] = Pair(*all_pairs[pair])

    def process_all(self, f):
        '''
        Calls a function 'f' for each pair for every year/month/day. It also
        provides the unziped file as an argument ready to be read.
        '''
        for year in self.index:
            for month in self.index[year]:
                for day in self.index[year][month]:
                    self.process_day(year, month, day, f)

    def process_day(self, year, month, day, f):
        '''
        Calls a function 'f' for each pair for the given year/month/day. It
        also provides the unziped file as an argument ready to be read.
        '''
        for pair in self.index[year][month][day]:
            self.process_pair(year, month, day, pair, f)

    def process_pair(self, year, month, day, pair, f):
        '''
        Calls a function 'f' for the given year/month/day/pair. It also
        provides the unziped file as an argument ready to be read.
        '''
        fname = Index.filename(pair, year, month, day)
        assert os.path.isfile(fname), "'{}' doesn't exist".format(fname)
        with gzip.open(fname, 'rb') as fhandle:
            f(year, month, day, pair, fhandle)

    def parse_line(self, line):
        '''
        Parses a single line from a file and returns a 'Record'.
        '''
        id, exchange, symbol, date, price, amount, sell = line.split(',')
        id, date = map(int, (id, date))
        price, amount = map(float, (price, amount))
        assert sell in ('true', 'false')
        sell = sell == 'true'
        thedatetime = datetime.datetime.fromtimestamp(date / 1000.0)
        pair = self.pairs_map[symbol]
        return Record(id, exchange, symbol, date, price, amount,
                      sell, thedatetime, pair)

    @staticmethod
    def parse_fname(fname):
        '''
        Helper function that parses the filename from an index file.
        '''
        parts = fname.split('/')
        assert len(parts) == 4, "'{}' is broken".format(fname)
        fname = parts[3]
        fmt = r'Bittrex_([^_]+)_trades_(\d+)_(\d+)_(\d+)\.csv\.gz'
        m = re.match(fmt, fname)
        assert m, "'{}' doesn't match".format(fname)
        pair, year, month, day = [m.group(i) for i in range(1, 5)]
        year, month, day = map(int, (year, month, day))
        return year, month, day, pair

    @staticmethod
    def filename(pair, year, month, day):
        '''
        Helper function that creates a filename out of a given year/month/day.
        '''
        fmt = ("Bittrex/{0}/{1}_{2:02d}/Bittrex_{0}_"
               "trades_{1}_{2:02d}_{3:02d}.csv.gz")
        return fmt.format(pair, year, month, day)
