
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


SQLALCHEMY_DATABASE_URL = "sqlite:///./semantic_toolkit.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AnalysisLog(Base):
    """
    语义计算任务日志表，用于存储每次 API 调用记录
    """
    __tablename__ = "analysis_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(100), index=True, comment="请求路径")
    request_data = Column(JSON, comment="请求原始参数")
    response_data = Column(JSON, comment="返回结果")
    status_code = Column(Integer, default=200, comment="状态码")
    created_at = Column(DateTime, default=datetime.datetime.utcnow, comment="创建时间")

# 创建表结构
def init_db():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话的依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
