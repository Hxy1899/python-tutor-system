# Python Tutor System - 后端服务指南

> **版本**: 1.1.0  
> **更新日期**: 2026-04-08  
> **框架**: FastAPI (Python 3.10+)

---

## 1. 模块功能说明

后端服务负责处理核心业务逻辑，包括：
- **API 路由**: 接收学生提交的代码并返回诊断结果。
- **预处理 (Preprocessor)**: 规范化代码，消除不必要的干扰项。
- **静态分析 (Static Analyzer)**: 调用 Pylint 库识别语法及潜在的质量问题。
- **沙箱隔离 (Sandbox)**: 在独立的 Docker 容器中安全执行代码，防御恶意脚本。
- **错误分类 (Error Classifier)**: 基于 TF-IDF 和 AST 特征的机器学习推理。
- **提示生成 (Hint Generator)**: 根据错误类型生成针对性的引导式反馈。
- **用户认证 (Auth)**: 基于 JWT 的登录、注册与权限管理。
- **作业管理 (Assignment)**: 教师发布作业、配置测试用例，学生查看作业。
- **学情统计 (Stats)**: 自动分析错误分布、学生进度及平均正确率。

---

## 2. 安装与配置指南

### 2.1 本地开发环境准备
1. 安装 Python 3.10+。
2. 安装 Docker Desktop（用于沙箱执行）。
3. 安装 MySQL 8.0+（如果非 Docker 运行）。

### 2.2 依赖安装
建议使用虚拟环境进行安装。

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\activate # Windows

# 安装所有必需的依赖包
pip install -r requirements.txt
```

### 2.3 配置环境变量
在 `app/config.py` 中可以调整以下配置，或通过 `.env` 文件覆盖：
- `DATABASE_URL`: `mysql+mysqlconnector://root:root@localhost:3306/tutor_db` (本地开发)
- `REDIS_URL`: `redis://localhost:6379` (本地开发)
- `MODEL_PATH`: 模型文件路径 (默认已通过 Docker 卷挂载)

---

## 3. 运行命令

### 3.1 数据库初始化 (首次运行必做)
```bash
# 本地开发模式
python scripts/init_db.py

# Docker 模式 (在项目根目录执行)
docker exec main-backend-1 python scripts/init_db.py
```

### 3.2 本地开发模式
```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端 (默认端口 8000)
uvicorn app.main:app --reload --port 8000
```

### 3.3 生产/容器模式 (推荐)
请在项目根目录 `main/` 下使用 `docker-compose`：
```bash
# 启动后端及相关服务 (MySQL, Redis)
docker-compose up -d backend
```

---

## 4. 测试与验证

### 4.1 单元测试
运行以下命令验证核心模块的功能：
```bash
pytest tests/
```

### 4.2 接口验证
访问 Swagger 文档并手动调用接口：
- 地址: [http://localhost:8000/docs](http://localhost:8000/docs)
- 接口: `POST /api/v1/auth/login`, `POST /api/v1/code/submit`, `GET /api/v1/stats/overall`

---

## 5. 运维与日志

### 5.1 日志查看
```bash
# 查看实时日志
docker logs -f main-backend-1
```

### 5.2 回滚方案
1. **代码回滚**: `git checkout <commit_id>`
2. **镜像回滚**: 修改 `docker-compose.yml` 镜像版本并执行 `docker-compose up -d`
3. **数据库回滚**: 手动恢复最近一次的 SQL 备份。

---

## 6. 常见问题 (FAQ)

**Q: 运行时提示 `Docker not found`？**
A: 后端沙箱模块依赖 Docker SDK，请确保本地 Docker 服务已启动且当前用户有权限调用。

**Q: 数据库连接超时？**
A: 请检查 `DATABASE_URL` 是否正确，且 MySQL 服务已开启。

---
? 2026 Backend Team. Python Tutor System.
