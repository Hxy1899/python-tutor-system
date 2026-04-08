# Python Tutor System —— 智能化编程作业纠错与提示工具

> **版本**: 1.0.0  
> **更新日期**: 2026-04-02  
> **项目定位**: 面向中小学 Python 编程教学，提供智能错误诊断 + 引导式提示 + 在线编辑器的完整解决方案。

---

## 1. 项目整体架构说明

本系统采用前后端分离的 **B/S 架构**，结合静态分析、动态沙箱及机器学习模型，构建了一个闭环的编程辅助环境。

### 1.1 目录结构解释
```text
main/
├── backend/                 # 后端服务（FastAPI + MySQL + Redis）
│   ├── app/                 # 核心业务逻辑
│   ├── tests/               # 单元测试与集成测试
│   └── scripts/             # 数据库初始化与数据填充脚本
├── frontend/                # 前端应用（Vue 3 + CodeMirror 6 + Pinia)
│   ├── src/                 # 源码（组件、视图、状态管理）
│   └── public/              # 静态资源
├── ml/                      # 机器学习模块
│   └── models/              # 已训练的模型文件（.pkl）
├── docker-compose.yml       # 容器化编排文件
└── README.md                # 项目总览文档（本文件）
```

### 1.2 核心工作流程
1. **代码提交**: 学生通过前端编辑器编写代码并点击提交。
2. **预处理**: 后端去除干扰项（注释、空行等）。
3. **多维诊断**:
   - **静态分析**: 捕获语法及风格问题。
   - **动态测试**: 在 Docker 沙箱中安全执行，捕获运行时错误。
   - **机器学习分类**: 基于代码特征与 AST 路径判定错误类型。
4. **提示生成**: 根据诊断出的错误类别生成**引导式提示**（非直接答案）。
5. **结果反馈**: 前端实时展示错误高亮及提示内容。

---

## 2. 逐步安装配置指南

### 2.1 环境准备
- **操作系统**: Windows 10+, Linux (Ubuntu 20.04+), 或 macOS.
- **基础软件**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop) (推荐)
  - [Node.js 18+](https://nodejs.org/) (用于本地前端开发)
  - [Python 3.10+](https://www.python.org/) (用于本地后端开发)

### 2.2 快速启动（推荐：使用 Docker）
这是最快捷的运行方式，包含数据库、Redis、后端及前端。

```bash
# 1. 进入项目根目录
cd main

# 2. 启动所有服务
docker-compose up --build -d

# 3. 查看容器状态
docker-compose ps
```

### 2.3 初始化设置
- **数据库**: 系统启动后会自动在 MySQL 容器中创建 `tutor_db`。
- **端口映射**:
  - 前端: [http://localhost:80](http://localhost:80)
  - 后端 API: [http://localhost:8000](http://localhost:8000)
  - API 文档 (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 3. 各模块功能说明

- **学生端**: 提供沉浸式 Python 编程环境，具备语法高亮、自动保存及即时错误纠偏功能。
- **智能诊断层**: 结合了 Pylint 的严谨与随机森林模型的灵活性，能够识别逻辑错误（LogicalError）及常见异常。
- **代码沙箱**: 确保恶意代码（如死循环、敏感文件操作）不会危害服务器安全。

---

## 4. 常见问题排查 (FAQ)

**Q: Docker 启动失败，提示端口被占用？**
A: 请检查 80, 8000, 3306 端口是否被其他服务占用，可修改 `docker-compose.yml` 中的端口映射。

**Q: 前端无法连接到后端 API？**
A: 确保后端容器处于 `running` 状态，并检查 `frontend/vite.config.js` 中的代理配置。

**Q: 机器学习模型预测不准？**
A: 请参考 `ml/README.md` 了解如何使用最新数据集重新训练模型。

---

## 5. 测试验证步骤

1. 访问 [http://localhost:80](http://localhost:80)。
2. 在编辑器输入有错误的代码，例如：`print("Hello" + 123)` (TypeError)。
3. 点击「提交诊断」。
4. 验证右侧提示面板是否出现了对应的引导式建议。

---
? 2026 Python Tutor System Project. All Rights Reserved.
