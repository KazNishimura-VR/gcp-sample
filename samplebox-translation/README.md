# Google Cloud Translation API（サンプル）

## samplebox-translation
　Google Cloud Translation APIに接続するサンプルです。

### 動作環境
|項目|内容|
|:---|:---|
|NAOqi|2.5.5.5|
|Choregraphe|2.5.5.5|
|Pepper|for Biz / 一般販売モデル / デベロッパー先行モデル|

### ボックス

#### [Text Edit]
　翻訳したい文字列を設定します。

#### [SetPathLibFld]
　libフォルダ化にある以下の依存ライブラリを有効化します。

* requests

#### [Translate]
　受け取った文字列をGoogle Translateに送信し、結果を受け取ります。

　以下のパラメーターを設定します。

+ APIKey: Google Cloud PlatformのAPIKey
+ Language: 翻訳言語（選択式）

#### [Say Text]
　入力された言葉を話します。
