# Python Tutor System - 前端应用指南

> **版本**: 1.1.0  
> **更新日期**: 2026-04-08  
> **框架**: Vue 3 + Vite + CodeMirror 6 + Pinia + Tailwind CSS

---

## 1. 模块功能说明

前端应用提供了直观的编程与学习界面，其核心组件包括：
- **CodeEditor.vue**: 基于 CodeMirror 6 的 Python 编辑器，支持语法高亮、错误定位。
- **HintPanel.vue**: 智能提示面板，展示引导式修复建议。
- **StudentView.vue**: 学生端主视图，支持查看作业、编写代码、提交诊断。
- **TeacherView.vue**: 教师端主视图，集成了学情统计与作业管理。
- **AssignmentManage.vue**: 教师发布与编辑作业的工具。
- **StatsReport.vue**: 可视化展示错误分布与学情数据。
- **Auth (Login/Register)**: 用户登录与注册流程，支持角色区分。

---

## 2. 安装与配置指南

### 2.1 环境准备
- 安装 [Node.js 20+](https://nodejs.org/)。
- 推荐使用 [pnpm](https://pnpm.io/) 或 `npm`。

### 2.2 依赖安装
在 `frontend/` 目录下执行：
```bash
npm install
```

### 2.3 配置 API 代理
在 `vite.config.js` 中调整后端 API 代理地址，或通过环境变量 `VITE_API_BASE_URL` 配置。

---

## 3. 运行命令

### 3.1 本地开发模式 (推荐)
```bash
# 安装依赖
npm install

# 启动开发服务器 (默认端口 3000)
# 此模式支持代码热重载，并通过代理连接到后端 (localhost:8000)
npm run dev
```

### 3.2 生产环境/容器模式
请在项目根目录 `main/` 下使用 `docker-compose`：
```bash
# 启动前端 (默认映射到主机的 80 端口)
docker-compose up -d frontend
```

---

## 4. 测试与验证

### 4.1 访问与联调
1. **本地开发**: 访问 [http://localhost:3000](http://localhost:3000)。
2. **容器模式**: 访问 [http://localhost:80](http://localhost:80)。
3. **接口配置**: 开发模式下，API 请求会通过 `vite.config.js` 的 `proxy` 转发至 `localhost:8000`。

---

## 5. 运维与日志

### 5.1 日志查看
```bash
# 查看 Nginx (Docker) 日志
docker logs -f main-frontend-1
```

### 5.2 回滚方案
1. **代码回滚**: `git checkout <commit_id>`
2. **重新构建**: `docker-compose build frontend && docker-compose up -d frontend`

---

## 6. 常见问题 (FAQ)

**Q: 为什么编辑器无法加载 Python 语法高亮？**
A: 请检查 `@codemirror/lang-python` 是否已正确安装。

**Q: 刷新页面后登录状态丢失？**
A: 请检查浏览器 LocalStorage 是否禁用了 `token` 和 `user` 字段的存储。

---
? 2026 Frontend Team. Python Tutor System.
