# PTT 二手相機 (DC_SALE) 搜尋小工具 (`family`)

即時爬取與搜尋 PTT `DC_SALE` 看板最新二手相機、鏡頭販售資訊的輕量 Web 工具。

- **線上正式版**：[https://family-six-bay.vercel.app](https://family-six-bay.vercel.app)
- **介面主題**：純深色模式 (Pure Dark Theme)
- **更新時間**：支援即時顯示最後爬蟲更新時間戳記與重新整理

## 特色功能
- **純深色沉浸式介面**：針對相機與鏡頭愛好者打造的低眩光純深色閱讀風格。
- **即時過濾與搜尋**：支援型號、焦段、品牌（Sony, Nikon, Canon, Fujifilm, Ricoh 等）關鍵字即時搜尋。
- **價格與售出狀態自動解析**：自動識別文章中之預估售價與售出/販售中狀態。
- **最後更新時間標示**：頂部與頁尾均有最後更新時間戳記，清楚掌握資料時效。

## 本地開發與爬蟲執行
```bash
# 執行 PTT DC_SALE 爬蟲以更新 data.json
python3 fetch_ptt.py

# 啟動本地靜態伺服器瀏覽
python3 -m http.server 3000
```
