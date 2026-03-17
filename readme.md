# 语义计算工具库 (Semantic Computing Toolkit)

本项目是一个基于 **FastAPI** 和 **SQLAlchemy** 开发的科技文献语义计算工具库 API 平台。它集成了 10 个核心语义分析模块，旨在通过标准的 RESTful 接口为智能平台和知识库系统提供深度语义计算支持。

---

## 核心功能模块 (Core Modules)

本项目提供以下 10 个核心语义计算接口，基础路径统一为 `/api/v1/semantic_compute/`：

1.  **语步识别 (Move Identify)**：标注文献中的研究背景、目的、方法、结果、结论。
2.  **自动分类 (Auto Classify)**：基于中图分类法的多类目科技文献自动分类。
3.  **关键词识别 (Keyword Extract)**：从中英文文献中自动抽取关键短语。
4.  **研究问题识别 (Problem Identify)**：自动识别研究问题句及其核心短语。
5.  **引用句识别 (Citation Identify)**：识别引用句并揭示其引用情感与意图。
6.  **概念定义识别 (Concept Define Identify)**：识别文献中的概念定义句及其被定义词。
7.  **命名实体识别与关系抽取 (NER & Relation)**：支持通用与科研领域的实体识别及三元组提取。
8.  **深度聚类 (Deep Cluster)**：基于句子特征的文献自动聚合。
9.  **聚类标签生成 (Cluster Label Generate)**：为聚类结果自动生成概括性标签。
10. **结构化自动综述 (Structured Review)**：构建“研究问题-方法-进展”三层树形结构。

---

## 技术栈 (Technology Stack)

*   **Web 框架**: FastAPI (高性能异步 Python 框架)
*   **数据验证**: Pydantic v2 (强类型数据建模)
*   **ORM**: SQLAlchemy (数据库对象关系映射)
*   **数据库**: SQLite (轻量级本地数据库，用于存储 API 调用日志)
*   **ASGI 服务器**: Uvicorn

---

## 部署指南 (Deployment Guide)

### 1. 环境准备
确保您的系统已安装 Python 3.8+。建议在虚拟环境中运行。

### 2. 安装依赖
在项目根目录下执行以下命令安装必要组件：

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 3. 启动服务
运行以下命令启动 FastAPI 开发服务器：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

*   `--reload`: 代码修改后自动重启服务器（仅建议开发环境使用）。
*   `--host 0.0.0.0`: 允许外部 IP 访问。
*   `--port 8000`: 服务监听端口。

---

## 交互式 API 文档 (API Documentation)

服务启动后，您可以通过浏览器访问以下地址查看完整的 API 接口规范，并进行在线测试：

*   **Swagger UI (推荐)**: [http://localhost:8000/docs](http://localhost:8000/docs)
    *   *特点：提供完整的请求/响应示例，支持一键测试接口。*
*   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
    *   *特点：更具可读性的静态文档布局。*

---

## 项目结构 (Project Structure)

```text
.
├── main.py            # API 入口文件，定义所有路由、模型和业务逻辑
├── database.py        # 数据库配置与模型定义
├── semantic_toolkit.db # SQLite 数据库文件 (自动生成)
└── readme.md          # 部署与说明文档
```

---

## API 调用规范 (API Specification)

*   **请求方式**: 统一使用 `POST`。
*   **Content-Type**: `application/json`。
*   **响应格式**:
    ```json
    {
        "code": 200,
        "message": "success",
        "data": { ... }
    }
    ```

---

## 维护者 (Maintainer)
大模型算法/开发团队
