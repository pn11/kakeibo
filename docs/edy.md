# 楽天 Edy データの作成方法

- [楽天Edyのサイトから利用履歴を取得したい - Yomanoma](http://blog.yomak.info/2015/07/rakutenedy_csv.html)

こちらで紹介されているスクリプトを使わさせて頂いた。

splinter というライブラリで自動でブラウザが動いて HTML を読み込むので、それをパースしてデータを持ってきてくれる。私の環境では、splinter と ChromeDriver が入ってなかったので入れた。

```
pip install splinter
brew tap homebrew/cask
brew cask install chromedriver
```

また、そのままだと料金が `3,500` とかになっている場合に CSV のカンマと区別できないのでカンマを除く処理を加えた。あと、引数の処理を加えたのと出力先をファイルに変更した。元のコードのライセンスが分からないのでこのリポジトリには入れず、 Fork して Gist に置いおいた。→ [rakutenedy_csv.py](https://gist.github.com/pn11/d6a77e60d6412edcfa7320600c0b784b)
