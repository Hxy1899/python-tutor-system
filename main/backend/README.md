# Python Tutor System - 后端服务指南

> **版本**: 1.0.0  
> **更新日期**: 2026-04-02  
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
- `DATABASE_URL`: 数据库连接字符串。
- `REDIS_URL`: Redis 连接字符串。
- `MODEL_PATH`: 机器学习模型文件路径。

---

## 3. 运行命令

### 3.1 开发模式运行
```bash
# 自动重载代码
uvicorn app.main:app --reload --port 8000
```

### 3.2 生产模式运行 (Docker)
```bash
docker build -t tutor-backend .
docker run -p 8000:8000 tutor-backend
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
- 接口: `POST /api/v1/code/submit`

---

## 5. 常见问题 (FAQ)

**Q: 运行时提示 `Docker not found`？**
A: 后端沙箱模块依赖 Docker SDK，请确保本地 Docker 服务已启动且当前用户有权限调用。

**Q: 数据库连接超时？**
A: 请检查 `DATABASE_URL` 是否正确，且 MySQL 服务已开启。

---
? 2026 Backend Team. Python Tutor System.
