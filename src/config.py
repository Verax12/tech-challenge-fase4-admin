from pydantic_settings import BaseSettings

# ATENÇÃO: A palavra 'class' tem que estar encostada na esquerda (coluna 0)
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:secret@localhost:5433/admin_db"
    # URL para comunicar com o outro microsserviço
    VENDAS_API_URL: str = "http://localhost:8000/vendas/veiculos"

    class Config:
        env_file = ".env"

settings = Settings()