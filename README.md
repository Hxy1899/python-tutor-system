# Python Tutor System —— 智能化编程作业纠错与提示工具

> 面向中小学 Python 编程教学场景，提供智能错误诊断 + 引导式提示 + 在线编辑器 + 教师学情分析的完整解决方案。

## ✨ 项目简介

本系统通过静态分析（pylint/flake8）、动态测试（Docker + pytest）以及基于随机森林的机器学习模型（TF‑IDF + AST 路径），精准识别学生代码中的常见错误，并生成**引导式提示**（而非直接给出答案），帮助学生自主调试与修正代码。同时提供教师端作业管理与学情统计报表，辅助教师高效教学。

## 🎯 核心功能

- **学生端**  
  - 在线 Python 编辑器（语法高亮、自动补全）  
  - 一键提交代码，获得错误类型与引导式提示  
  - 根据提示修改代码并重新提交，直至正确  

- **教师端**  
  - 查看学生作业提交列表与详情  
  - 自动生成学情统计报表（错误分布、完成进度）  
  - 轻量化批改与反馈  

- **智能诊断**  
  - 代码预处理（去注释、规范缩进）  
  - 静态分析 + 动态执行（Docker 沙箱）  
  - 机器学习错误分类（支持 SyntaxError、IndentationError、NameError、TypeError、LogicalError 等）  
  - 上下文感知的引导式提示生成  

## 🛠 技术栈

| 层级     | 技术                                          |
| -------- | --------------------------------------------- |
| 前端     | Vue 3 + CodeMirror 6 + Pinia + Axios          |
| 后端     | Python 3.10 + FastAPI + SQLAlchemy + Pydantic |
| 数据库   | MySQL 8 + Redis 7                             |
| 机器学习 | Scikit‑learn + Pandas + NumPy                 |
| 代码沙箱 | Docker (python:3.10‑slim + pytest)            |
| 静态分析 | pylint + flake8                               |
| 部署     | Docker Compose / Nginx                        |

## 📦 环境要求

- Python 3.10+
- Node.js 20+ & npm
- Docker & Docker Compose
- MySQL 8（使用 Docker 可免手动安装）
- Redis 7（使用 Docker 可免手动安装）

## 🚀 快速开始（本地运行）

### 1. 克隆项目

```bash
git clone https://github.com/Hxy1899/python-tutor-system.git
cd python-tutor-system