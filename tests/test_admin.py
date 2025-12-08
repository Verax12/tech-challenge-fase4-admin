from unittest.mock import patch, MagicMock
import requests

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "admin-service"}

def test_cadastrar_veiculo_sucesso_com_integracao(client):
    """
    Testa se o veículo é salvo no banco E se a requisição HTTP
    para o serviço de vendas é disparada corretamente.
    """
    payload = {
        "marca": "Chevrolet", "modelo": "Onix", "ano": 2023,
        "cor": "Prata", "preco": 80000.0
    }

    # MOCK: Fingimos que o requests.post retorna sucesso (201)
    # O caminho no patch deve ser onde o requests é IMPORTADO, não onde é definido
    with patch("src.routers.admin.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        # Executa a chamada real da API
        response = client.post("/admin/veiculos", json=payload)

        # 1. Verifica se salvou no banco local e retornou 201
        assert response.status_code == 201
        data = response.json()
        assert data["modelo"] == "Onix"
        assert "id" in data

        # 2. Verifica se a integração foi chamada
        mock_post.assert_called_once()
        # Verifica se enviou o JSON correto para a URL configurada
        args, kwargs = mock_post.call_args
        assert payload["marca"] == kwargs["json"]["marca"]

def test_cadastrar_veiculo_falha_integracao(client):
    """
    Testa a resiliência: O sistema deve salvar no banco local
    MESMO se o serviço de vendas estiver fora do ar.
    """
    payload = {
        "marca": "Ford", "modelo": "Ka", "ano": 2019,
        "cor": "Branco", "preco": 45000.0
    }

    # MOCK: Simulamos um erro de conexão (Serviço de Vendas caiu)
    with patch("src.routers.admin.requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectionError("Serviço indisponível")

        response = client.post("/admin/veiculos", json=payload)

        # Deve retornar 201 (criado localmente) mesmo com erro na integração
        # Pois o requisito não diz para cancelar a venda, e sim comunicar
        assert response.status_code == 201
        assert response.json()["modelo"] == "Ka"

def test_editar_veiculo(client):
    """
    Testa o fluxo de edição (PUT).
    """
    # 1. Cria veículo (mockando a integração para não dar erro no log)
    with patch("src.routers.admin.requests.post"):
        resp_create = client.post("/admin/veiculos", json={
            "marca": "Fiat", "modelo": "Toro", "ano": 2021, "cor": "Vinho", "preco": 120000.0
        })
    veiculo_id = resp_create.json()["id"]

    # 2. Atualiza o preço e a cor
    update_payload = {"cor": "Preto", "preco": 115000.0}
    resp_update = client.put(f"/admin/veiculos/{veiculo_id}", json=update_payload)

    assert resp_update.status_code == 200
    assert resp_update.json()["cor"] == "Preto"
    assert resp_update.json()["preco"] == 115000.0
    assert resp_update.json()["modelo"] == "Toro" # Mantém o original

def test_editar_veiculo_inexistente(client):
    resp = client.put("/admin/veiculos/9999", json={"cor": "Azul"})
    assert resp.status_code == 404