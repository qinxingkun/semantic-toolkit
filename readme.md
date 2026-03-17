# 语义计算工具库 (Semantic Computing Toolkit)

本项目是一个专为 **科技文献深度分析** 设计的语义计算平台。基于 **FastAPI** 和 **Pydantic v2** 开发，集成了 10 个核心语义工具模块，提供了超过 **80 个** 细分功能接口。

本项目采用模块化架构，旨在为学术平台、智能综述系统及科研知识库提供高性能、标准化、且带有详尽示例的 API 支持。

---

## 核心功能模块 (10 大工具，80+ API)

所有 API 均遵循统一路径规范：`/api/v1/semantic_compute/{工具名}/{具体功能}`。

### 1. 语步识别 (Move Identify)
标标注文献摘要或全文中的研究逻辑成分。
- **特色接口**: `transition_analysis` (转换逻辑分析), `validate_sequence` (逻辑连贯性评分), `style_analysis` (写作风格识别)。

### 2. 自动分类 (Auto Classify)
基于《中图法》(CLC) 及学科门类的深度分类与标引。
- **特色接口**: `clc_full_path` (完整路径提取), `cross_disciplinary_score` (交叉学科评分), `journal_fit` (投稿期刊匹配)。

### 3. 关键词识别 (Keyword Extract)
从海量文献中提取核心术语及其语义关联。
- **特色接口**: `co_occurrence` (共现分析), `hierarchy` (上下位关系提取), `novelty_detection` (新兴词汇检测)。

### 4. 研究问题识别 (Problem Identify)
自动定位文献中的科学难题、研究空白与假设。
- **特色接口**: `identify_core` (核心问题识别), `complexity_score` (问题价值评估), `gap_analysis` (研究空白识别)。

### 5. 引用分析 (Citation Analysis)
揭示引用的学术意图、情感倾向及知识流动。
- **特色接口**: `sentiment_intensity` (情感强度分析), `density_analysis` (引用分布密度), `citation_function` (学术功能识别)。

### 6. 概念定义识别 (Concept Definition)
精准提取术语定义及其演变脉络。
- **特色接口**: `ambiguity_detection` (歧义检测), `evolution_trace` (定义演变追溯), `consistency_check` (定义一致性检测)。

### 7. 命名实体识别与关系抽取 (NER & Relation)
识别科研实体并构建三元组知识。
- **特色接口**: `event_extraction` (学术事件提取), `importance_scoring` (实体权重评估), `coref_resolution` (指代消解)。

### 8. 深度聚类 (Deep Cluster)
基于语义向量对文献集进行多维度自动聚合。
- **特色接口**: `stability_score` (聚类稳定性), `recommend_k` (最佳类簇数推荐), `viz_data` (降维可视化坐标)。

### 9. 聚类标签生成 (Cluster Labeling)
为聚类结果生成具有高度概括性的语义标签。
- **特色接口**: `representative_sentence` (代表性句子提取), `thematic_analysis` (深层主题挖掘), `multilingual_labels` (中英对照标签)。

### 10. 结构化自动综述 (Structured Review)
构建“问题-方法-进展”的三层知识图谱。
- **特色接口**: `review_tree` (结构化树形分析), `research_front` (研究前沿检测), `executive_summary` (决策级摘要)。

---

## 技术架构 (Architecture)

*   **框架**: FastAPI (异步、高性能)
*   **模型**: Pydantic v2 (严谨的数据验证与自动文档生成)
*   **结构**: 模块化路由设计，每个工具拥有独立的逻辑文件。
*   **文档**: 深度集成了 OpenAPI 规范，每个接口均包含 **中英文双语** 的详尽输入输出示例。

---

## 项目结构 (Project Structure)

```text
.
├── api/
│   ├── index.py              # 主入口，路由整合
│   ├── database.py           # 数据库与日志配置
│   └── routers/              # 10 大工具独立路由模块
│       ├── common.py         # 公共数据模型
│       ├── step_recognition.py
│       ├── auto_classification.py
│       └── ... (其它工具路由)
├── requirements.txt          # 依赖清单
├── vercel.json               # Vercel 部署配置
└── readme.md                 # 本说明文件
```

---

## 快速开始 (Quick Start)

### 本地开发
1. **安装依赖**:
   ```bash
   pip install fastapi uvicorn pydantic sqlalchemy
   ```
2. **启动服务**:
   ```bash
   uvicorn api.index:app --reload --port 8888
   ```
3. **访问文档**:
   访问 [http://localhost:8888/docs](http://localhost:8888/docs) 即可查看带 **完整请求/响应示例** 的 Swagger 文档。

### Vercel 部署
本项目已针对 Vercel 优化，可直接进行 Serverless 部署：
1. `npm i -g vercel`
2. `vercel`

---

## API 调用规范 (API Specification)

*   **统一前缀**: `/api/v1/semantic_compute`
*   **响应结构**:
    ```json
    {
        "code": 200,
        "message": "success",
        "data": { ... } // 具体业务数据
    }
    ```

---

## 联系与贡献
如有任何功能需求或 BUG 反馈，欢迎提交 Issue。
