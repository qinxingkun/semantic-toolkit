
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Dict
from database import get_db, init_db, AnalysisLog
import json

app = FastAPI(
    title="语义计算工具库",
    description="针对科技文献的 10 个核心语义计算功能接口",
    version="1.1.0",
)

# 初始化数据库表
@app.on_event("startup")
def startup_event():
    init_db()

# --- 通用基础响应模型 (不带 Any 以便更好地支持 Swagger) ---
class BaseResponse(BaseModel):
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="提示信息")

# --- 1. 语步识别工具 (Rhetorical Move Identification) ---
class MoveIdentifyRequest(BaseModel):
    text: str = Field(..., description="输入的文本片段")
    lang: str = Field("zh", description="zh: 中文, en: 英文")
    doc_type: str = Field("abstract", description="abstract: 摘要, fund: 基金项目等")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "本研究旨在解决大型语言模型在垂直领域表现不佳的问题。我们提出了一种基于DPO的对齐算法。实验表明，该方法使模型准确率提升了15%。综上所述，该方法能有效提升模型性能。",
                "lang": "zh",
                "doc_type": "abstract"
            }
        }
    )

class MoveItem(BaseModel):
    sentence: str
    label: str

class MoveIdentifyResponseData(BaseModel):
    moves: List[MoveItem]

class MoveIdentifyResponse(BaseResponse):
    data: MoveIdentifyResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "moves": [
                        {"sentence": "本研究旨在解决大型语言模型在垂直领域表现不佳的问题。", "label": "研究目的"},
                        {"sentence": "我们提出了一种基于DPO的对齐算法。", "label": "研究方法"},
                        {"sentence": "实验表明，该方法使模型准确率提升了15%。", "label": "研究结果"},
                        {"sentence": "综上所述，该方法能有效提升模型性能。", "label": "研究结论"}
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/move_identify/", response_model=MoveIdentifyResponse, tags=["语义计算工具库"])
def move_identify(request: MoveIdentifyRequest, db: Session = Depends(get_db)):
    """从科技文献文本中自动标注出表示研究背景、研究目的、研究方法、研究结果、研究结论的句子。"""
    data = MoveIdentifyResponseData(moves=[
        {"sentence": "本研究旨在解决大型语言模型在垂直领域表现不佳的问题。", "label": "研究目的"},
        {"sentence": "我们提出了一种基于DPO的对齐算法。", "label": "研究方法"},
        {"sentence": "实验表明，该方法使模型准确率提升了15%。", "label": "研究结果"},
        {"sentence": "综上所述，该方法能有效提升模型性能。", "label": "研究结论"}
    ])
    return MoveIdentifyResponse(data=data)

# --- 2. 自动分类工具 (Automatic Classification) ---
class AutoClassifyRequest(BaseModel):
    text: str
    lang: str = "zh"
    top_k: int = 3

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "本文研究了基于Transformer架构的预训练语言模型在自然语言处理中的应用...",
                "lang": "zh",
                "top_k": 3
            }
        }
    )

class CategoryItem(BaseModel):
    category_code: str
    category_name: str
    confidence: float

class AutoClassifyResponseData(BaseModel):
    categories: List[CategoryItem]

class AutoClassifyResponse(BaseResponse):
    data: AutoClassifyResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "categories": [
                        {"category_code": "TP311.56", "category_name": "人工智能，大模型", "confidence": 0.95},
                        {"category_code": "TP391", "category_name": "信息处理(信息处理系统)", "confidence": 0.82}
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/auto_classify/", response_model=AutoClassifyResponse, tags=["语义计算工具库"])
def auto_classify(request: AutoClassifyRequest, db: Session = Depends(get_db)):
    """将输入的科技文献文本片段细分到中图分类法（不少于2105个类目）中。"""
    data = AutoClassifyResponseData(categories=[
        {"category_code": "TP311.56", "category_name": "人工智能，大模型", "confidence": 0.95},
        {"category_code": "TP391", "category_name": "信息处理(信息处理系统)", "confidence": 0.82}
    ])
    return AutoClassifyResponse(data=data)

# --- 3. 关键词识别工具 (Keyword Extraction) ---
class KeywordExtractRequest(BaseModel):
    text: str
    lang: str = "zh"
    top_k: int = 5

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "...",
                "lang": "zh",
                "top_k": 5
            }
        }
    )

class KeywordExtractResponseData(BaseModel):
    keywords: List[str]

class KeywordExtractResponse(BaseResponse):
    data: KeywordExtractResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "keywords": ["大型语言模型", "注意力机制", "提示工程", "微调", "自然语言处理"]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/keyword_extract/", response_model=KeywordExtractResponse, tags=["语义计算工具库"])
def keyword_extract(request: KeywordExtractRequest, db: Session = Depends(get_db)):
    """从输入的科技文献文本片段中自动抽取若干个中英文文献关键词。"""
    data = KeywordExtractResponseData(keywords=["大型语言模型", "注意力机制", "提示工程", "微调", "自然语言处理"])
    return KeywordExtractResponse(data=data)

# --- 4. 研究问题识别工具 (Research Problem Identification) ---
class ProblemIdentifyRequest(BaseModel):
    text: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "当前大模型在多智能体协同场景中常常出现幻觉，如何缓解多轮对话中的上下文遗忘是当前亟待解决的关键难题。"
            }
        }
    )

class ProblemItem(BaseModel):
    sentence: str
    problem_phrase: str

class ProblemIdentifyResponseData(BaseModel):
    problems: List[ProblemItem]

class ProblemIdentifyResponse(BaseResponse):
    data: ProblemIdentifyResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "problems": [
                        {
                            "sentence": "如何缓解多轮对话中的上下文遗忘是当前亟待解决的关键难题。",
                            "problem_phrase": "多轮对话中的上下文遗忘"
                        }
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/problem_identify/", response_model=ProblemIdentifyResponse, tags=["语义计算工具库"])
def problem_identify(request: ProblemIdentifyRequest, db: Session = Depends(get_db)):
    """自动识别表达文献研究问题的句子，以及该句中表达研究问题的短语。"""
    data = ProblemIdentifyResponseData(problems=[
        {
            "sentence": "如何缓解多轮对话中的上下文遗忘是当前亟待解决的关键难题。",
            "problem_phrase": "多轮对话中的上下文遗忘"
        }
    ])
    return ProblemIdentifyResponse(data=data)

# --- 5. 引用句识别工具 (Citation Sentence Identification) ---
class CitationIdentifyRequest(BaseModel):
    text: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "不同于Smith等人(2022)提出的传统RNN结构，本文采用了更高效的架构。"
            }
        }
    )

class CitationItem(BaseModel):
    sentence: str
    citation_target: str
    citation_intent: str
    citation_sentiment: str

class CitationIdentifyResponseData(BaseModel):
    citations: List[CitationItem]

class CitationIdentifyResponse(BaseResponse):
    data: CitationIdentifyResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "citations": [
                        {
                            "sentence": "不同于Smith等人(2022)提出的传统RNN结构，本文采用了更高效的架构。",
                            "citation_target": "Smith等人(2022)",
                            "citation_intent": "对比/指出不足",
                            "citation_sentiment": "negative"
                        }
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/citation_identify/", response_model=CitationIdentifyResponse, tags=["语义计算工具库"])
def citation_identify(request: CitationIdentifyRequest, db: Session = Depends(get_db)):
    """从全文中识别标注引用的句子，并揭示引用情感与引用意图。"""
    data = CitationIdentifyResponseData(citations=[
        {
            "sentence": "不同于Smith等人(2022)提出的传统RNN结构，本文采用了更高效的架构。",
            "citation_target": "Smith等人(2022)",
            "citation_intent": "对比/指出不足",
            "citation_sentiment": "negative"
        }
    ])
    return CitationIdentifyResponse(data=data)

# --- 6. 概念定义识别工具 (Concept Definition Identification) ---
class ConceptDefineIdentifyRequest(BaseModel):
    text: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "检索增强生成（RAG）是一种结合了信息检索和文本生成的技术，旨在提升大模型回答的准确性。"
            }
        }
    )

class DefinitionItem(BaseModel):
    sentence: str
    concept_term: str

class ConceptDefineIdentifyResponseData(BaseModel):
    definitions: List[DefinitionItem]

class ConceptDefineIdentifyResponse(BaseResponse):
    data: ConceptDefineIdentifyResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "definitions": [
                        {
                            "sentence": "检索增强生成（RAG）是一种结合了信息检索和文本生成的技术，旨在提升大模型回答的准确性。",
                            "concept_term": "检索增强生成（RAG）"
                        }
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/concept_define_identify/", response_model=ConceptDefineIdentifyResponse, tags=["语义计算工具库"])
def concept_define_identify(request: ConceptDefineIdentifyRequest, db: Session = Depends(get_db)):
    """自动识别描述定义概念的句子，揭示被定义的概念词。"""
    data = ConceptDefineIdentifyResponseData(definitions=[
        {
            "sentence": "检索增强生成（RAG）是一种结合了信息检索和文本生成的技术，旨在提升大模型回答的准确性。",
            "concept_term": "检索增强生成（RAG）"
        }
    ])
    return ConceptDefineIdentifyResponse(data=data)

# --- 7. 命名实体识别与关系抽取工具 (NER & Relation Extraction) ---
class NERRelationRequest(BaseModel):
    text: str
    domain_type: str = "scientific"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "张三教授在清华大学研发了ChatGLM模型。",
                "domain_type": "scientific"
            }
        }
    )

class EntityItem(BaseModel):
    entity: str
    type: str
    start: int
    end: int

class RelationItem(BaseModel):
    subject: str
    predicate: str
    object: str

class NERRelationResponseData(BaseModel):
    entities: List[EntityItem]
    relations: List[RelationItem]

class NERRelationResponse(BaseResponse):
    data: NERRelationResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "entities": [
                        {"entity": "张三", "type": "Person", "start": 0, "end": 2},
                        {"entity": "清华大学", "type": "Organization", "start": 5, "end": 9},
                        {"entity": "ChatGLM", "type": "Model/Product", "start": 12, "end": 19}
                    ],
                    "relations": [
                        {"subject": "张三", "predicate": "就职于", "object": "清华大学"},
                        {"subject": "张三", "predicate": "研发", "object": "ChatGLM"}
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/ner_and_relation/", response_model=NERRelationResponse, tags=["语义计算工具库"])
def ner_and_relation(request: NERRelationRequest, db: Session = Depends(get_db)):
    """包含实体识别与实体关系抽取。支持通用、科研、专业领域的中英文实体及关系提取。"""
    data = NERRelationResponseData(
        entities=[
            {"entity": "张三", "type": "Person", "start": 0, "end": 2},
            {"entity": "清华大学", "type": "Organization", "start": 5, "end": 9},
            {"entity": "ChatGLM", "type": "Model/Product", "start": 12, "end": 19}
        ],
        relations=[
            {"subject": "张三", "predicate": "就职于", "object": "清华大学"},
            {"subject": "张三", "predicate": "研发", "object": "ChatGLM"}
        ]
    )
    return NERRelationResponse(data=data)

# --- 8. 深度聚类工具 (Deep Clustering) ---
class DocItem(BaseModel):
    doc_id: str
    text: str

class DeepClusterRequest(BaseModel):
    documents: List[DocItem]
    target_clusters: int = 0

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "documents": [
                    {"doc_id": "doc_1", "text": "图神经网络在推荐系统中的应用..." },
                    {"doc_id": "doc_2", "text": "基于GCN的知识图谱补全机制..." }
                ],
                "target_clusters": 0
            }
        }
    )

class ClusterItem(BaseModel):
    cluster_id: str
    doc_ids: List[str]

class DeepClusterResponseData(BaseModel):
    clusters: List[ClusterItem]

class DeepClusterResponse(BaseResponse):
    data: DeepClusterResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "clusters": [
                        {"cluster_id": "cluster_01", "doc_ids": ["doc_1", "doc_2"]},
                        {"cluster_id": "cluster_02", "doc_ids": ["doc_3"]}
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/deep_cluster/", response_model=DeepClusterResponse, tags=["语义计算工具库"])
def deep_cluster(request: DeepClusterRequest, db: Session = Depends(get_db)):
    """将用户上传的多篇科技文献文本基于句子特征聚合成若干类簇。"""
    data = DeepClusterResponseData(clusters=[
        {"cluster_id": "cluster_01", "doc_ids": ["doc_1", "doc_2"]},
        {"cluster_id": "cluster_02", "doc_ids": ["doc_3"]}
    ])
    return DeepClusterResponse(data=data)

# --- 9. 聚类标签生成工具 (Cluster Label Generation) ---
class ClusterDataItem(BaseModel):
    cluster_id: str
    texts: List[str]

class ClusterLabelRequest(BaseModel):
    clusters_data: List[ClusterDataItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "clusters_data": [
                    {
                        "cluster_id": "cluster_01",
                        "texts": ["图神经网络在推荐系统中的应用...", "基于GCN的知识图谱补全机制..." ]
                    }
                ]
            }
        }
    )

class ClusterLabelItem(BaseModel):
    cluster_id: str
    label: str

class ClusterLabelResponseData(BaseModel):
    cluster_labels: List[ClusterLabelItem]

class ClusterLabelResponse(BaseResponse):
    data: ClusterLabelResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "cluster_labels": [
                        {"cluster_id": "cluster_01", "label": "图神经网络与图表示学习"}
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/cluster_label_generate/", response_model=ClusterLabelResponse, tags=["语义计算工具库"])
def cluster_label_generate(request: ClusterLabelRequest, db: Session = Depends(get_db)):
    """在深度聚类基础上，用简短、概括性的词或短语生成类簇标签。"""
    data = ClusterLabelResponseData(cluster_labels=[
        {"cluster_id": "cluster_01", "label": "图神经网络与图表示学习"}
    ])
    return ClusterLabelResponse(data=data)

# --- 10. 结构化自动综述工具 (Structured Automatic Review) ---
class StructuredReviewRequest(BaseModel):
    documents: List[DocItem]
    topic: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "documents": [{"doc_id": "doc_1", "text": "..."}],
                "topic": "大模型在K12教育中的应用"
            }
        }
    )

class ProgressItem(BaseModel):
    research_progress: str
    source_docs: List[str]

class MethodItem(BaseModel):
    research_method: str
    progress: List[ProgressItem]

class ReviewTreeItem(BaseModel):
    research_problem: str
    methods: List[MethodItem]

class StructuredReviewResponseData(BaseModel):
    review_tree: List[ReviewTreeItem]

class StructuredReviewResponse(BaseResponse):
    data: StructuredReviewResponseData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "review_tree": [
                        {
                            "research_problem": "大语言模型如何实现个性化作业设计？",
                            "methods": [
                                {
                                    "research_method": "基于RAG与多智能体协同策略",
                                    "progress": [
                                        {
                                            "research_progress": "早期采用单模型Prompt，目前演进为基于LangGraph构建多角色Agent进行出题、审核与评估的流水线(doc_1, doc_4)。",
                                            "source_docs": ["doc_1", "doc_4"]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    )

@app.post("/api/v1/semantic_compute/structured_review/", response_model=StructuredReviewResponse, tags=["语义计算工具库"])
def structured_review(request: StructuredReviewRequest, db: Session = Depends(get_db)):
    """按“研究问题-研究方法-研究进展”的三层树形结构对文献集进行综合分析。"""
    data = StructuredReviewResponseData(review_tree=[
        {
            "research_problem": "大语言模型如何实现个性化作业设计？",
            "methods": [
                {
                    "research_method": "基于RAG与多智能体协同策略",
                    "progress": [
                        {
                            "research_progress": "早期采用单模型Prompt，目前演进为基于LangGraph构建多角色Agent进行出题、审核与评估的流水线(doc_1, doc_4)。",
                            "source_docs": ["doc_1", "doc_4"]
                        }
                    ]
                }
            ]
        }
    ])
    return StructuredReviewResponse(data=data)
