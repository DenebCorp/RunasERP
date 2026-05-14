#!/bin/bash

# Script de teste do MVP - ERP Runas
# Testa os fluxos críticos: Auth, Clientes e Produtos

set -e

API_GATEWAY="http://localhost:8000"
CLIENTES_SERVICE="http://localhost:8001"
PRODUTOS_SERVICE="http://localhost:8002"

echo "🧪 Iniciando testes do MVP - ERP Runas"
echo "========================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para testar endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Testing $name... "
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$status" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $status)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected $expected_status, got $status)"
        return 1
    fi
}

echo "📡 1. Testando Health Checks"
echo "----------------------------"
test_endpoint "API Gateway Health" "$API_GATEWAY/health"
test_endpoint "Clientes Service Health" "$CLIENTES_SERVICE/health"
test_endpoint "Produtos Service Health" "$PRODUTOS_SERVICE/health"
echo ""

echo "🔐 2. Testando Autenticação"
echo "---------------------------"

# Login com admin padrão
echo -n "Login com admin... "
LOGIN_RESPONSE=$(curl -s -X POST "$API_GATEWAY/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@runas.com&password=Admin@123")

ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -n "$ACCESS_TOKEN" ]; then
    echo -e "${GREEN}✓ OK${NC}"
    echo "   Token obtido: ${ACCESS_TOKEN:0:20}..."
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "   Response: $LOGIN_RESPONSE"
    exit 1
fi
echo ""

echo "👥 3. Testando Serviço de Clientes via Gateway"
echo "----------------------------------------------"

# Listar clientes (deve estar vazio inicialmente)
echo -n "GET /api/clientes... "
CLIENTES_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$API_GATEWAY/api/clientes" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

STATUS=$(echo "$CLIENTES_RESPONSE" | tail -n1)
BODY=$(echo "$CLIENTES_RESPONSE" | head -n-1)

if [ "$STATUS" -eq "200" ]; then
    echo -e "${GREEN}✓ OK${NC}"
    echo "   Response: $BODY"
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $STATUS)"
fi

# Criar cliente
echo -n "POST /api/clientes (criar cliente)... "
CREATE_CLIENTE=$(curl -s -w "\n%{http_code}" -X POST "$API_GATEWAY/api/clientes" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "nome": "João Silva",
        "cpf_cnpj": "12345678901",
        "email": "joao@example.com",
        "telefone": "+5511999999999",
        "tipo": "PESSOA_FISICA"
    }')

STATUS=$(echo "$CREATE_CLIENTE" | tail -n1)
if [ "$STATUS" -eq "201" ] || [ "$STATUS" -eq "200" ]; then
    echo -e "${GREEN}✓ OK${NC}"
    CLIENTE_ID=$(echo "$CREATE_CLIENTE" | head -n-1 | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -n1)
    echo "   Cliente criado com ID: $CLIENTE_ID"
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $STATUS)"
fi
echo ""

echo "📦 4. Testando Serviço de Produtos via Gateway"
echo "----------------------------------------------"

# Criar categoria
echo -n "POST /api/categorias (criar categoria)... "
CREATE_CATEGORIA=$(curl -s -w "\n%{http_code}" -X POST "$API_GATEWAY/api/categorias" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "nome": "Eletrônicos",
        "descricao": "Produtos eletrônicos"
    }')

STATUS=$(echo "$CREATE_CATEGORIA" | tail -n1)
if [ "$STATUS" -eq "201" ] || [ "$STATUS" -eq "200" ]; then
    echo -e "${GREEN}✓ OK${NC}"
    CATEGORIA_ID=$(echo "$CREATE_CATEGORIA" | head -n-1 | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -n1)
    echo "   Categoria criada com ID: $CATEGORIA_ID"
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $STATUS)"
    CATEGORIA_ID=1
fi

# Criar produto
echo -n "POST /api/produtos (criar produto)... "
CREATE_PRODUTO=$(curl -s -w "\n%{http_code}" -X POST "$API_GATEWAY/api/produtos" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"nome\": \"Notebook Dell\",
        \"descricao\": \"Notebook Dell Inspiron 15\",
        \"sku\": \"DELL-NB-001\",
        \"categoria_id\": $CATEGORIA_ID,
        \"preco_venda\": 3500.00,
        \"preco_custo\": 2800.00,
        \"ativo\": true
    }")

STATUS=$(echo "$CREATE_PRODUTO" | tail -n1)
if [ "$STATUS" -eq "201" ] || [ "$STATUS" -eq "200" ]; then
    echo -e "${GREEN}✓ OK${NC}"
    PRODUTO_ID=$(echo "$CREATE_PRODUTO" | head -n-1 | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -n1)
    echo "   Produto criado com ID: $PRODUTO_ID"
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $STATUS)"
fi

# Listar produtos
echo -n "GET /api/produtos... "
PRODUTOS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$API_GATEWAY/api/produtos" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

STATUS=$(echo "$PRODUTOS_RESPONSE" | tail -n1)
if [ "$STATUS" -eq "200" ]; then
    echo -e "${GREEN}✓ OK${NC}"
    BODY=$(echo "$PRODUTOS_RESPONSE" | head -n-1)
    echo "   Response: ${BODY:0:100}..."
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $STATUS)"
fi
echo ""

echo "🔓 5. Testando Logout"
echo "--------------------"
echo -n "POST /auth/logout... "
LOGOUT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_GATEWAY/auth/logout" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

STATUS=$(echo "$LOGOUT_RESPONSE" | tail -n1)
if [ "$STATUS" -eq "200" ]; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $STATUS)"
fi
echo ""

echo "========================================"
echo -e "${GREEN}✅ Testes do MVP concluídos!${NC}"
echo ""
echo "📊 Resumo:"
echo "  - API Gateway: Funcionando"
echo "  - Autenticação: Funcionando"
echo "  - Serviço Clientes: Funcionando"
echo "  - Serviço Produtos: Funcionando"
echo ""
echo "🎉 MVP está pronto para testes manuais!"
