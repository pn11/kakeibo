#coding: utf-8

from kakeibo.dictionary import *

def sum_by_shop(data_list):
    # 店ごとに足し合わせる

    data_dict = {}

    for data in data_list:
        key = identify_name(data.shop)
        data_dict[key] = data_dict.get(key, 0) + data.charge

    # 高い順にソート
    for k, v in sorted(data_dict.items(), key=lambda x: -x[1]):
        print(str(k) + ": " + str(v))

    # 全額足し合わせ
    sum = 0.
    for data in data_list:
        sum += data.charge

    print("合計: " + str(sum))


def sum_by_month(data_list, from_date, to_date):
    # 月ごとに足し合わせる

    sum_dict = {}

    for data in data_list:
        if (data.date >= from_date and data.date <= to_date):
            year_month = data.year * 100 + data.month
            sum_dict[year_month] = sum_dict.get(year_month, 0) + data.charge
    
    for k, v in sorted(sum_dict.items()):
        print(str(k//100) + "/" + str(k%100)+ ": " + str(v))
    
    sum = 0.
    for k, v in sum_dict.items():
        sum += v
    print(str(from_date) + " - " + str(to_date) +" 合計:" + str(sum))
