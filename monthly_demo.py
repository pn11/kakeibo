# coding: utf-8

import glob
import pandas as pd
import re
import datetime

from kakeibo.import_data import import_data
from kakeibo.plot import plot_gas_and_electricity
from kakeibo.analyse import sum_by_month
from kakeibo.analyse import sum_by_shop
from kakeibo.analyse import create_monthly_report


rakuten_dir = "kakeibo-data/rakuten"
jwest_dir = "kakeibo-data/jwest"
lawson_dir = "kakeibo-data/lawson"


data_rakuten = import_data(rakuten_dir, data_type='rakuten')
data_jwest = import_data(jwest_dir, data_type='jwest')
data_lawson = import_data(lawson_dir, data_type='lawson')

data_all = data_rakuten+data_jwest+data_lawson
data_all = sorted(data_all, key=lambda x: x.date)
dict_all = [a.to_dict() for a in data_all]

print(create_monthly_report(dict_all, 2018, 8))
print(create_monthly_report(dict_all, 2018, 9))
print(create_monthly_report(dict_all, 2018, 10))
print(create_monthly_report(dict_all, 2018, 11))