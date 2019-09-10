# coding: utf-8

# 名寄せ用辞書 (keyを一部として含まれるレコードは全てvalueで置き換えられる。)
# 例: 「関西電力 2017/01」 → 「関西電力」
name_id_dict = {
    "関西電力": "関西電力",
    "大阪ガス": "大阪ガス",
    "ソフトバンク": "ソフトバンク",
    "ＡＭＡＺＯＮ　ＤＯＷＮＬＯＡＤＳ": "Kindle Unlimited / Amazon Prime",
    "Ａｍａｚｏｎ　Ｄｏｗｎｌｏａｄｓ": "Kindle Unlimited / Amazon Prime",
    "AMAZON DOWNLOADS": "Kindle Unlimited / Amazon Prime",
    "Amazonプライム会費": "Kindle Unlimited / Amazon Prime",
    "アマゾンプライムカイヒ":  "Kindle Unlimited / Amazon Prime",

    "チケットピア": "チケットぴあ",
    "センタクビン": "せんたく便",

    "イオン フシミ": "イオン伏見",
    "イオンモ-ルキヨウト": "イオンモール京都",
    "キヨウトセイカツキヨウドウクミ": "京都COOP",

    "アイアイジエイサ-ビスリヨウ": "IIJサービス料",
    "サクラインタ-ネツト": "さくらインターネット",

    "JRヒガシニホン ミドリノマ": "JR東日本みどりの窓口",
    "ニシニホンジエイア-ルバスネ": "西日本JRバスネット"
}


def identify_name(input_str):
    # 名寄せと可読性の向上をする

    for k, v in name_id_dict.items():
        if input_str.find(k) != -1:
            return v

    return input_str
