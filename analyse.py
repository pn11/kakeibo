# coding: utf-8

import glob
import pandas as pd
import re
import datetime

rakuten_dir = "data/rakuten"
jwest_dir = "data/jwest"
lawson_dir = "data/lawson"


class ChargeData:
    year = 0
    month = 0
    day = 0
    date = datetime.datetime(1970, 1, 1)
    is_new_signature = True
    user = ""
    shop = ""
    payment_method = ""
    charge = 0.0
    payment_fee = 0.0
    total_payment_amount = 0.0
    total_paying_time = 0
    current_paying_time = 0
    charge_for_this_month = 0.0
    charge_left_for_next_month = 0.0
    notes = ""

    def print(self):
        print(str(self.year) + "/" + str(self.month) + "/" + str(self.day) +
              " " + str(self.charge) + " 円 @ " + str(self.shop))

    def create_date(self):
        self.date = datetime.datetime(self.year, self.month, self.day)


# 名寄せ用辞書
name_id_dict = {
    "関西電力": "関西電力",
    "大阪ガス": "大阪ガス",
    "ｼﾞ-ﾕ-": "ジーユー",
    "ＥＴＣ": "ETC",
    "ソフトバンク": "ソフトバンク",
    "ＡＭＡＺＯＮ　ＤＯＷＮＬＯＡＤＳ": "Kindle Unlimited / Amazon Prime",
    "Ａｍａｚｏｎ　Ｄｏｗｎｌｏａｄｓ": "Kindle Unlimited / Amazon Prime",
}


def identify_name(input_str):
    # 名寄せと可読性の向上をする

    for k, v in name_id_dict.items():
        if input_str.find(k) != -1:
            return v

    return input_str

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


def import_rakuten():
    filenames = glob.glob(rakuten_dir + "/*.csv")
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


def import_jwest():
    filenames = glob.glob(jwest_dir + "/*.csv")
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


def import_lawson():
    filenames = glob.glob(lawson_dir + "/*.csv")
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


data_rakuten = import_rakuten()
data_jwest = import_jwest()
data_lawson = import_lawson()

print('楽天カード')
sum_by_shop(data_rakuten)

print('\n\nJ-WESTカード')
sum_by_shop(data_jwest)

print('\n\nJMBローソンPontaカード')
sum_by_shop(data_lawson)

print('\n\nAll cards total')
data_all = data_rakuten+data_jwest+data_lawson
sum_by_month(data_all, datetime.datetime(2000, 4, 1), datetime.datetime(2018, 3, 31))

