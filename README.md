# Chat-to-DB（智能问数系统）

基于自然语言的智能数据库查询平台。用户通过自然语言提问，系统自动将问题转化为 SQL、执行查询并返回结果，支持可选的图表可视化。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户                                  │
│                   ┌─────────┴─────────┐                     │
│                   ▼                   ▼                     │
│            Chat UI (:3000)      Admin UI (:3001)            │
│            (Next.js)            (React + Ant Design)        │
│                   │                   │                     │
└───────────────────┼───────────────────┼─────────────────────┘
                    │ LangGraph SDK     │ Axios
                    ▼                   ▼
┌────────────────────────┐  ┌──────────────────────────────┐
│  LangGraph Server      │  │  Admin API (FastAPI :8000)    │
│  (FastAPI :2025)       │  │  ├─ 连接管理                  │
│  ┌──────────────────┐  │  │  ├─ 数据建模                  │
│  │  SupervisorAgent  │  │  │  ├─ 值映射                    │
│  │  ┌──────────────┐│  │  │  ├─ 知识图谱可视化            │
│  │  │ Schema Agent ││  │  │  └─ 混合问答管理              │
│  │  │ SQL 生成     ││  │  └──────────┬───────────────────┘
│  │  │ SQL 校验     ││  │             │
│  │  │ SQL 执行     ││  │             ▼
│  │  │ 图表生成     ││  │  ┌──────────────────────────────┐
│  │  │ 错误恢复     ││  │  │        MySQL                 │
│  │  └──────────────┘│  │  └──────────────────────────────┘
│  └──────────────────┘  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  LLM (智谱/DeepSeek)   │
│  Milvus (向量检索)      │
│  Neo4j (知识图谱)       │
└────────────────────────┘
```

## 技术栈

| 组件 | 技术 |
|------|------|
| **后端框架** | FastAPI + Uvicorn |
| **AI 编排** | LangGraph（Supervisor 多 Agent 模式） |
| **LLM** | 智谱 Anthropic API / DeepSeek / Ollama |
| **主数据库** | MySQL（SQLAlchemy + PyMySQL） |
| **向量数据库** | Milvus（语义检索） |
| **图数据库** | Neo4j（知识图谱） |
| **嵌入模型** | Ollama（qwen3-embedding） |
| **聊天前端** | Next.js 15 + React 19 + Tailwind CSS 4 |
| **管理前端** | React 18 + Ant Design 5 + AntV G6 |
| **图表** | Recharts / Chart.js |

## 多 Agent 系统

系统采用 LangGraph Supervisor 模式，由 6 个专业 Agent 协作完成自然语言到 SQL 的转换：

| Agent | 职责 |
|-------|------|
| **Schema Agent** | 分析用户查询，提取实体，检索相关数据库 Schema |
| **SQL Generator** | 基于 Schema 上下文和用户问题生成 SQL |
| **SQL Validator** | 校验 SQL 语法、安全性和性能 |
| **SQL Executor** | 执行已校验的 SQL 查询 |
| **Chart Generator** | 检测可视化意图，生成图表规格 |
| **Error Recovery** | 处理各阶段错误并建议修复方案 |

**典型执行流程：**
```
用户提问 → Schema分析 → SQL生成 → SQL校验 → SQL执行 → [图表生成] → 返回结果
                                                    ↘ 错误恢复 → 重试
```

## 混合检索系统

系统使用 FusionRanker 融合多路检索结果，提升 SQL 生成质量：

- **语义检索**（权重 60%）：基于 Milvus 向量相似度搜索
- **结构检索**（权重 20%）：基于 Neo4j 知识图谱关系匹配
- **模式检索**（权重 10%）：基于历史查询模式匹配
- **质量评分**（权重 10%）：基于 QA 对质量评估

## 项目结构

```
chat-to-db/
├── backend/                    # 后端服务
│   ├── admin_server.py         # 管理 API 服务 (端口 8000)
│   ├── chat_server.py          # LangGraph 聊天服务 (端口 2025)
│   ├── langgraph.json          # LangGraph 部署配置
│   ├── requirements.txt        # Python 依赖
│   └── app/
│       ├── agents/             # 多 Agent 系统
│       │   ├── agents/         # 各专业 Agent 实现
│       │   ├── chat_graph.py   # 主图定义
│       │   └── parallel_chat_graph.py  # 并行图变体
│       ├── api/                # API 路由（7 个端点组）
│       ├── core/               # 配置、LLM、状态管理
│       ├── crud/               # 数据库 CRUD 操作
│       ├── db/                 # 数据库连接和会话
│       ├── models/             # SQLAlchemy ORM 模型
│       ├── schemas/            # Pydantic 数据模型
│       └── services/           # 业务服务层
├── frontend/
│   ├── admin/                  # 管理后台 (React + Ant Design)
│   │   └── src/
│   │       ├── pages/          # 页面组件
│   │       ├── components/     # 公共组件
│   │       └── services/       # API 服务
│   └── chat/                   # 聊天界面 (Next.js)
│       └── src/
│           ├── app/            # Next.js App Router
│           ├── components/     # UI 组件
│           └── providers/      # LangGraph SDK 集成
└── docs/                       # 项目文档
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Neo4j 5.0+（可选，用于知识图谱）
- Milvus 2.0+（可选，用于混合检索）
- Ollama（可选，用于本地嵌入模型）

### 1. 配置环境变量

在 `backend/` 目录下创建 `.env` 文件：

```env
# MySQL
MYSQL_SERVER=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=chat2db
MYSQL_PORT=3306

# Neo4j（可选）
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Milvus（可选）
MILVUS_HOST=localhost
MILVUS_PORT=19530

# LLM 配置
ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_API_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Ollama 嵌入模型（可选）
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=qwen3-embedding:0.6b
```

### 2. 启动后端

```bash
# 安装依赖
pip install -r backend/requirements.txt

# 启动管理 API（端口 8000）
cd backend
python admin_server.py

# 启动 LangGraph 聊天服务（端口 2025）
cd backend
python chat_server.py
```

### 3. 启动前端

```bash
# 管理后台
cd frontend/admin
npm install
npm start        # 默认端口 3001

# 聊天界面
cd frontend/chat
pnpm install
pnpm dev         # 默认端口 3000
```

### 4. 访问系统

- 聊天界面：http://localhost:3000
- 管理后台：http://localhost:3001
- 管理 API 文档：http://localhost:8000/docs

## 核心功能

### 自然语言查询
- 输入中文自然语言问题，自动生成并执行 SQL
- 支持多轮对话上下文
- 流式输出，实时展示 Agent 执行过程

### 数据建模
- 可视化管理数据库连接
- 自动/手动维护表结构和字段元数据
- 管理表间关系和字段值映射

### 知识图谱
- 可视化展示数据库表间关系
- 基于 Neo4j 的结构化知识存储
- 交互式图谱浏览和编辑

### 智能训练
- 管理问答训练对，提升 SQL 生成准确率
- 混合检索（向量 + 图谱）匹配相似问题
- 收集用户反馈持续优化

## API 端点

| 路径 | 说明 |
|------|------|
| `POST /api/connections` | 数据库连接管理 |
| `GET/POST /api/schema` | Schema 元数据管理 |
| `POST /api/query` | 自然语言查询 |
| `GET/POST /api/value-mappings` | 值映射管理 |
| `GET /api/graph-visualization` | 知识图谱可视化 |
| `GET/POST /api/hybrid-qa` | 混合问答管理 |
| `GET/POST /api/relationship-tips` | 表关系提示 |
