from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_index_path: str = "artifacts/index.faiss"
    metadata_path: str = "artifacts/metadata.json"
    chunk_size: int = 700
    chunk_overlap: int = 100
    top_k_vector: int = 8
    top_k_bm25: int = 8
    top_k_final: int = 4
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
