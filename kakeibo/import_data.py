# coding: utf-8
import glob
import logging
import mojimoji
import pandas as pd
import re

from kakeibo.charge_data import ChargeData

rakuten_dir = "data/rakuten"
jwest_dir = "data/jwest"
lawson_dir = "data/lawson"


invalid_characters = ['㈱']

def parse_number(number_str):
    '''カンマを含む数値の文字列をfloatに変換'''
    if type(number_str) == float:
        # float だった場合はそのまま返す
        return number_str
    elif type(number_str) == int:
        return float(number_str)
    elif ',' in number_str:
        number_str = number_str.replace(',', '')
    return float(number_str)


def parse_str(str_):
    '''カタカナは全角に、英字、数字は半角に統一'''
    if type(str_) != str:
        str_ = str(str_)
    return mojimoji.han_to_zen(mojimoji.zen_to_han(str_, kana=False), digit=False, ascii=False)


def import_data(dir, data_type):
    data_list = []
    if data_type == 'rakuten':
        data_list = import_rakuten(dir)
    elif data_type == 'jwest':
        data_list = import_jwest(dir)
    elif data_type == 'lawson':
        data_list = import_lawson(dir)
    else:
        data_list = None
    return data_list


def import_rakuten(dir):
    filenames = glob.glob(dir + "/*.csv")
    df = None

    for f in filenames:
        try:
            df_tmp = pd.read_csv(f, encoding="Shift-JIS")
        except UnicodeDecodeError:
            import codecs
            i = 0
            f2 = codecs.open(f, encoding='shift-jis')
            try:
                for i, line in enumerate(f2):
                    pass
            except:
                logging.error(f'{f}: {i+2}行目に無効な全角文字(例:{invalid_characters})が含まれています。')
            exit(-1)
        if df is None:
            df = df_tmp
        else:
            df = pd.concat([df, df_tmp], sort=True)

    datalist = []
    if df is None:
        return datalist

    for _, row in df.iterrows():
        date = str(row[u"利用日"]).rstrip()
        if date == "nan":
            continue  # 変換レートの行をスキップ # TODO

        data = ChargeData()
        split1 = date.split(".")
        split2 = date.split("/")
        if len(split1) > 1:
            data.year = int(split1[0]) + 2000
            data.month = int(split1[1])
            data.day = int(split1[2])
        elif len(split2):
            data.year = int(split2[0])
            data.month = int(split2[1])
            data.day = int(split2[2])
        else:
            raise ValueError("未知のCSVフォーマット")
        data.create_date()
        data.charge = parse_number(row[u"利用金額"])
        data.is_new_signature = str(row[u"新規サイン"])
        data.user = parse_str(row[u"利用者"])
        data.shop = parse_str(row[u"利用店名・商品名"])
        data.payment_method = parse_str(row[u"支払方法"])
        data.charge = parse_number(row[u"利用金額"])
        data.payment_fee = parse_number(row[u"支払手数料"])
        data.total_payment_amount = parse_number(row[u"支払総額"])

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
            df = pd.concat([df, df_tmp], sort=True)

    datalist = []
    if df is None:
        return datalist

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
        data.user = parse_str(row[u"ご利用者"])
        data.shop = parse_str(row[u"ご利用店名（海外ご利用店名／海外都市名）"])
        data.charge = parse_number(row[u"ご利用金額（円）"])
        data.notes = parse_str(row[u"現地通貨額・通貨名称・換算レート"])

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
            df = pd.concat([df, df_tmp], sort=True)

    datalist = []
    if df is None:
        return datalist

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
        data.user = parse_str(row[u"本人・家族区分"])
        data.shop = parse_str(row[u"ご利用店名及び商品名"])
        data.charge = parse_number(row[u"利用金額"])
        data.notes = parse_str(row[u"備考"])

        datalist.append(data)

    return datalist
