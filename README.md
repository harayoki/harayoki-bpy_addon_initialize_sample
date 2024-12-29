# bpy addon initialize sample
pip で　bpy モジュールを導入したpythonプロジェクトで、アドオンを動的に追加するサンプル。


# 動作環境

Windows11 + Python 3.11.4 で作成されています。bpy・PyInstallerなどのモジュールを利用します。
Macでも動作すると思われます。

動作環境構築までの手順例を下記に記します。

```
python -m venv venv
venv\Scripts\activate.bat
（もしくは venv\Scripts\Activate.ps1）
pip install -r requirements.txt
```

## 処理内容

* 初期状態で存在するアドオン一覧を表示する。
* addonフォルダに入っているアドオンを自動で初期化する。
* アウトプットフォルダ指示があればアドオンで何か処理をしてアウトプットをする。


### 使い方

src/test1.pyをpythonで実行する。結果がコンソールに表示される。
アドオンフォルダを指定するとその中のアドオンを動的に読み込んで初期化する。
アウトプットフォルダ指定をすると、そこにテストアウトプットを行う。

`python.exe src\test1.py -a addons`
`python.exe src\test1.py -a .\addons -o out`
