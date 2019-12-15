# 家計簿

## 概要

クレジットカード明細とかを解析する。要 Python3, Pandas, Matplotlib。

- 楽天カード (Master)
- J-WESTカード (VISA)
- JMBローソンPontaセゾンカード (VISA)

を処理できる。PiTaPa、Edy とかもやる予定。

## 前提条件

### ライブラリのインストール

```sh
pip install pandas matplotlib mojimoji
```

### データ

`kakeibo-data` にデータを置いておく。以下のような感じ。

```txt
.
├── edy
│   ├── edy_201802.csv
        中略
│   ├── edy_201805.csv
│   └── get_edy_data.py
├── jwest
│   ├── 201603.csv
        中略
│   └── 201902.csv
├── lawson
│   ├── SAISON_1706.csv
        中略
│   └── SAISON_1902.csv
└── rakuten
    ├── enavi201705(6999).csv
    ├── enavi201706(6999).csv
        以下略
```

## 動かし方

```
python analyse_demo.py
```

でデモ。`kakeibo` の中のモジュールで処理を行う。

## 課題

- たまにおかしいファイルとか、フォーマットの変更には手動で修正する必要がある。
  - せめてどこでエラーが出ているか分かりやすいようにしたい。
- クレジットカード明細をダウンロードしてくるのがめんどくさい。
  - そのあたりは MoneyForward とかには勝てない。
  - Seleinum や Splinter でどうにかしようにも画像認証とかある場合は無理。

## その他

- [楽天 Edy データの作成方法](docs/edy.md)
