# 個人 Dashboard

一個基於 Python 的個人 Dashboard 應用，集成 Tkinter 桌面界面和 Flask 後端。

## 功能特性

- ⏰ **即時時間顯示** - 顯示當前日期和時間
- 📅 **互動式月曆** - 可切換月份查看日期
- ✅ **任務管理** - 添加、編輯、完成和刪除任務
- 💾 **數據持久化** - 任務保存在 SQLite 數據庫
- 🌐 **前後端分離** - Tkinter 前端 + Flask 後端

## 系統要求

- Python 3.8+
- pip

## 安裝

### 1. 克隆倉庫

```bash
git clone https://github.com/evan-pei/personal-dashboard.git
cd personal-dashboard
```

### 2. 安裝後端依賴

```bash
cd backend
pip install -r requirements.txt
```

### 3. 安裝前端依賴

Tkinter 通常已包含在 Python 中，如果沒有請安裝：

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

**Windows:** 已包含

## 運行

### 方式一：分別運行（推薦）

**終端 1 - 啟動後端服務器：**
```bash
cd backend
python app.py
```

你應該看到：
```
 * Running on http://localhost:5000
```

**終端 2 - 啟動前端應用：**
```bash
cd frontend
python dashboard.py
```

### 方式二：使用 run.sh（可選）

創建 `run.sh` 文件（自動同時啟動前後端）

## 使用說明

### 時間顯示
- 右上角自動顯示當前時間，每秒更新

### 月曆功能
- 點擊 **< 上月** 查看上一個月
- 點擊 **下月 >** 查看下一個月
- 當天日期會以淡藍色高亮顯示

### 任務管理
1. **新增任務**：點擊 "+ 新增任務" 按鈕
   - 輸入標題（必填）
   - 添加描述（可選）
   - 設置期限 YYYY-MM-DD 格式（可選）

2. **編輯任務**：雙擊列表中的任務

3. **標記完成**：選中任務後點擊 "✓ 完成" 按鈕
   - 完成的任務會顯示為灰色且前面有 ✓ 符號

4. **刪除任務**：
   - 選中任務後點擊 "✕ 刪除" 按鈕
   - 或按 Delete 鍵

5. **刷新**：點擊 "⟳ 刷新" 按鈕同步最新任務

## 文件結構

```
personal-dashboard/
├── backend/
│   ├── app.py                 # Flask 應用主文件
│   ├── config.py              # 配置文件
│   ├── requirements.txt       # 依賴列表
│   └── database.db            # 數據庫（自動生成）
├── frontend/
│   └── dashboard.py           # Tkinter 應用
└── README.md                  # 本文檔
```

## API 文檔

### 獲取所有任務
```
GET /api/tasks
```

### 創建新任務
```
POST /api/tasks
Content-Type: application/json

{
  "title": "任務標題",
  "description": "描述（可選）",
  "due_date": "2024-12-31"（可選，YYYY-MM-DD 格式）
}
```

### 更新任務
```
PUT /api/tasks/:id
Content-Type: application/json

{
  "title": "新標題",
  "description": "新描述",
  "completed": true
}
```

### 刪除任務
```
DELETE /api/tasks/:id
```

## 故障排除

### 連接錯誤
- 確保後端服務器正在運行（http://localhost:5000）
- 檢查防火牆設置

### 數據庫錯誤
- 刪除 `backend/database.db` 文件並重新啟動後端

### Tkinter 導入錯誤
- 參考上面的「安裝」章節，按照你的操作系統安裝 python3-tk

## 技術棧

- **前端**：Tkinter（Python GUI）
- **後端**：Flask（Python Web Framework）
- **數據庫**：SQLite
- **通信**：REST API + HTTP

## 未來功能

- [ ] 任務優先級設置
- [ ] 任務分類標籤
- [ ] 日程提醒功能
- [ ] 數據導出（CSV/PDF）
- [ ] 深色模式

## 許可證

MIT License

## 作者

Evan Pei
