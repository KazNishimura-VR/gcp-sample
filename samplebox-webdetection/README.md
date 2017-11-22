# Google Web detection（サンプル）

## samplebox-webdetection
　Google Vision APIに接続するサンプルです。
　Pepperカメラから得た画像をWeb検索します。

### 動作環境
|項目|内容|
|:---|:---|
|NAOqi|2.5.5.5|
|Choregraphe|2.5.5.5|
|Pepper|for Biz / 一般販売モデル / デベロッパー先行モデル|

### ボックス

#### [Take Picture]
　写真を撮影します。

#### [Web Detection]
　撮影した画像を受け取りGoogle Vision APIに送信し、結果を受け取ります。

　以下のパラメーターを設定します。

+ API URL: Google Vision API のURL
+ Google Key: APIKey

#### [Say Text]
　入力された言葉を話します。
