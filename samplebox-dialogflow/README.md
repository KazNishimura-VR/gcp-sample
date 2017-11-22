# Google Dialogflow（サンプル）

## samplebox-dialogflow
　Dialogflow（旧称：API.AI）に接続するためのサンプルです。

### 動作環境
|項目|内容|
|:---|:---|
|NAOqi|2.5.5.5|
|Choregraphe|2.5.5.5|
|Pepper|for Biz / 一般販売モデル / デベロッパー先行モデル|

### ボックス

#### [SetPathLibFld]
　libフォルダ化にある以下の依存ライブラリを有効化します。

* apiai

#### [Dialogflow]
　以下のパラメーターを設定します。

+ api_ai_token: DialogflowのClientAccessToken

#### [Text Edit]
　Dialogflowに問い合わせる質問（テキスト）を設定します。
