# coding: utf-8

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
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
    # ToDo: Use pandas.Series instead of dictionary.

    sum_dict = {}

    for data in data_list:
        if (data.date >= from_date and data.date <= to_date):
            year_month = data.year * 100 + data.month
            sum_dict[year_month] = sum_dict.get(year_month, 0) + data.charge

    for k, v in sorted(sum_dict.items()):
        print(str(k//100) + "/" + str(k % 100) + ": " + str(v))

    sum = 0.
    for k, v in sum_dict.items():
        sum += v
    print(str(from_date) + " - " + str(to_date) + " 合計:" + str(sum))


def create_monthly_report(data_dict_list, year, month, notebook=False):
    '''
    月別の内訳を作成する。
    '''

    df = get_month_data(data_dict_list, year, month)
    if len(df) == 0:
        return df

    df = merge_same_shop(df)
    plt.figure()
    df_for_plot = df[df['Charge']>0.0] # 合計がマイナスのものはプロットしない
    df_for_plot.plot(kind='pie', y = 'Charge',
            counterclock=False, startangle=90,
            shadow=False, labels=df['Shop'], legend = False, fontsize=14,
            autopct='%1.1f%%', figsize=(10, 10))
    plt.title(f"{year}/{month}", fontsize = 22)

    if notebook:
        plt.show()
    if not notebook:
        plt.savefig('piechart-{}-{}.png'.format(year, month))
        plt.close('all')

    return df

def get_month_data(data_dict_list, year, month):
    '''
    指定した月のデータのみを含む DataFrame を作成する。
    '''
    if month < 1 or month > 12:
        raise ValueError("Month have to be from 1 to 12")

    df = pd.DataFrame.from_records(data_dict_list)

    df = df[df["Date"] >= datetime.datetime(year, month, 1)]

    if month == 12:
        df = df[df["Date"] < datetime.datetime(year+1, 1, 1)]
    else:
        df = df[df["Date"] < datetime.datetime(year, month+1, 1)]

    return df


def merge_same_shop_(data_dict_list):
    # Shop が同じものを一つにまとめる。
    merged_dict = {}

    for dic in data_dict_list:
        merged_dict[dic["Shop"]] = merged_dict.get(dic["Shop"], 0) + dic["Charge"]
    
    print(merged_dict)


def merge_same_shop(df):
    # Shop が同じものを一つにまとめる。
    merged_dict = {}

    for rec in df.itertuples():
        shop_name = rec.Shop
        charge = rec.Charge
        merged_dict[shop_name] = merged_dict.get(shop_name, 0) + charge
    
    shops = []
    charges = []

    for k, v in merged_dict.items():
        shops.append(k)
        charges.append(v)
    
    df = pd.DataFrame({"Charge": charges, "Shop": shops}).sort_values('Charge', ascending=False).reset_index(drop=True)

    return df
    

