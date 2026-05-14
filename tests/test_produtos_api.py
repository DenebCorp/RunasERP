"""
Script de teste para validar os endpoints do serviço de Produtos.
"""
import requests
import json
from uuid import uuid4
from decimal import Decimal

BASE_URL = "http://localhost:8002"

# Cores para terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def test_health():
    """Testa o health check."""
    print(f"\n{BOLD}🔍 Testando Health Check{RESET}")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}✓ Health check OK{RESET}")
            print(f"  Resposta: {response.json()}")
            return True
        else:
            print(f"{RED}✗ Health check falhou: {response.status_code}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}✗ Erro ao conectar: {str(e)}{RESET}")
        return False


def test_categorias():
    """Testa CRUD de categorias."""
    print(f"\n{BOLD}🏷️  Testando Categorias{RESET}")
    
    categoria_id = None
    
    try:
        # CREATE
        print(f"\n  1. Criando categoria...")
        payload = {
            "nome": "Eletrônicos",
            "descricao": "Produtos eletrônicos em geral"
        }
        response = requests.post(f"{BASE_URL}/categorias", json=payload, timeout=5)
        if response.status_code == 201:
            categoria = response.json()
            categoria_id = categoria["id"]
            print(f"{GREEN}  ✓ Categoria criada: {categoria_id}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao criar categoria: {response.status_code}{RESET}")
            print(f"    {response.text}")
            return False

        # READ
        print(f"\n  2. Obtendo categoria...")
        response = requests.get(f"{BASE_URL}/categorias/{categoria_id}", timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}  ✓ Categoria obtida: {response.json()['nome']}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao obter categoria: {response.status_code}{RESET}")
            return False

        # LIST
        print(f"\n  3. Listando categorias...")
        response = requests.get(f"{BASE_URL}/categorias", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"{GREEN}  ✓ Total de categorias: {data['total']}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao listar categorias: {response.status_code}{RESET}")
            return False

        # UPDATE
        print(f"\n  4. Atualizando categoria...")
        payload = {"nome": "Eletrônicos Premium"}
        response = requests.put(f"{BASE_URL}/categorias/{categoria_id}", json=payload, timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}  ✓ Categoria atualizada{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao atualizar categoria: {response.status_code}{RESET}")
            return False

        return categoria_id

    except Exception as e:
        print(f"{RED}✗ Erro: {str(e)}{RESET}")
        return None


def test_produtos(categoria_id):
    """Testa CRUD de produtos."""
    print(f"\n{BOLD}📦 Testando Produtos{RESET}")
    
    produto_id = None
    
    try:
        # CREATE
        print(f"\n  1. Criando produto...")
        payload = {
            "categoria_id": categoria_id,
            "nome": "Notebook Dell XPS 13",
            "descricao": "Notebook de alto desempenho"
        }
        response = requests.post(f"{BASE_URL}/produtos", json=payload, timeout=5)
        if response.status_code == 201:
            produto = response.json()
            produto_id = produto["id"]
            print(f"{GREEN}  ✓ Produto criado: {produto_id}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao criar produto: {response.status_code}{RESET}")
            print(f"    {response.text}")
            return False

        # READ
        print(f"\n  2. Obtendo produto...")
        response = requests.get(f"{BASE_URL}/produtos/{produto_id}", timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}  ✓ Produto obtido: {response.json()['nome']}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao obter produto: {response.status_code}{RESET}")
            return False

        # LIST
        print(f"\n  3. Listando produtos...")
        response = requests.get(f"{BASE_URL}/produtos", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"{GREEN}  ✓ Total de produtos: {data['total']}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao listar produtos: {response.status_code}{RESET}")
            return False

        return produto_id

    except Exception as e:
        print(f"{RED}✗ Erro: {str(e)}{RESET}")
        return None


def test_variantes(produto_id):
    """Testa CRUD de variantes."""
    print(f"\n{BOLD}🎨 Testando Variantes{RESET}")
    
    variante_id = None
    
    try:
        # CREATE
        print(f"\n  1. Criando variante...")
        payload = {
            "produto_id": produto_id,
            "sku": "DELL-XPS-13-001",
            "preco_custo": 2500.00,
            "markup_pct": 30.0,
            "preco_venda": 3250.00,
            "atributos": [
                {"chave": "cor", "valor": "prata"},
                {"chave": "storage", "valor": "512GB SSD"}
            ]
        }
        response = requests.post(f"{BASE_URL}/variantes", json=payload, timeout=5)
        if response.status_code == 201:
            variante = response.json()
            variante_id = variante["id"]
            print(f"{GREEN}  ✓ Variante criada: {variante_id}{RESET}")
            print(f"    SKU: {variante['sku']}")
        else:
            print(f"{RED}  ✗ Erro ao criar variante: {response.status_code}{RESET}")
            print(f"    {response.text}")
            return False

        # READ
        print(f"\n  2. Obtendo variante...")
        response = requests.get(f"{BASE_URL}/variantes/{variante_id}", timeout=5)
        if response.status_code == 200:
            variante = response.json()
            print(f"{GREEN}  ✓ Variante obtida{RESET}")
            print(f"    SKU: {variante['sku']}")
            print(f"    Preço de venda: R$ {variante['preco_venda']}")
        else:
            print(f"{RED}  ✗ Erro ao obter variante: {response.status_code}{RESET}")
            return False

        # LIST BY PRODUTO
        print(f"\n  3. Listando variantes do produto...")
        response = requests.get(f"{BASE_URL}/variantes/produto/{produto_id}", timeout=5)
        if response.status_code == 200:
            variantes = response.json()
            print(f"{GREEN}  ✓ Total de variantes: {len(variantes)}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao listar variantes: {response.status_code}{RESET}")
            return False

        return variante_id

    except Exception as e:
        print(f"{RED}✗ Erro: {str(e)}{RESET}")
        return None


def test_fornecedores():
    """Testa CRUD de fornecedores."""
    print(f"\n{BOLD}🏢 Testando Fornecedores{RESET}")
    
    fornecedor_id = None
    
    try:
        # CREATE
        print(f"\n  1. Criando fornecedor...")
        payload = {
            "nome": "Dell Brasil",
            "cnpj": "00.000.000/0001-00",
            "email": "contato@dell.com.br",
            "telefone": "(11) 3000-0000",
            "cidade": "São Paulo",
            "uf": "SP"
        }
        response = requests.post(f"{BASE_URL}/fornecedores", json=payload, timeout=5)
        if response.status_code == 201:
            fornecedor = response.json()
            fornecedor_id = fornecedor["id"]
            print(f"{GREEN}  ✓ Fornecedor criado: {fornecedor_id}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao criar fornecedor: {response.status_code}{RESET}")
            print(f"    {response.text}")
            return False

        # READ
        print(f"\n  2. Obtendo fornecedor...")
        response = requests.get(f"{BASE_URL}/fornecedores/{fornecedor_id}", timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}  ✓ Fornecedor obtido: {response.json()['nome']}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao obter fornecedor: {response.status_code}{RESET}")
            return False

        # LIST
        print(f"\n  3. Listando fornecedores...")
        response = requests.get(f"{BASE_URL}/fornecedores", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"{GREEN}  ✓ Total de fornecedores: {data['total']}{RESET}")
        else:
            print(f"{RED}  ✗ Erro ao listar fornecedores: {response.status_code}{RESET}")
            return False

        return fornecedor_id

    except Exception as e:
        print(f"{RED}✗ Erro: {str(e)}{RESET}")
        return None


def main():
    """Executa todos os testes."""
    print(f"\n{BOLD}{YELLOW}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}{YELLOW}  TESTE DE ENDPOINTS - SERVIÇO DE PRODUTOS{RESET}")
    print(f"{BOLD}{YELLOW}═══════════════════════════════════════════════════════════════{RESET}")
    
    # Test health
    if not test_health():
        print(f"\n{RED}{BOLD}❌ Serviço não está respondendo!{RESET}")
        print(f"   Certifique-se de que o container de produtos está rodando.")
        print(f"   URL: {BASE_URL}")
        return

    # Test categorias
    categoria_id = test_categorias()
    if not categoria_id:
        print(f"\n{RED}{BOLD}❌ Erro ao testar categorias!{RESET}")
        return

    # Test produtos
    produto_id = test_produtos(categoria_id)
    if not produto_id:
        print(f"\n{RED}{BOLD}❌ Erro ao testar produtos!{RESET}")
        return

    # Test variantes
    variante_id = test_variantes(produto_id)
    if not variante_id:
        print(f"\n{RED}{BOLD}❌ Erro ao testar variantes!{RESET}")
        return

    # Test fornecedores
    fornecedor_id = test_fornecedores()
    if not fornecedor_id:
        print(f"\n{RED}{BOLD}❌ Erro ao testar fornecedores!{RESET}")
        return

    # Success
    print(f"\n{BOLD}{GREEN}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"{GREEN}{BOLD}✓ TODOS OS TESTES PASSARAM COM SUCESSO!{RESET}")
    print(f"{BOLD}{GREEN}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"\n{BOLD}Recursos testados:{RESET}")
    print(f"  • Categorias: {categoria_id}")
    print(f"  • Produtos: {produto_id}")
    print(f"  • Variantes: {variante_id}")
    print(f"  • Fornecedores: {fornecedor_id}")
    print()


if __name__ == "__main__":
    main()
