# Kaiko - Bittrex Python index
A python module that provides easier access to the Kaiko Bittrex Historical trade data. Assuming that you've bought the files from [here](https://www.kaiko.com/products/bittrex-historical-trade-data), you can now use these (relativelly) simple 2 steps to process them.

1. Create an `index.csv` file. We assume that you have unziped the file and when you `ls Bittrex` you see the pairs e.g. `2GIVEBTC`, `8BITBTC` etc. Then you run: `find Bittrex -type f | grep -v ".DS_Store" > index.csv` and an `index.csv` file must have been created for you. This file has all the `.csv.gz` files of the archive.
2. When you install with `pip install kaikobittrex`, you can create an `Index` object from Python and access the content of those files like this:


```
#!/usr/bin/env python

from kaikobittrex import Index

idx = Index.from_file()

def process_pair(year, month, day, pair, f):
    for lineno, line in enumerate(f.readlines()):
        line = line.strip()
        if lineno == 0:
            assert line == "id,exchange,symbol,date,price,amount,sell"
        else:
            record = idx.parse_line(line)
            print record

idx.process_all(process_pair)
```

There are additional `process_*` methods that allow you to process subset of those data. `process_day(self, year, month, day, f)` and `process_pair(self, year, month, day, pair, f)` all take the same type of callback argument `f` and process the subset of records you defined. The `Index` object also exposes the `index` member which has records for given date/pair, the `pairs` member that has all available pairs and the `pairs_map` member that maps pairs to coin base/quote pairs. See the test file for more details.

## Notes

To release `python setup.py sdist`, `twine upload dist/*`.
