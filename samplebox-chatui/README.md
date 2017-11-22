# ChatUI（サンプル）

## samplebox-chatui
　Chat.UI: Pepper用のチェットインターフェイスのサンプルです。

### 動作環境
|項目|内容|
|:---|:---|
|NAOqi|2.5.5.5|
|Choregraphe|2.5.5.5|
|Pepper|for Biz / 一般販売モデル / デベロッパー先行モデル|

### ボックス

#### [Show App]
　Tablet Browser を起動させ、ディスプレイの表示を有効化します。

#### [ChatUI]
　アプリケーションのイベントを管理します。

　以下の入力でチャットインターフェイスを利用できます。

+ pepperSay: ペッパーの会話（文字列）
+ userSay: ユーザーの回答（文字列）
+ chatDebug: デバッグ表示（文字列）
+ imgShow: 画像の表示（文字列：htmlフォルダから相対パス）
+ chatInit: チェットインターフェイスの初期化（バン）

　以下のイベントを捕捉し対応する処理を呼び出しします。

+ ssa-hw-init: 初期化
+ ssa-hw-say: Pepperのセリフ表示
+ ssa-hw-dubugmsg: タブレットへのデバッグ表示
+ ssa-user-answer: タブレット操作によるユーザの回答
+ ssa-hw-imgshow: 画像の表示
+ ssa/show-dialog: ダイアログ表示
+ ssa/close-dialog: ダイアログ非表示

　チャットダイアログ無いで翻訳・NLCを呼び出す場合は、
html/js/chatui.js内の文字列を設定してください。

```
const TRANSLATION_API_KEY = "YOUR_TRANSLATION_API_KEY";
const NATURAL_LANGUAGE_API_KEY = "YOUR_NATURAL_LANGUAGE_API_KEY";
```

#### [Hide Web View]
　Web Viewを終了させ、ディスプレイの表示を戻します。
