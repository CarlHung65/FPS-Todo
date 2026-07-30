# FPS-Todo
Learning project for FastAPI、PostgreSQL、Streamlit.
```
技術架構分工說明
Backend（後端）：FastAPI — 負責 API 介面、商業邏輯、身份驗證、資料處理。
Database（資料庫）：PostgreSQL — 儲存結構化資料（配合 SQLAlchemy 或 SQLModel 作為 ORM）。
Frontend（前端）：Streamlit — 快速建立 UI 介面，直接呼叫 FastAPI 提供的 API 進行資料互動。

學習藍圖

1：基礎打底 & PostgreSQL 資料庫設計
目標：掌握 PostgreSQL 基本操作與 Python 後端資料庫連線。

重點內容：
PostgreSQL 基礎：安裝、使用 pgAdmin 或 DBeaver 管理介面，掌握 CRUD SQL 語法與 Primary/Foreign Key 設定。
Python 與 DB 連線：學習使用 SQLAlchemy (2.0+) 或 SQLModel 建立 ORM 類別與資料表映射（Mapping）。
資料庫遷移（Migration）：學習 Alembic 工具來管理資料表結構變更。
實作小練習：用 Python 寫一個腳本，在 PostgreSQL 中自動建立 Users 與 Tasks 資料表，並執行新增、查詢操作。

2：FastAPI 後端 API 開發
目標：掌握 FastAPI 核心機制、自動化文檔與資料庫整合。

重點內容：
FastAPI 核心：路由（Routing）、請求參數（Query/Path Parameters）、Pydantic 資料驗證（Schemas）。
依賴注入（Dependency Injection）：使用 Depends() 管理資料庫 Session 生命週期（建立與關閉）。
非同步開發 (Async)：了解 async/await 與 asyncpg/AsyncSession 的搭配。
認證機制：實作 JWT (JSON Web Token) 使用者登入與權限驗證。
實作小練習：寫出完整的 CRUD RESTful API，並利用內建的 /docs (Swagger UI) 進行介面測試。

3：Streamlit 前端 UI 與 API 串接
目標：用 Streamlit 快速打造互動式 UI，並與 FastAPI 後端進行通訊。

重點內容：
Streamlit 介面元件：Forms, Buttons, Tables, Charts, Sidebar 佈局。
狀態管理（State Management）：掌握 st.session_state（這是在 Streamlit 處理登入狀態、跨頁面資料傳遞的核心機制）。
後端通訊：使用 Python requests 或 httpx 套件發送 HTTP Request 到 FastAPI 介面。
效能優化：使用 @st.cache_data 避免重複發送不必要的 API 請求。
實作小練習：建立一個 Streamlit 頁面，包含「使用者登入表單」與「資料新增/列表顯示」。

4：實戰全棧專案與容器化部署
目標：整合三者，完成一個端到端專案，並使用 Docker 包裝。

重點內容：
專案整合：建立一個「個人待辦事項系統」或「數據分析與管理平台」。
環境變數管理：使用 .env 檔案儲存資料庫密碼與 JWT Secret Key（配合 pydantic-settings）。
Docker 容器化：撰寫 Dockerfile，並使用 docker-compose.yml 一鍵啟動 PostgreSQL、FastAPI、Streamlit 三個服務。
實作小練習：執行 docker compose up 即可順利開啟整套系統。


💡 建議實作專案主題
學完理論後，強烈建議挑選一個實作專案來練習：

個人財務/記帳管理系統
FastAPI：提供記帳 CRUD API，計算總支出與分類統計。
PostgreSQL：儲存交易紀錄、分類與使用者帳號。
Streamlit：呈現收支圖表（Pie chart / Line chart）、新增消費紀錄表單。

AI 知識庫 / 文件問答系統 (RAG App)
FastAPI：串接 OpenAI / Local LLM API，處理文本向量化與檢索邏輯。
PostgreSQL：搭配 pgvector 套件，直接做向量搜尋與用戶對話紀錄儲存。
Streamlit：對話式 UI（st.chat_input / st.chat_message）與文件上傳區。

🛠️ 推薦工具與套件組合
開發語言：Python 3.10+
後端：fastapi, uvicorn, pydantic, pydantic-settings
資料庫 ORM：sqlmodel（由 FastAPI 作者開發，整合了 Pydantic 與 SQLAlchemy，非常適合新手）
資料庫驅動：psycopg2-binary 或 asyncpg
前端：streamlit, requests / httpx
```