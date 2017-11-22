# Google Tensorflow（サンプル）

## samplebox-detection
　Google ML EngineあるいはGoogle Compute Engine（GPUインスタンス）を利用したPepperにおけるTensorflowのサンプルです。

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
* sixmm(sixm)
* uritemplate

#### [TakePhoto Script]
　写真を撮影します。Choregraphe から実行する場合以下にファイルを書き出します。

Choregraph：

```
/home/nao/.local/share/PackageManager/apps/.lastUploadedChoregrapheBehavior/html/
```

pkg：

```
/home/nao/.local/share/PackageManager/apps/samplebox-detection/html/
```

#### [Prediction]
　GCPに画像をアップロードし、結果を受け取ります。
　以下のパラメーターを設定します。

+ Project Name: GCPのプロジェクトネーム
+ Model Name: GCPのモデルネーム
+ Key Path: GCPのクライアントアクセスキーのパス
+ Label Path: ラベルファイルのパス
+ Version: バージョン（"v1"としてください）
+ Timeout: タイムアウト
+ GPU API Url: （GPU版のみ）GPUサーバのURLを指定します。
+ GPU API Key: （GPU版のみ）GPUサーバのAPIキーを指定します。

#### [SayJSON]
　[Prediction]ボックスから受け取ったJSON文字列を読み取りPepperが話します。

## GPUサーバ

* 画像認識用の高速サーバの構築方法です。（ML Engineをのみを利用する場合は、構成する必要はありません）

### インストール

#### ハードウェアの構成

* 以下の構成のサーバを用意します。

|   |内容|
|:--|:--|
|OS|Ubuntu 14.04 LTS x86-64|
|GPU|nVidia Cuda 対応GPU（例：nVidia Tesla K80）|
|N/W|インターネット接続、TCP PORT:5000で接続できること|

※検証環境では、Google Compute Engineを利用しています。

|   |内容|
|:--|:--|
|マシンタイプ|n1-standard-1（vCPU x 1、メモリ 3.75 GB）|
|CPU プラットフォーム|Intel Ivy Bridge|
|OS|Ubuntu 14.04 LTS x86-64|
|GPU|1 x NVIDIA Tesla K80|

#### GPUドライバのインストール

* GPUドライバをインストールします。
　以下のスクリプトを作成し、実行します。

```
#!/bin/bash
echo "Checking for CUDA and installing."
# Check for CUDA and try to install.
if ! dpkg-query -W cuda-8-0; then
  curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/cuda-repo-ubuntu1404_8.0.61-1_amd64.deb
  dpkg -i ./cuda-repo-ubuntu1404_8.0.61-1_amd64.deb
  apt-get update
  apt-get install cuda-8-0 -y
  apt-get install linux-headers-$(uname -r) -y
fi
```

* ドライバが古い場合は以下のコマンドでドライバを取り除き上記スクリプトを実行してください。

```
sudo apt-get --purge remove nvidia-*
sudo apt-get --purge remove cuda-*
```

* GPUが認識しているか以下のコマンドで確認します。

```
nvidia-smi
```

#### Python 環境の構築

* Python 3 をインストールします。

```
sudo apt-get install python3
```

* 構成ライブラリをインストールします。

```
pip install -r requirements.txt
```

#### TensorFlow のインストール

* TensorFlow（GPU） をインストールします。

* 以下の環境変数を登録します。

```
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

#### サーバソフトウェアのデプロイ

* GPUが搭載されたサーバに構成ファイル群をコピーします。
　本リポジトリをサーバにクローンしてください。

```
〓
```

* サーバプログラムを起動します。

### 起動

* 以下のコマンドを入力します。

```
python flask_server/gpuserver.py
```
