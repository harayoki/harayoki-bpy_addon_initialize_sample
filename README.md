# bpy addon initialize sample
pip で　bpy モジュールを導入したpythonプロジェクトで、アドオンを動的に追加するサンプル。


# 動作環境

Windows11 + Python 3.11.4 で作成されています。bpyモジュールを利用します。Macでも動作すると思われる。

Windowsでの動作環境構築までの手順例を下記に記します。

```
python -m venv venv
venv\Scripts\activate.bat
（もしくは venv\Scripts\Activate.ps1）
pip install -r requirements.txt
```

## 処理内容

* 初期状態で存在するアドオン一覧を表示する。
* 指定されたフォルダに入っているアドオンを自動で初期化する。


### 使い方

python、またはBlenderのバックグラウンドモードもしくはBlenderのスクリプトパネルで実行する。
アドオンフォルダを指定するとその中のアドオンを動的に読み込んで初期化する。

### bpyモジュールをPIP導入したpythonプロジェクトの場合

src/test1.pyをpythonで実行する。結果がコンソールに表示される。

`python.exe src\test1.py -a addons`

### Blenderのバックグラウンドモードの場合

`blender.exe -b --python src\test1.py -- -a addons`

### Blender内のscriptパネルで実行する場合

まず、systemコンソールを表示。src\test1.py をコピペまたは読み込んだ状態で実行。
※ Blenderがフリーズする事が何回かあったので注意する。

アドオンを追加したい場合はmain呼び出しにアドオンフォルダへのパスを追加する。

`main(addon_dir='addonsフォルダへのパス')`

### アドオン実行テスト

コマンドにtest引数を付けた場合、このリポジトリ内のaddonsフォルダにあるアドオンを追加して、コマンドでアドオンを実行する。

`python.exe src\test1.py --test`

直にaddonディレクトリを指定する事もできる。Blenderのscriptパネルで実行時などで自動でaddonsフォルダが確定できない場合に使う。

`python.exe src\test1.py --test -a other_addons`

save_blendでblendファイルパスを指定するとテスト結果を保存できる。

`python.exe src\test1.py --test -a other_addons --save_blend out/result.blend`

