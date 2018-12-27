# coding: utf-8

import glob
import pandas as pd
import re
import datetime

from kakeibo.import_data import import_data
from kakeibo.plot import plot_gas_and_electricity
from kakeibo.analyse import sum_by_month
from kakeibo.analyse import sum_by_shop


rakuten_dir = "data/rakuten"
jwest_dir = "data/jwest"
lawson_dir = "data/lawson"


data_rakuten = import_data(rakuten_dir, data_type='rakuten')
data_jwest = import_data(jwest_dir, data_type='jwest')
data_lawson = import_data(lawson_dir, data_type='lawson')

print('楽天カード')
sum_by_shop(data_rakuten)

print('\n\nJ-WESTカード')
sum_by_shop(data_jwest)

print('\n\nJMBローソンPontaカード')
sum_by_shop(data_lawson)

print('\n\nAll cards total')
data_all = data_rakuten+data_jwest+data_lawson
data_all = sorted(data_all, key=lambda x: x.date)
sum_by_month(data_all, datetime.datetime(2017, 4, 1), datetime.datetime(2019, 4, 1))

print('電気・ガス料金')

plot_gas_and_electricity(data_all)
