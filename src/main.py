from fastapi import FastAPI
from src.database import engine, Base
from src.routers import admin

# Cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Principal (Admin Backoffice)",
    description="Sistema de gestão de estoque. Comunica-se com a API de Vendas.",
    version="1.0.0"
)
app.include_router(admin.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "admin-service"}