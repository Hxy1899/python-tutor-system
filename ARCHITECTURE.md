## 1. 文档概述

本文档基于《智能化编程作业纠错与提示工具PRD》，定义系统的工程目录结构、模块划分、关键文件职责及部署约定。系统采用前后端分离架构，后端提供RESTful API，前端为单页应用（SPA），集成机器学习错误诊断能力。

---

## 2. 总体工程结构

```
python-tutor-system/
├── backend/                 # 后端服务（FastAPI）
├── frontend/                # 前端应用（Vue 3）
├── ml/                      # 机器学习模型训练与推理模块
├── docker-compose.yml       # 本地开发/测试编排
├── .env.example             # 环境变量模板
├── README.md                # 项目说明
└── docs/                    # 补充文档（API文档、部署手册等）
```

---

## 3. 后端工程结构 (backend/)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── api/                 # 路由层（接口定义）
│   │   ├── __init__.py
│   │   ├── v1/              # API版本 v1
│   │   │   ├── __init__.py
│   │   │   ├── code.py      # 代码提交、诊断接口
│   │   │   ├── assignment.py# 作业管理接口（教师）
│   │   │   ├── stats.py     # 学情统计接口
│   │   │   └── auth.py      # 用户认证（可选）
│   ├── core/                # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── preprocessor.py  # 代码预处理（规整、过滤）
│   │   ├── static_analyzer.py # 静态分析（pylint/flake8封装）
│   │   ├── dynamic_tester.py  # 动态测试（Docker + pytest）
│   │   ├── error_classifier.py # 错误分类器（调用ML模型）
│   │   ├── hint_generator.py   # 引导式提示生成
│   │   └── sandbox.py          # Docker沙箱管理
│   ├── models/              # 数据库ORM模型（SQLAlchemy）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── assignment.py
│   │   ├── submission.py
│   │   └── error_log.py
│   ├── schemas/             # Pydantic 请求/响应模型
│   │   ├── __init__.py
│   │   ├── code.py
│   │   ├── assignment.py
│   │   └── stats.py
│   ├── services/            # 业务服务层
│   │   ├── __init__.py
│   │   ├── diagnosis_service.py  # 诊断流程编排
│   │   ├── assignment_service.py
│   │   └── stats_service.py
│   ├── utils/               # 工具函数
│   │   ├── __init__.py
│   │   ├── logger.py        # 日志配置
│   │   ├── redis_client.py  # Redis连接
│   │   └── security.py      # 沙箱安全辅助
│   └── config.py            # 配置管理（环境变量）
├── tests/                   # 后端单元测试与集成测试
│   ├── test_api/
│   ├── test_core/
│   └── conftest.py
├── scripts/                 # 辅助脚本
│   ├── init_db.py           # 数据库初始化
│   └── seed_data.py         # 测试数据填充
├── requirements.txt         # Python依赖
├── requirements-dev.txt     # 开发依赖
└── Dockerfile               # 后端容器构建文件
```

### 3.1 后端关键模块说明

| 模块路径                        | 职责                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| `api/v1/code.py`                | 接收学生代码，调用诊断服务，返回错误类型与提示。             |
| `core/preprocessor.py`          | 去除注释、空行、特殊字符，规范化缩进。                       |
| `core/static_analyzer.py`       | 调用 pylint / flake8 获取静态问题列表，并转换为内部错误码。  |
| `core/dynamic_tester.py`        | 将代码放入 Docker 容器执行预设单元测试，捕获运行时错误。     |
| `core/error_classifier.py`      | 结合静态/动态结果，使用随机森林模型（TF-IDF+AST路径）判定错误类别。 |
| `core/hint_generator.py`        | 根据错误类别和学生代码上下文，生成自然语言引导提示。         |
| `models/`                       | 使用 SQLAlchemy + MySQL，记录学生提交、错误历史、作业成绩。  |
| `services/diagnosis_service.py` | 编排预处理→静态分析→动态测试→分类→提示生成流程。             |

---

## 4. 前端工程结构 (frontend/)

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── main.js              # 应用入口
│   ├── App.vue              # 根组件
│   ├── assets/              # 静态资源（CSS、图片）
│   ├── components/          # 通用组件
│   │   ├── CodeEditor.vue   # CodeMirror 6 封装
│   │   ├── HintPanel.vue    # 引导式提示展示区
│   │   └── ErrorHighlight.vue # 代码内错误高亮
│   ├── views/               # 页面视图
│   │   ├── StudentView.vue  # 学生端主页面（编辑器+提示）
│   │   ├── TeacherView.vue  # 教师端仪表盘
│   │   ├── AssignmentManage.vue # 作业管理
│   │   └── StatsReport.vue  # 学情统计报表
│   ├── router/              # Vue Router
│   │   └── index.js
│   ├── stores/              # Pinia 状态管理
│   │   ├── codeStore.js     # 代码内容、提交历史
│   │   └── userStore.js     # 用户角色、登录状态
│   ├── api/                 # 后端接口调用封装
│   │   ├── client.js        # axios实例
│   │   ├── code.js          # 提交代码、获取诊断结果
│   │   ├── assignment.js
│   │   └── stats.js
│   └── utils/               # 前端工具
│       └── highlight.js     # 错误位置映射
├── .env.development
├── .env.production
├── package.json
├── vite.config.js
└── Dockerfile               # 前端（Nginx）容器文件
```

### 4.1 前端关键组件说明

| 组件                 | 功能                                                         |
| -------------------- | ------------------------------------------------------------ |
| `CodeEditor.vue`     | 基于 CodeMirror 6 的 Python 编辑器，支持语法高亮、自动补全。 |
| `HintPanel.vue`      | 展示错误分类（如语法错误、缩进错误、变量未定义）以及引导式提示，不直接提供修复代码。 |
| `ErrorHighlight.vue` | 根据后端返回的错误行号，在编辑器中高亮对应行。               |
| `StudentView.vue`    | 整合编辑器、提交按钮、提示面板，支持多次提交修改。           |
| `TeacherView.vue`    | 展示所有学生作业列表、批改入口、学情概览卡片。               |

---

## 5. 机器学习模块 (ml/)

```
ml/
├── data/                    # 训练数据存放（不纳入版本控制）
│   ├── raw/                 # 原始学生代码样本
│   └── processed/           # 预处理后的特征
├── notebooks/               # Jupyter 探索与实验
├── models/                  # 训练好的模型文件
│   └── rf_error_model.pkl   # 随机森林模型
├── features/                # 特征工程脚本
│   ├── extract_tfidf.py     # 基于代码文本的TF-IDF
│   └── extract_ast.py       # 抽象语法树路径提取
├── train.py                 # 模型训练主脚本
├── predict.py               # 推理接口（供后端调用）
└── requirements-ml.txt      # 机器学习依赖（scikit-learn, pandas, ast etc.）
```

### 5.1 集成方式

- 后端 `error_classifier.py` 通过子进程或直接导入 `ml/predict.py` 调用模型。
- 模型输入：代码字符串 + 静态分析报告摘要 → 输出预定义错误类别（如 `SyntaxError`, `IndentationError`, `NameError`, `TypeError`, `LogicalError` 等）。
- 训练数据来自历史学生提交及公开错误数据集（如 MuTAP, CodeNet）。

---

## 6. 数据存储设计（概要）

### 6.1 MySQL 主要表结构

```sql
-- 用户表
users (
  id INT PK,
  role ENUM('student','teacher'),
  name VARCHAR(50),
  ...
)

-- 作业表
assignments (
  id INT PK,
  title VARCHAR(100),
  description TEXT,
  test_code TEXT,   -- 单元测试代码（用于动态测试）
  created_at DATETIME
)

-- 提交记录表
submissions (
  id INT PK,
  user_id INT FK,
  assignment_id INT FK,
  code TEXT,
  error_type VARCHAR(50),
  hint TEXT,
  is_correct BOOLEAN,
  submitted_at DATETIME
)

-- 错误日志表（用于模型迭代）
error_logs (
  id INT PK,
  submission_id INT FK,
  static_report JSON,
  dynamic_output TEXT,
  predicted_label VARCHAR(50)
)
```

### 6.2 Redis 缓存

- 临时存储：当前会话的代码诊断中间结果（减少重复计算，TTL=10min）。
- 队列：异步执行动态测试任务（使用 Redis List 或 Celery）。

---

## 7. 容器化与部署配置

### 7.1 docker-compose.yml 服务定义

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: tutor_db
    volumes:
      - mysql_data:/var/lib/mysql
  redis:
    image: redis:7-alpine
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - mysql
      - redis
    environment:
      DATABASE_URL: mysql://root:root@mysql/tutor_db
      REDIS_URL: redis://redis:6379
  frontend:
    build: ./frontend
    ports:
      - "80:80"
  sandbox:
    image: python:3.10-slim   # 动态测试用沙箱容器
    command: tail -f /dev/null
volumes:
  mysql_data:
```

### 7.2 代码沙箱执行流程

1. 后端 `dynamic_tester` 将学生代码与预设单元测试写入临时文件。
2. 调用 Docker SDK 创建一次性容器，挂载文件，执行 `pytest`。
3. 捕获 stdout/stderr，超时（如 5 秒）后强制终止容器。
4. 返回执行结果（通过/失败/错误类型）。

---

## 8. 开发与运行指南（简述）

### 8.1 后端启动

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 8.2 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 8.3 机器学习模型训练

```bash
cd ml
pip install -r requirements-ml.txt
python train.py --data data/processed/ --output models/
```

---

## 9. 扩展性说明

- **新增错误类型**：修改 `error_classifier.py` 中的类别映射，重新训练模型并更新 `hint_generator.py` 的提示模板。
- **支持其他语言**：未来可替换静态分析工具（如 ESLint for JS），核心流程不变。
- **教师端增强**：可独立部署报表服务（如 Metabase）直接查询 MySQL。

---

## 10. 附录：关键配置文件示例

### 10.1 backend/app/config.py

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "mysql://root:root@localhost/tutor_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    sandbox_image: str = "python:3.10-slim"
    static_tools: list = ["pylint", "flake8"]
    model_path: str = "../ml/models/rf_error_model.pkl"

settings = Settings()
```

### 10.2 frontend/src/api/client.js

```javascript
import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
});

export default client;
```
