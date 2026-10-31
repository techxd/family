# 專案狀態 (STATUS.md)

## 專案資訊
- **專案名稱**：volleyball-attendance (`danny`)
- **主要技術棧**：Next.js 14.2.23 (App Router), React 18, TypeScript, Tailwind CSS, Lucide React
- **正式環境網址**：https://danny-pied.vercel.app

## 現有架構
- `app/`：Next.js 應用路由與頁面
- `lib/`：通用工具函式與模組
- `next.config.js` / `tailwind.config.js` / `tsconfig.json`：專案配置檔
- `.vercel/`：Vercel 部署關聯設定

## Vercel 上線網站總覽
1. **芳和實中排球團 - 請假與報名系統** (`danny`)：https://danny-pied.vercel.app
2. **PTT 二手相機 (DC_SALE) 搜尋小工具** (`family`)：https://family-six-bay.vercel.app
3. **士林・永和 即時天氣** (`weather-shilin-yonghe`)：https://weather-shilin-yonghe.vercel.app

---

## 自動雙平台同步發布規範 (GitHub + Vercel SOP)

為確保往後所有 Web 專案皆能以標準化、自動化方式同步發布至 GitHub 與 Vercel，訂定以下操作規範：

### 1. 標準 `.gitignore` 規範
每個新 Web 專案建立時，根目錄必須包含 `.gitignore`，嚴禁將敏感變數與建置快取推送到 Git 遠端：
```gitignore
# 依賴套件
node_modules/
.pnp
.pnp.js

# 部署與本地配置快取
.vercel/
.next/
out/
build/
dist/

# 環境變數與機密資訊
.env
.env*.local
.env.production
.env.development

# 日誌與系統檔
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
Thumbs.db
```

### 2. 全新專案初次發布 SOP
在專案根目錄依序執行以下步驟：

```bash
# Step 1: 初始化並建立初次提交
git init
git add .
git commit -m "feat: initial commit"
git branch -M main

# Step 2: 透過 GitHub CLI 建立遠端 Repo 並自動推送代碼
gh repo create <專案英文名稱> --public --source=. --remote=origin --push

# Step 3: 透過 Vercel CLI 進行非互動生產環境部署
vercel --prod --yes
```

### 3. 既有專案更新發布 SOP
日常代碼調整完成後，單行指令完成遠端推送與生產部署：
```bash
git add . && git commit -m "<更新說明>" && git push && vercel --prod --yes
```

### 4. 必備 CLI 工具與環境狀態檢查
- **Git**：`git --version`
- **GitHub CLI (`gh`)**：`gh auth status`
- **Vercel CLI**：`vercel whoami`

---

## 最新進度與異動記錄 (2026-10-31 22:50)
- **本次任務**：讀取 `https://family-six-bay.vercel.app` (`family` 專案)，改為純粹深色風格並加上最後更新時間，同步推送至 GitHub 與 Vercel。
- **執行成果**：
  1. **爬蟲更新**：執行 `python3 fetch_ptt.py` 取得最新 76 篇 DC_SALE 看板二手買賣文章，更新 `data.json`（最新更新時間戳記：`2026-10-31 22:48:53`）。
  2. **純深色介面改版**：
     - 背景採用沉浸式純深色 `#090d16`，搭配頂部導覽 `#0d1322` 與磨砂質感 `slate-900` 卡片。
     - 移除深淺色切換開關，統一為純深色高對比字體排版與發光標籤（販售中/已售出/價格）。
     - 擴充快捷品牌篩選按鈕（Sony, Nikon, Canon, Fujifilm, Ricoh/GR）。
  3. **最後更新時間強化**：
     - 頂部導覽列新增時鐘圖示與醒目「最後更新時間」標籤（精確至秒）。
     - 新增「重新整理」按鈕，方便隨時以防快取機制重新拉取最新 `data.json`。
     - 底部頁尾同步顯示系統時間戳記。
  4. **GitHub 儲存庫建立與同步**：
     - 配置本機 Git 使用者名稱與信箱。
     - 規範 `.gitignore` 與建立 [README.md](file:///home/techxd/agent-projects/family/README.md)。
     - 透過 `gh repo create` 成功建立公開倉庫並推送：[https://github.com/techxd/family](https://github.com/techxd/family)。
  5. **Vercel 生產部署**：
     - 透過 `vercel --prod --yes` 完成部署。
     - 線上正式網址已同步生效：[https://family-six-bay.vercel.app](https://family-six-bay.vercel.app)。
- **檔案異動**：
  - [family/index.html](file:///home/techxd/agent-projects/family/index.html)：純深色版型重構、更新時間與重整按鈕
  - [family/data.json](file:///home/techxd/agent-projects/family/data.json)：最新 76 篇文章與時間戳更新
  - [family/.gitignore](file:///home/techxd/agent-projects/family/.gitignore)：標準化部署與快取忽略清單
  - [family/README.md](file:///home/techxd/agent-projects/family/README.md)：建立專案說明文件
  - [danny/STATUS.md](file:///home/techxd/agent-projects/danny/STATUS.md)：更新專案進度與紀錄

---

## 歷史記錄 (2026-10-31 22:40)
- **歷史任務**：檢查並配置 N200 上的 GitHub 與 Vercel 同步環境，建立「自動雙平台同步發布規範」。
- **CLI 環境檢查結果**：
  - **Git**：已安裝 (`git version 2.47.3`)。
  - **GitHub CLI (`gh`)**：已安裝 (`gh version 2.46.0`)，已授權登入（帳號：`techxd`，Protocol：`https`，Token Scopes：`gist`, `read:org`, `repo`, `workflow`）。
  - **Vercel CLI**：已安裝 (`Vercel CLI 65.9.0`)，已授權登入（帳號：`technicians32-2940`，Team：`bearkid (Bearkid)`，方案：`Hobby`）。
  - **整體狀態**：**GitHub 與 Vercel 雙平台 CLI 環境已全部配置並授權完畢**，可隨時執行自動化同步與部署。
- **完成事項**：
  1. 完整驗證本機 CLI 環境（`git`、`gh`、`vercel` 均已就緒並通過驗證）。
  2. 確認專案 [.gitignore](file:///home/techxd/agent-projects/danny/.gitignore) 具備完整忽略規則（排除 node_modules, .vercel, .env 等）。
  3. 於 [STATUS.md](file:///home/techxd/agent-projects/danny/STATUS.md) 正式建立雙平台同步發布 SOP（全新專案發布與既有專案更新流程）。
- **檔案異動**：
  - 更新 [STATUS.md](file:///home/techxd/agent-projects/danny/STATUS.md)
