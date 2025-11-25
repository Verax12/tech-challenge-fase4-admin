from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from src.database import Base

class Veiculo(Base):
    __tablename__ = "veiculos_admin"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    ano = Column(Integer)
    cor = Column(String)
    preco = Column(Float)
    data_cadastro = Column(DateTime, default=datetime.utcnow)