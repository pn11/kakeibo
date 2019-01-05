# coding: utf-8

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
