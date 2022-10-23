# Backup Record Searcher
## 簡易多平台自動漫畫庫存同步程式
## 用法
`
docker run -p <external_port>:8586 -v </path/to/volume folder>:/app/datenbank -d poynt2005/backuprecordsearcher:<tag>
`
## 目前只有打算建置 Rpi4 的版本
## 2022-10-22 更新： 使用 sqlite3 作為儲存的資料庫並新增 x86 鏡像
