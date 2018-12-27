# 家計簿

## 概要

クレジットカード明細とかを解析する。要 Python3, Pandas, Matplotlib。

- 楽天カード (Master)
- J-WESTカード (VISA)
- JMBローソンPontaセゾンカード (VISA)

を処理できる。PiTaPa、Edy とかもやる予定。

##　動かし方

```
python analyse_demo.py
```

でデモ。`kakeibo` の中のモジュールで処理を行う。

## 課題

- たまにおかしいファイルとか、フォーマットの変更には手動で修正する必要がある。
  - せめてどこでエラーが出ているか分かりやすいようにしたい。
- クレジットカード明細をダウンロードしてくるのがめんどくさい。
  - そのあたりは MoneyForward とかには勝てない。
  - Splinter でどうにかしようにも画像認証とかある場合は無理。

## その他

- [楽天カードフォーマットについて](docs/rakuten_format.md)
- [楽天 Edy データの作成方法](docs/edy.md)
