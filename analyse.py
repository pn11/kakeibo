# coding: utf-8

import glob
import pandas as pd


rakuten_dir = "data/rakuten"


class ChargeData:
    year = 0
    month = 0
    day = 0
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

    def print(self):
        print(str(self.year) + "/" + str(self.month) + "/" + str(self.day) +
              " " + str(self.charge) + " 円" + "@ " + str(self.shop))


# 名寄せ用辞書
name_id_dict = {
    "関西電力": "関西電力",
    "大阪ガス": "大阪ガス",
    "ｼﾞ-ﾕ-": "ジーユー"
}


def identify_name(input_str):
    # 名寄せと可読性の向上をする

    for k, v in name_id_dict.items():
        if input_str.find(k) != -1:
            return v

    return input_str


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


data_rakuten = import_rakuten()

dict_rakuten = {}

# 店ごとに足し合わせる
for data in data_rakuten:
    key = identify_name(data.shop)
    dict_rakuten[key] = dict_rakuten.get(key, 0) + data.charge

# 高い順にソート
for k, v in sorted(dict_rakuten.items(), key=lambda x: -x[1]):
    print(str(k) + ": " + str(v))

# 全額足し合わせ
sum = 0.
for data in data_rakuten:
    sum += data.charge

print("合計: " + str(sum))