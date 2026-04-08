# Python Tutor System - 前端应用指南

> **版本**: 1.0.0  
> **更新日期**: 2026-04-02  
> **框架**: Vue 3 + Vite + CodeMirror 6 + Pinia

---

## 1. 模块功能说明

前端应用提供了直观的编程与学习界面，其核心组件包括：
- **CodeEditor.vue**: 基于 CodeMirror 6 的高性能 Python 编辑器，具备语法高亮、自动保存、错误高亮定位及代码折叠等特性。
- **HintPanel.vue**: 智能提示面板，展示由后端诊断生成的引导式修复建议。
- **StudentView.vue**: 学生端主视图，集成了代码编辑、一键提交及实时诊断反馈。
- **Auth/User Management**: 用户登录及角色切换功能。

---

## 2. 安装与配置指南

### 2.1 环境准备
- 安装 [Node.js 20+](https://nodejs.org/)。
- 推荐使用 [pnpm](https://pnpm.io/) 或 `npm` 作为包管理器。

### 2.2 依赖安装
在 `frontend/` 目录下执行：
```bash
npm install
```

### 2.3 配置 API 代理
在 `vite.config.js` 中可以调整后端 API 的代理地址，默认指向 `http://localhost:8000`。

---

## 3. 运行命令

### 3.1 本地开发模式
```bash
# 启动本地开发服务器，默认端口 3000
npm run dev
```

### 3.2 生产环境构建
```bash
# 构建静态资源文件，输出至 dist/ 目录
npm run build
```

### 3.3 生产环境预览
```bash
# 预览构建后的静态应用
npm run preview
```

---

## 4. 测试与验证

### 4.1 访问与联调
1. 确保后端 API (`http://localhost:8000`) 已启动。
2. 运行 `npm run dev` 并访问 [http://localhost:3000](http://localhost:3000)。
3. 在编辑器中输入一段包含语法错误的代码并点击提交，验证提示面板是否实时更新。

---

## 5. 常见问题 (FAQ)

**Q: 为什么编辑器无法加载 Python 语法高亮？**
A: 请检查 `@codemirror/lang-python` 是否已正确安装。

**Q: 点击提交后一直处于「提交中...」状态？**
A: 请检查后端 API 是否响应超时，或网络代理配置是否正确。

---
? 2026 Frontend Team. Python Tutor System.
