# StockPriceAnalysis

## 前提ソフトウェア
* Docker

## 起動方法

```
$ cd docker
$ docker-compose up -d
```

|コンテナ|役割|
----|----
|phpmyadmin|データベースをGUIで参照・操作するためのツール。http://localhost:8888/ でアクセスする。|
|redis|一部の計算結果を一時保存する領域として使用する。dockerを終了するとデータは消える。|
|mysql|ヒストリカルデータを保存しているデータベース。設定を変えることでdocker停止後も保存できるがデフォルトだと保存しない。|
|client|アプリケーション実行の端末用コンテナ。|

## アプリケーション起動方法
```
$ docker exec -it client bash
# python3 -m app.application
### Welcome to Stock Price Analysis!!! ###
(command)>> 
```

## コマンド説明

### 基本コマンド

|コマンド名|フォーマット|説明|
----|----|----
|help|`help`|全コマンドの使い方を出力する。|
|quit|`quit`|コマンドラインを抜ける。|
|load|`load /path/to/the/csvfile`|ヒストリカルデータのCSVファイルを読み込んでデータベースに保存する。形式は後述。既存のデータベース上に銘柄と日付が同一の異なるデータが存在した場合、画面に表示してabortする。|
|forceload|`forceload /path/to/the/csvfile`|ヒストリカルデータのCSVを強制的にデータベースに保存する。loadコマンドのチェックを省略したもの。|
|search|`search <keyword(string)>`|与えた文字列でデータベース上の銘柄名を検索する。|
|marketsearch|`marketsearch <keyword(string)>`|与えた文字列でデータベース上の市場を検索する。|
|tagsearch|`tagsearch <keyword(string)>`|与えた文字列でデータベース上のタグを検索する。|
|chart|`chart`|プリセットされたデータ(`From`/`To`/`Market`/`Ticker`)を用いて画面上にチャートを描画する。|
|sma|`sma <term(integer)>`|プリセットされたデータ(`From`/`To`/`Market`/`Ticker`)を用いて画面上に`term`日SMAのチャートを描画する。|
|wma|`wma <term(integer)>`|プリセットされたデータ(`From`/`To`/`Market`/`Ticker`)を用いて画面上に`term`日WMAのチャートを描画する。|
|ema|`ema <term(integer)>`|プリセットされたデータ(`From`/`To`/`Market`/`Ticker`)を用いて画面上に`term`日EMAのチャートを描画する。|
|ticker|`ticker <ticker(string)>`|与えたTickerシンボルをプリセットする。|
|market|`market <market(string)>`|与えたMarketシンボルをプリセットする。|
|syntax|`syntax <market(string)>:<ticker(string)>`|与えたMarketとTickerシンボルをプリセットする。|
|from|`from <date(YYYY-MM-DD)>`|与えた日付を期間の開始日付としてプリセットする。|
|to|`to <date(YYYY-MM-DD)>`|与えた日付を期間の終了日付としてプリセットする。|
|tag|`tag <tag name(strings)>`|タグをプリセットする。カンマ区切りで複数指定可能。複数指定した場合はタグが使用されるコマンドの中でOR条件で適用される。|
|tagload|`tagload /path/to/the/csvfile`|銘柄に紐づけるタグ情報をtsvファイルを読み込んでデータベースに保存する。形式は後述。|
|tagdelete|`tagdelete <tagname(string)>`|指定のタグをデータベースから削除する。|
|principal|`principal <amount(decimal)>`|プリセットデータに指定の資金を設定する。シミュレーションで使用する。|
|today|`today <date(YYYY-MM-DD) *optional>`|プリセットデータに今日の日付を設定する。シミュレーションでこの日を当日として使用する。引数省略時は実日付がセットされる。|
|listings|`listings <syntax(string)>`|指定の銘柄データを上場扱いにする。その銘柄は各コマンド実行時に対象になる。|
|delistings|`listings <syntax(string)>`|指定の銘柄データを上場廃止扱いにする。その銘柄は各コマンド実行時に対象にならない。|
|lastdate|`lastdate <order [desc/asc]> <limit(integer)> <offset(integer)>`|各銘柄のヒストリカルデータの最新の日付をソートして表示する。|
|firstdate|`firstdate <order [desc/asc]> <limit(integer)> <offset(integer)>`|各銘柄のヒストリカルデータの最初の日付をソートして表示する。|
|cacheclear|`cacheclear <cachekey(string)>`|対象のキーのキャッシュデータを削除する|
|cachemultiple|`cachemultiple <cachekey(string)> <coefficient(decimal)>`|対象のキーのキャッシュデータの値に一律係数を掛けて上書きする。|
|cacheshow|`cacheshow <cachekey(string)> <limit(integer)> <offset(integer)>`|対象のキーのキャッシュデータを表示する。|
|cachetag|`cachetag <cachekey(string)> <limit(integer)>`|対象のキーのキャッシュデータに含まれる銘柄を`cache`というタグ名で紐づけてデータベースに登録する。|
|ath|`ath <term(integer)> <basedate(YYYY-MM-DD) *optional>`|`basedate`(省略時は`Today`)を基準に`term`営業日の間の最終日終値がATHである銘柄を`Market`/`Tag`から検索して出力する。|
|atl|`atl <term(integer)> <basedate(YYYY-MM-DD) *optional>`|`basedate`(省略時は`Today`)を基準に`term`営業日の間の最終日終値がATLである銘柄を`Market`/`Tag`から検索して出力する。|
|atr|`atr <term(integer)> <basedate(YYYY-MM-DD) *optional>`|`basedate`(省略時は`Today`)を基準に`term`営業日の間のATRを計算する。対象銘柄は`Market`/`Ticker`で指定。|

### 分析コマンド

#### rank
指定したプリセットデータ、引数を使ってランキングを表形式で出力する。キャッシュをONにすると指定したキーで結果が保存される。

##### 使用するプリセットデータ
`Market`/`Tags`/`Today`

##### サブコマンド(price)

`Today`と`term`営業日前の終値を比較し、騰落率をソートして出力する。キャッシュの保存をTrueにした場合は銘柄と騰落率がキャッシュに保持される。

`rank price <order [desc/asc]> <term(integer)> <limit(integer)> <offset(integer)> <save cache[True/False]) *optional> <cachekey(string) *optional>`

#### サブコマンド(volume)

`Today`と`term`営業日前の取引量を比較し、騰落率をソートして出力する。キャッシュの保存をTrueにした場合は銘柄と騰落率がキャッシュに保持される。

`rank volume <order [desc/asc]> <term(integer)> <limit(integer)> <offset(integer)> <save cache[True/False] *optional> <cachekey(string) *optional>`

#### サブコマンド(rs)

`Today`を基準にRelative Strengthの値を比較し、値をソートして出力する。キャッシュの保存をTrueにした場合は銘柄と値がキャッシュに保持される。

`rank rs <order [desc/asc]> <limit(integer)> <offset(integer)> <save cache[True/False] *optional> <cachekey(string) *optional>`

#### サブコマンド(deviation)

`Today`を基準に`shortterm`営業日の期間における終値の標準偏差と`longterm`営業日の期間における終値の標準偏差の比率をソートして出力する。キャッシュの保存をTrueにした場合は銘柄と値がキャッシュに保持される。

`rank deviation <order [desc/asc]> <longterm(integer)> <shortterm(integer)> <limit(integer)> <offset(integer)> <save cache[True/False] *optional> <cachekey(string) *optional>`

#### trend
指定したプリセットデータ、引数を使ってSMAとの比較を表形式で出力する。キャッシュをONにすると指定したキーで結果が保存される。

##### 使用するプリセットデータ
`Market`/`Tags`/`Today`

##### サブコマンド(price)

終値の`smaterm`日SMAに上下`margin`を考える。`Today`を基準に`term`営業日の期間における終値がそれよりも上にくる件数と下にくる件数を算出して出力する。どちらの件数で降順に出力するか`sortkey`指定可能。キャッシュの保存をTrueにした場合は銘柄と値がキャッシュに保持される。

`trend price <sortkey[up/down]> <term(integer)> <smaterm(integer)> <margin(%)(integer)> <limit(integer)> <offset(integer)> <save cache[True/False] *optional> <cachekey(string) *optional>`

##### サブコマンド(volume)

取引量の`smaterm`日SMAに上下`margin`を考える。`Today`を基準に`term`営業日の期間における取引量がそれよりも上にくる件数と下にくる件数を算出して出力する。どちらの件数で降順に出力するか`sortkey`指定可能。キャッシュの保存をTrueにした場合は銘柄と値がキャッシュに保持される。

`trend volume <sortkey[up/down]> <term(integer)> <smaterm(integer)> <margin(%)(integer)> <limit(integer)> <offset(integer)> <save cache[True/False] *optional> <cachekey(string) *optional>`

##### サブコマンド(momentum)

取引量の`smaterm`日SMAに上下`margin`を考える。`Today`を基準に`term`営業日の期間における取引量がそれよりも上にくる場合に前日より終値が上がった件数と下がった件数を算出して出力する。どちらの件数で降順に出力するか`sortkey`指定可能。キャッシュの保存をTrueにした場合は銘柄と値がキャッシュに保持される。

`trend momentum <sortkey[up/down]> <term(integer)> <smaterm(integer)> <margin(%)(integer)> <limit(integer)> <offset(integer)> <save cache[True/False] *optional> <cachekey(string) *optional>`

## プリセットデータ
アプリケーション起動後、コマンド実行をするか何も入力せずにEnterを押すと以下のような画面表示がされる。

```
---------------------------------------------------------------------------------------------------------------------------------------------------
Market:                     | Ticker:                     | Tags:                                                                                 |
From:             2020-10-28| To:               2021-08-24| Today:            2021-08-24|
Principal:             10000| Commission: (Min:    0, Max: 22.2, Rate:   0.0495)|
```

`chart`などのプリセットデータを使用するコマンドが使用する。

## CSVデータ形式

以下のような形式で用意。リポジトリ直下の`stockdata`ディレクトリは`client`の`/stockdata`へマウントされている為、`stockdata`配下にcsvを配置して`load`コマンドや`forceload`コマンドで読み込む。

```
Symbol,Market,Date,Open,High,Low,Close,Volume
DIA,NYSEARCA,2019/04/01 16:00:00,261.23,262.66,260.58,262.39,6051711
DIA,NYSEARCA,2019/04/02 16:00:00,262,262.07,261.08,261.69,2320048
DIA,NYSEARCA,2019/04/03 16:00:00,262.58,262.72,261.22,262,3265528
DIA,NYSEARCA,2019/04/04 16:00:00,262.22,263.94,262.11,263.78,4397042
DIA,NYSEARCA,2019/04/05 16:00:00,264.56,264.84,263.61,264.16,3112718
DIA,NYSEARCA,2019/04/08 16:00:00,262.83,263.4,262.37,263.22,3231685
DIA,NYSEARCA,2019/04/09 16:00:00,262.12,262.14,260.95,261.51,4161583
DIA,NYSEARCA,2019/04/10 16:00:00,261.9,262.07,261,261.6,3602862
DIA,NYSEARCA,2019/04/11 16:00:00,261.92,262.25,260.58,261.4,2731683
DIA,NYSEARCA,2019/04/12 16:00:00,263.87,264.39,263.08,264.07,3395215
VOO,NYSEARCA,2019/04/01 16:00:00,261.46,262.78,261.19,262.53,3304080
VOO,NYSEARCA,2019/04/02 16:00:00,262.67,262.85,261.81,262.62,1512626
VOO,NYSEARCA,2019/04/03 16:00:00,263.87,264.25,262.4,263.11,1937471
VOO,NYSEARCA,2019/04/04 16:00:00,263.37,263.96,262.67,263.74,1738462
VOO,NYSEARCA,2019/04/05 16:00:00,264.42,265.06,264.12,265.01,1504961
VOO,NYSEARCA,2019/04/08 16:00:00,264.57,265.31,263.91,265.24,1720280
VOO,NYSEARCA,2019/04/09 16:00:00,264.22,264.54,263.29,263.83,2016861
VOO,NYSEARCA,2019/04/10 16:00:00,264.25,264.84,263.85,264.74,2990910
VOO,NYSEARCA,2019/04/11 16:00:00,265.24,265.24,264.09,264.69,1567704
VOO,NYSEARCA,2019/04/12 16:00:00,266.33,266.77,265.63,266.48,1903391
```

## TSVデータ形式

以下のような形式で用意。`tagload`コマンドで読み込む。

`<market name>:<ticker name>tab<tag name(:区切りで複数指定)>`

```
NYSEARCA:VOO  USA:ETF:INDEX
```

## 保存データバックアップ
データベースに保存したデータはDockerを停止すると消える。バックアップとリストアは以下のように実施する。

__バックアップ__
```
$ docker exec -it mysql bash
# cd /tools/
# ./export_sqlfile.sh ./backup_data.sql
```
`./docker/db/tools/`配下にファイルが作成される。

__リストア__
```
$ docker exec -it mysql bash
# cd /tools/
# ./import_sqlfile.sh ./backup_data.sql
```
`./docker/db/tools/`配下のファイルを読み込む。

## 自動テスト
__前提パッケージ__
* Python3

```
$ python3 -m unittest discover tests -v
```

