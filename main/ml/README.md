# Python Tutor System - 机器学习模块指南

> **版本**: 1.0.0  
> **更新日期**: 2026-04-02  
> **算法**: 随机森林分类器 (Random Forest)

---

## 1. 模块功能说明

机器学习模块主要用于错误识别与自动分类：
- **特征提取**: 基于 Python 代码的 TF-IDF 文本特征及 AST (抽象语法树) 路径特征。
- **错误分类**: 针对 SyntaxError, IndentationError, NameError, TypeError 等多种 Python 典型错误进行分类预测。
- **推理服务**: 后端 `error_classifier.py` 模块会加载已训练好的模型进行实时推理。

---

## 2. 目录结构说明
```text
ml/
├── data/                    # 训练原始数据集 (不包含在版本库中)
├── models/                  # 已训练好的模型文件
│   ├── classifier.pkl       # 随机森林模型文件
│   ├── le.pkl               # 标签编码器文件
│   └── tfidf.pkl            # TF-IDF 特征提取器文件
├── features/                # 特征工程脚本 (如 extract_tfidf.py, extract_ast.py)
├── train.py                 # 模型训练主脚本
└── README.md                # 模块文档（本文件）
```

---

## 3. 模型更新与训练指南

### 3.1 依赖准备
```bash
# 安装机器学习相关的依赖包
pip install scikit-learn pandas numpy joblib astor
```

### 3.2 重新训练模型
如果您获得了新的学生错误数据集，可以按照以下步骤重新训练：
1. 将数据集放置在 `ml/data/` 目录下。
2. 运行训练脚本：
```bash
python train.py --data data/ --output models/
```
3. 训练完成后，新的 `.pkl` 文件将保存在 `ml/models/` 目录中。

---

## 4. 运行验证

运行后端 API 的诊断接口，若返回的 `error_type` 与预期一致，则说明模型已成功加载并进行推理。

---
? 2026 AI Team. Python Tutor System.
