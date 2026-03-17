
from pydantic import BaseModel, Field
from typing import Any

class BaseResponse(BaseModel):
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="提示信息")
    data: Any = Field(None, description="返回的具体数据内容")
