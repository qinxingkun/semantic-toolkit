
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db, init_db
from .routers import (
    step_recognition,
    auto_classification,
    keyword_extraction,
    problem_identification,
    citation_analysis,
    concept_definition,
    named_entity,
    deep_clustering,
    cluster_labeling,
    structured_review
)

app = FastAPI(
    title="语义计算工具库",
    description="针对科技文献的 10 个核心语义计算功能接口，包含 80+ 个详细 API",
    version="1.2.0",
)

# 初始化数据库表
@app.on_event("startup")
def startup_event():
    init_db()

# 基础路由前缀
BASE_PREFIX = "/api/v1/semantic_compute"

# 注册所有工具的路由
app.include_router(step_recognition.router, prefix=BASE_PREFIX)
app.include_router(auto_classification.router, prefix=BASE_PREFIX)
app.include_router(keyword_extraction.router, prefix=BASE_PREFIX)
app.include_router(problem_identification.router, prefix=BASE_PREFIX)
app.include_router(citation_analysis.router, prefix=BASE_PREFIX)
app.include_router(concept_definition.router, prefix=BASE_PREFIX)
app.include_router(named_entity.router, prefix=BASE_PREFIX)
app.include_router(deep_clustering.router, prefix=BASE_PREFIX)
app.include_router(cluster_labeling.router, prefix=BASE_PREFIX)
app.include_router(structured_review.router, prefix=BASE_PREFIX)

@app.get("/")
def read_root():
    return {"message": "欢迎使用语义计算工具库 API 平台", "docs": "/docs"}
