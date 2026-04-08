import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "Python Tutor System"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:root@localhost/tutor_db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # ML Models
    MODEL_PATH: str = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(__file__), "../../ml/models/classifier.pkl"))
    LE_PATH: str = os.getenv("LE_PATH", os.path.join(os.path.dirname(__file__), "../../ml/models/le.pkl"))
    TFIDF_PATH: str = os.getenv("TFIDF_PATH", os.path.join(os.path.dirname(__file__), "../../ml/models/tfidf.pkl"))
    
    # Sandbox
    SANDBOX_IMAGE: str = "python:3.10-slim"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-it-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    class Config:
        case_sensitive = True

settings = Settings()
