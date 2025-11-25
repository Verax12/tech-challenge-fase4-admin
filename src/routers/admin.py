import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Veiculo
from src.schemas import VeiculoCreate, VeiculoResponse, VeiculoUpdate
from src.config import settings

router = APIRouter(prefix="/admin", tags=["Administração de Veículos"])


@router.post("/veiculos", response_model=VeiculoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_veiculo(veiculo_in: VeiculoCreate, db: Session = Depends(get_db)):
    """
    Cadastra um veículo no Backoffice e envia para o Serviço de Vendas via HTTP.
    """
    # 1. Salva no Banco Local (Admin)
    novo_veiculo = Veiculo(
        marca=veiculo_in.marca,
        modelo=veiculo_in.modelo,
        ano=veiculo_in.ano,
        cor=veiculo_in.cor,
        preco=veiculo_in.preco
    )
    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)

    # 2. Integração: Envia para o Serviço de Vendas
    # Aqui cumprimos o requisito de comunicação via HTTP 
    try:
        payload = veiculo_in.model_dump()
        # O ID local não vai para lá, lá gera um novo ID ou usamos um UUID compartilhado.
        # Para simplificar, mandamos os dados brutos.

        response = requests.post(settings.VENDAS_API_URL, json=payload, timeout=5)

        if response.status_code != 201:
            print(f"ERRO DE INTEGRAÇÃO: O serviço de vendas retornou {response.status_code}")
            # Em um sistema real, você usaria uma fila (RabbitMQ/SQS) aqui para garantir entrega
            # ou marcaria uma flag 'sincronizado=False' no banco para tentar depois.

    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO: Não foi possível contatar o serviço de vendas. Detalhes: {e}")
        # Não falhamos o request do Admin se o Vendas estiver fora, mas logamos o erro.

    return novo_veiculo


@router.put("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def editar_veiculo(veiculo_id: int, veiculo_in: VeiculoUpdate, db: Session = Depends(get_db)):
    """
    Edita os dados de um veículo existente.
    """
    veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    # Atualiza campos se foram passados
    if veiculo_in.marca: veiculo.marca = veiculo_in.marca
    if veiculo_in.modelo: veiculo.modelo = veiculo_in.modelo
    if veiculo_in.ano: veiculo.ano = veiculo_in.ano
    if veiculo_in.cor: veiculo.cor = veiculo_in.cor
    if veiculo_in.preco: veiculo.preco = veiculo_in.preco

    db.commit()
    db.refresh(veiculo)

    # Nota: Para atualizar no Serviço de Vendas, precisaríamos de um endpoint PUT lá também.
    # Como o foco do desafio é a comunicação básica, o POST acima já valida a arquitetura.

    return veiculo