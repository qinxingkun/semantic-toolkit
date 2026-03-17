
from fastapi import APIRouter
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from .common import BaseResponse

router = APIRouter(prefix="/move_identify", tags=["语步识别工具"])

# --- Models ---
class StepRequest(BaseModel):
    text: str = Field(..., description="输入的科技文献文本片段")
    lang: str = Field("zh", description="语言类型: zh, en")
    doc_type: str = Field("abstract", description="文献类型: abstract, funding, paper")

class StepResult(BaseModel):
    sentence: str = Field(..., description="句子内容")
    label: str = Field(..., description="语步标签")
    score: float = Field(..., description="置信度分数")

# --- 1. Identify All ---
class AllStepsRequest(StepRequest):
    model_config = ConfigDict(json_schema_extra={"example": {
        "text": "本研究旨在解决大型语言模型在垂直领域表现不佳的问题。我们提出了一种基于DPO的对齐算法。实验表明，该方法使模型准确率提升了15%。综上所述，该方法能有效提升模型性能。",
        "lang": "zh",
        "doc_type": "abstract"
    }})

class AllStepsResponse(BaseResponse):
    data: List[StepResult]
    model_config = ConfigDict(json_schema_extra={"example": {
        "code": 200, "message": "success",
        "data": [
            {"sentence": "本研究旨在解决大型语言模型在垂直领域表现不佳的问题。", "label": "研究目的", "score": 0.98},
            {"sentence": "我们提出了一种基于DPO的对齐算法。", "label": "研究方法", "score": 0.95},
            {"sentence": "实验表明，该方法使模型准确率提升了15%。", "label": "研究结果", "score": 0.97},
            {"sentence": "综上所述，该方法能有效提升模型性能。", "label": "研究结论", "score": 0.96}
        ]
    }})

@router.post("/all", response_model=AllStepsResponse)
def identify_all(request: AllStepsRequest):
    """一键识别文本中的所有语步成分（背景、目的、方法、结果、结论）"""
    return AllStepsResponse(data=[])

# --- 2. Step Transition Analysis ---
class TransitionItem(BaseModel):
    from_step: str
    to_step: str
    logic_connective: Optional[str]

class TransitionResponse(BaseResponse):
    data: List[TransitionItem]
    model_config = ConfigDict(json_schema_extra={"example": {
        "code": 200, "message": "success",
        "data": [
            {"from_step": "研究目的", "to_step": "研究方法", "logic_connective": "通过"},
            {"from_step": "研究结果", "to_step": "研究结论", "logic_connective": "综上所述"}
        ]
    }})

@router.post("/transition_analysis", response_model=TransitionResponse)
def analyze_transition(request: AllStepsRequest):
    """分析语步之间的转换逻辑与衔接词，揭示论证脉络"""
    return TransitionResponse(data=[])

# --- 3. Step Intensity/Weight ---
class IntensityResponse(BaseResponse):
    data: Dict[str, float]
    model_config = ConfigDict(json_schema_extra={"example": {
        "code": 200, "message": "success",
        "data": {
            "研究目的": 0.15,
            "研究方法": 0.45,
            "研究结果": 0.30,
            "研究结论": 0.10
        }
    }})

@router.post("/intensity_analysis", response_model=IntensityResponse)
def analyze_intensity(request: AllStepsRequest):
    """计算各语步在文本中所占的权重比，识别研究侧重点（如：方法驱动型或结果驱动型）"""
    return IntensityResponse(data={})

# --- 4. Sequence Completeness ---
class SequenceValidationResponse(BaseResponse):
    data: Dict[str, Any]
    model_config = ConfigDict(json_schema_extra={"example": {
        "code": 200, "message": "success",
        "data": {
            "is_complete": False,
            "missing_steps": ["研究背景"],
            "score": 75.5,
            "suggestion": "缺少背景铺垫，建议增加对领域现状的描述。"
        }
    }})

@router.post("/validate_sequence", response_model=SequenceValidationResponse)
def validate_sequence(request: AllStepsRequest):
    """验证语步序列的完整性，并根据学术写作规范给出评分与改进建议"""
    return SequenceValidationResponse(data={})

# --- 5. Step Style Analysis ---
class StyleResponse(BaseResponse):
    data: Dict[str, str]
    model_config = ConfigDict(json_schema_extra={"example": {
        "code": 200, "message": "success",
        "data": {
            "研究方法": "描述性",
            "研究结果": "定量化",
            "研究结论": "推导性"
        }
    }})

@router.post("/style_analysis", response_model=StyleResponse)
def analyze_style(request: AllStepsRequest):
    """识别不同语步的写作风格（如：描述性、论证性、定量性）"""
    return StyleResponse(data={})

# --- 6. Step-Keyword Mapping ---
class MappingResponse(BaseResponse):
    data: Dict[str, List[str]]
    model_config = ConfigDict(json_schema_extra={"example": {
        "code": 200, "message": "success",
        "data": {
            "研究方法": ["DPO算法", "对齐训练", "强化学习"],
            "研究结果": ["准确率", "15%提升"]
        }
    }})

@router.post("/keyword_mapping", response_model=MappingResponse)
def map_keywords(request: AllStepsRequest):
    """提取每个语步块对应的核心关键词，实现语义对齐"""
    return MappingResponse(data={})

# --- 7. Compare Moves ---
class CompareRequest(BaseModel):
    text1: str
    text2: str
    model_config = ConfigDict(json_schema_extra={"example": {
        "text1": "摘要A内容...",
        "text2": "摘要B内容..."
    }})

class CompareResponse(BaseResponse):
    data: Dict[str, Any]
    model_config = ConfigDict(json_schema_extra={"example": {
        "code": 200, "message": "success",
        "data": {
            "structural_similarity": 0.82,
            "diff_steps": ["摘要A缺少结论语步"],
            "comparison_report": "两者在研究方法的描述深度上存在显著差异。"
        }
    }})

@router.post("/compare_structure", response_model=CompareResponse)
def compare_structure(request: CompareRequest):
    """对比两篇文献的语步结构差异，常用于范文对比或同行评审"""
    return CompareResponse(data={})

# --- 8. Batch Identify ---
class BatchStepsRequest(BaseModel):
    texts: List[str]
    model_config = ConfigDict(json_schema_extra={"example": {
        "texts": ["文本1...", "文本2..."]
    }})

class BatchStepsResponse(BaseResponse):
    data: List[List[StepResult]]
    model_config = ConfigDict(json_schema_extra={"example": {
        "code": 200, "message": "success",
        "data": [
            [{"sentence": "句子1", "label": "研究目的", "score": 0.9}],
            [{"sentence": "句子2", "label": "研究方法", "score": 0.85}]
        ]
    }})

@router.post("/batch_identify", response_model=BatchStepsResponse)
def batch_identify(request: BatchStepsRequest):
    """批量对多篇文献进行语步自动标注"""
    return BatchStepsResponse(data=[])
