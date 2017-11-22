# Google Speech To Text（サンプル）

## samplebox-gsttre
　Google Cloud Speech API を使い音声認識した結果をPepperが話すサンプルです（オウム返し）。

### 動作環境
|項目|内容|
|:---|:---|
|NAOqi|2.5.5.5|
|Choregraphe|2.5.5.5|
|Pepper|for Biz / 一般販売モデル / デベロッパー先行モデル|

### ボックス

#### [SetPathLibFld]
　libフォルダ化にある以下の依存ライブラリを有効化します。

* googleapiclient
* httplib2
* oauth2client
* pyasn1
* pyasn1_modules
* rsa
* sixmm(Pepper内部のバージョンと競合するためsixmをリネーム)
* uritemplate

#### [GoogleSTT]
　以下のパラメーターを設定します。

+ GoogleSTTKey: Client Access Key
+ Timeout: タイムアウト

　処理の進行はPepperのLED表示等により確認できます。

|表現|内容|
|---|---|
|右目：赤|APIキー不足|
|左目：赤|APIエラー1|
|左目：紫|APIエラー2（応答キー不足）|
|両目：緑|音声データ送信|
|両目：青|認識失敗|
|両目：白|認識成功|
