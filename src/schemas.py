from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class VeiculoBase(BaseModel):
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: float = Field(gt=0, description="Preço deve ser positivo")

    @field_validator('ano')
    def ano_valido(cls, v):
        if v < 1886 or v > datetime.now().year + 1:
            raise ValueError('Ano inválido')
        return v

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None
    cor: Optional[str] = None
    preco: Optional[float] = None

class VeiculoResponse(VeiculoBase):
    id: int
    data_cadastro: datetime

    class Config:
        from_attributes = True