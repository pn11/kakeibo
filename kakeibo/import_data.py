# coding: utf-8

import re
import glob
import pandas as pd
from kakeibo.charge_data import ChargeData

rakuten_dir = "data/rakuten"
jwest_dir = "data/jwest"
lawson_dir = "data/lawson"

def import_data(dir, data_type):
    data_list = []
    if data_type == 'rakuten':
        data_list = import_rakuten(dir)
    elif data_type == 'jwest':
        data_list = import_jwest(dir)
    elif data_type == 'lawson':
        data_list == import_lawson(dir)
    else:
        data_list = None
    return data_list

def import_rakuten(dir):
    filenames = glob.glob(dir + "/*.csv")
    df = None

    for f in filenames:
        df_tmp = pd.read_csv(f, encoding="Shift-JIS")
        if df is None:
            df = df_tmp
        else:
            df = pd.concat([df, df_tmp])

    datalist = []

    for _, row in df.iterrows():
        date = str(row[u"利用日"]).rstrip()
        if date == "nan":
            continue  # 変換レートの行をスキップ # TODO

        data = ChargeData()
        split = date.split(".")
        data.year = int(split[0]) + 2000
        data.month = int(split[1])
        data.day = int(split[2])
        data.create_date()
        data.charge = float(row[u"利用金額"])
        data.is_new_signature = str(row[u"新規サイン"])
        data.user = str(row[u"利用者"])
        data.shop = str(row[u"利用店名・商品名"])
        data.payment_method = str(row[u"支払方法"])
        data.charge = float(row[u"利用金額"])
        data.payment_fee = float(row[u"支払手数料"])
        data.total_payment_amount = float(row[u"支払総額"])
        payment_time = str(row[u"支払回数/何回目"]).rstrip().split("/")
        data.total_paying_time = str(payment_time[0])
        data.current_paying_time = str(payment_time[1])
        data.charge_for_this_month = float(row[u"当月請求額"])
        data.charge_left_for_next_month = float(row[u"翌月繰越残高"])

        datalist.append(data)

    return datalist


def import_jwest(dir):
    filenames = glob.glob(dir + "/*.csv")
    df = None

    for f in filenames:
        df_tmp = pd.read_csv(f, encoding="Shift-JIS")
        if df is None:
            df = df_tmp
        else:
            df = pd.concat([df, df_tmp])

    datalist = []

    for _, row in df.iterrows():
        date = str(row[u"ご利用日"]).rstrip()
        if date == "nan":
            continue  # データじゃない行をスキップ

        data = ChargeData()
        
        split = re.split('[年月日]', date)
        data.year = int(split[0])
        data.month = int(split[1])
        data.day = int(split[2])
        data.create_date()
        data.user = str(row[u"ご利用者"])
        data.shop = str(row[u"ご利用店名（海外ご利用店名／海外都市名）"])
        data.charge = float(row[u"ご利用金額（円）"].replace(',', ''))
        data.notes = str(row[u"現地通貨額・通貨名称・換算レート"])

        datalist.append(data)

    return datalist


def import_lawson(dir):
    filenames = glob.glob(dir + "/*.csv")
    df = None

    for f in filenames:
        df_tmp = pd.read_csv(f, encoding="Shift-JIS", skiprows=4)
        if df is None:
            df = df_tmp
        else:
            df = pd.concat([df, df_tmp])

    datalist = []

    for _, row in df.iterrows():
        date = str(row[u"利用日"]).rstrip()
        if date == "nan":
            continue  # データじゃない行をスキップ

        data = ChargeData()
        
        split = re.split('[/]', date)
        data.year = int(split[0])
        data.month = int(split[1])
        data.day = int(split[2])
        data.create_date()
        data.user = str(row[u"本人・家族区分"])
        data.shop = str(row[u"ご利用店名及び商品名"])
        data.charge = float(row[u"利用金額"])
        data.notes = str(row[u"備考"])

        datalist.append(data)

    return datalist

