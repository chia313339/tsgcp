# 程式說明
* 使用python3.7
* 因有使用CDN需要外網環境

# 基本說明
treestudio GCP 版本，主要提供樣板網頁給功能串接，使用下面語法即可開啟9000port的服務。
```
python main2.py
```
main.py及main2.py只差在port，main.py主要給nginx docker服務使用。

# nginx docker說明
使用dockerfile建立image，啟動後即可使用nginx框架起服務。
```
docker build -t treestudio . --no-cache
```
```
docker run -it -p 80:80 -d treestudio
```
# Reference
風格參考[網頁素材](https://adminlte.io/themes/v3/index3.html)

