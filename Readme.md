# Backup Record Searcher

## 簡易多平台自動漫畫庫存同步程式

### 說明

原本是在 [2022-09-03](https://github.com/poynt2005/backup-record-searcher/commit/b24656edccf57841ff6f34d832e5a13dd588f544) 新建的小項目，目的是為了同步、查看、搜尋硬碟中的漫畫檔案  
之前代碼結構、目錄比較混亂，db 檔案也沒放，製作漫畫數據的程序也沒放上來，故這次重新整理一下  
本次整理重點:

1. 將該有的檔案全部補上，包含 sql, webui html... 等
2. 去除樹梅派支持
3. 使用 pyinstaller + multi stage build，嘗試降低容器佔用空間
4. 刪掉所有 .DS_Store，這東西很煩 = =

### 建置

```
docker build -t backuprecordsearcher .
```

### 運行

請參考 runscript.txt，其中:

1. your_api_port 為 api server 的連線埠
2. path/to/server/logs: 為要存放 gunicorn 記錄檔的卷宗目錄
3. path/to/datenbank: 為存放 sql datenbank 檔案的卷宗目錄，裡面若沒有 datenbank.db 的話，則容器會自己新建

### 使用

1. 運行本容器
2. Windows 安裝 python
3. 檔案總管進入存檔案的硬碟目錄，運行 MkList_client.py 依照指示完成
4. 同步完後，打開 index.html，右上角齒輪圖案點進去設定 server api 網址，儲存

### 備註

本容器推至自架的私人容器倉庫
