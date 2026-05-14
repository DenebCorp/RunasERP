# 🧪 Guia de Teste - Serviço de Estoque

**Data**: 2026-05-14  
**Status**: ✅ Pronto para testes

---

## 🚀 Passo 1: Subir o Ambiente

```bash
# Subir todos os serviços
docker-compose up -d

# Aguardar ~30 segundos para inicialização

# Verificar se todos estão rodando
docker-compose ps
```

**Esperado**: Todos os containers com status `Up (healthy)`

---

## 🔍 Passo 2: Verificar Health Check

```bash
# Health check do serviço de estoque
curl http://localhost:8003/health
```

**Resposta esperada**:
```json
{
  "status": "healthy",
  "service": "estoque"
}
```

---

## 🔐 Passo 3: Obter Token de Autenticação

```bash
# Login no API Gateway
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@runas.com&password=Admin@123"
```

**Copie o `access_token` da resposta!**

```bash
# Definir variável (facilita os testes)
export TOKEN="seu_access_token_aqui"
```

---

## 📦 Passo 4: Testar Endpoints de Estoque

### 4.1. Criar Produto (Pré-requisito)

Primeiro, precisamos ter um produto cadastrado:

```bash
# Criar categoria
curl -X POST http://localhost:8000/api/categorias \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Bebidas",
    "descricao": "Bebidas em geral",
    "ativo": true
  }'
```

```bash
# Criar produto
curl -X POST http://localhost:8000/api/produtos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Coca-Cola 2L",
    "descricao": "Refrigerante Coca-Cola 2 litros",
    "sku": "COCA-2L-001",
    "categoria_id": 1,
    "preco_venda": 8.50,
    "preco_custo": 6.00,
    "ativo": true
  }'
```

**Anote o `id` do produto criado!**

### 4.2. Criar Estoque

```bash
# Criar registro de estoque para o produto
curl -X POST http://localhost:8003/estoque \
  -H "Content-Type: application/json" \
  -d '{
    "produto_id": 1,
    "quantidade": 0,
    "estoque_minimo": 10,
    "estoque_maximo": 100,
    "localizacao": "Prateleira A1"
  }'
```

**Resposta esperada**:
```json
{
  "id": 1,
  "produto_id": 1,
  "variante_id": null,
  "quantidade": 0,
  "quantidade_reservada": 0,
  "quantidade_disponivel": 0,
  "estoque_minimo": 10,
  "estoque_maximo": 100,
  "localizacao": "Prateleira A1",
  "ativo": true,
  "created_at": "2026-05-14T...",
  "updated_at": "2026-05-14T..."
}
```

### 4.3. Entrada de Estoque (com Lote)

```bash
# Registrar entrada de 50 unidades com lote
curl -X POST http://localhost:8003/estoque/entrada \
  -H "Content-Type: application/json" \
  -d '{
    "produto_id": 1,
    "quantidade": 50,
    "motivo": "Compra de fornecedor",
    "documento": "NF-12345",
    "custo_unitario": 6.00,
    "criar_lote": true,
    "codigo_lote": "LOTE-2026-001",
    "data_fabricacao": "2026-05-01",
    "data_validade": "2027-05-01",
    "fornecedor": "Distribuidora ABC",
    "nota_fiscal": "NF-12345"
  }'
```

**Resposta esperada**: Estoque atualizado com quantidade = 50

### 4.4. Listar Estoque

```bash
# Listar todos os estoques
curl http://localhost:8003/estoque
```

### 4.5. Consultar Estoque Específico

```bash
# Buscar estoque por ID
curl http://localhost:8003/estoque/1
```

**Resposta esperada**: Estoque com alertas
```json
{
  "id": 1,
  "produto_id": 1,
  "quantidade": 50,
  "quantidade_disponivel": 50,
  "alerta_estoque_baixo": false,
  "alerta_estoque_zerado": false,
  ...
}
```

### 4.6. Saída de Estoque

```bash
# Registrar saída de 5 unidades
curl -X POST http://localhost:8003/estoque/saida \
  -H "Content-Type: application/json" \
  -d '{
    "produto_id": 1,
    "quantidade": 5,
    "motivo": "Venda",
    "documento": "VENDA-001"
  }'
```

**Resposta esperada**: Estoque com quantidade = 45

### 4.7. Reservar Estoque

```bash
# Reservar 10 unidades para uma venda
curl -X POST http://localhost:8003/estoque/reservar \
  -H "Content-Type: application/json" \
  -d '{
    "produto_id": 1,
    "quantidade": 10,
    "documento": "PEDIDO-001"
  }'
```

**Resposta esperada**: 
- quantidade = 45
- quantidade_reservada = 10
- quantidade_disponivel = 35

### 4.8. Liberar Reserva

```bash
# Liberar 10 unidades reservadas
curl -X POST http://localhost:8003/estoque/liberar-reserva \
  -H "Content-Type: application/json" \
  -d '{
    "produto_id": 1,
    "quantidade": 10,
    "documento": "PEDIDO-001"
  }'
```

### 4.9. Ajustar Estoque (Inventário)

```bash
# Ajustar estoque após contagem física
curl -X POST http://localhost:8003/estoque/ajuste \
  -H "Content-Type: application/json" \
  -d '{
    "estoque_id": 1,
    "quantidade_nova": 50,
    "motivo": "Ajuste de inventário",
    "observacao": "Contagem física realizada"
  }'
```

### 4.10. Listar Movimentações

```bash
# Ver histórico de movimentações do estoque
curl http://localhost:8003/estoque/1/movimentacoes
```

**Resposta esperada**: Lista de todas as movimentações (entrada, saída, ajuste, etc.)

### 4.11. Listar Lotes

```bash
# Ver lotes do estoque
curl http://localhost:8003/estoque/1/lotes
```

**Resposta esperada**: Lista de lotes com alertas de vencimento

### 4.12. Lotes Vencendo

```bash
# Ver lotes próximos do vencimento (30 dias)
curl http://localhost:8003/estoque/lotes/vencendo
```

### 4.13. Estoque Baixo

```bash
# Listar produtos com estoque abaixo do mínimo
curl http://localhost:8003/estoque/baixo
```

### 4.14. Estoque Zerado

```bash
# Listar produtos sem estoque
curl http://localhost:8003/estoque/zerado
```

### 4.15. Relatório Geral

```bash
# Relatório geral de estoque
curl http://localhost:8003/estoque/relatorios/geral
```

**Resposta esperada**:
```json
{
  "total_produtos": 1,
  "total_em_estoque": 50,
  "produtos_estoque_baixo": 0,
  "produtos_sem_estoque": 0,
  "valor_total_estoque": null
}
```

### 4.16. Relatório de Movimentações

```bash
# Relatório de movimentações do dia
curl "http://localhost:8003/estoque/relatorios/movimentacoes?data_inicio=2026-05-14T00:00:00&data_fim=2026-05-14T23:59:59"
```

---

## 🎯 Fluxo Completo de Teste

### Cenário: Entrada → Venda → Reserva → Saída

```bash
# 1. Criar estoque
curl -X POST http://localhost:8003/estoque \
  -H "Content-Type: application/json" \
  -d '{"produto_id": 1, "quantidade": 0, "estoque_minimo": 10}'

# 2. Entrada de 100 unidades
curl -X POST http://localhost:8003/estoque/entrada \
  -H "Content-Type: application/json" \
  -d '{"produto_id": 1, "quantidade": 100, "motivo": "Compra"}'

# 3. Reservar 20 unidades (carrinho)
curl -X POST http://localhost:8003/estoque/reservar \
  -H "Content-Type: application/json" \
  -d '{"produto_id": 1, "quantidade": 20, "documento": "PEDIDO-001"}'

# 4. Confirmar venda (saída)
curl -X POST http://localhost:8003/estoque/saida \
  -H "Content-Type: application/json" \
  -d '{"produto_id": 1, "quantidade": 20, "motivo": "Venda", "documento": "VENDA-001"}'

# 5. Liberar reserva
curl -X POST http://localhost:8003/estoque/liberar-reserva \
  -H "Content-Type: application/json" \
  -d '{"produto_id": 1, "quantidade": 20, "documento": "PEDIDO-001"}'

# 6. Verificar estoque final
curl http://localhost:8003/estoque/1
```

**Resultado esperado**:
- Quantidade inicial: 0
- Após entrada: 100
- Após reserva: 100 (80 disponível, 20 reservado)
- Após saída: 80 (80 disponível, 0 reservado)

---

## 🐛 Troubleshooting

### Erro: "Produto ou variante não encontrado"

**Causa**: Produto não existe no serviço de produtos  
**Solução**: Criar o produto primeiro (ver seção 4.1)

### Erro: "Quantidade disponível insuficiente"

**Causa**: Tentando retirar mais do que tem disponível  
**Solução**: Verificar quantidade disponível antes da saída

### Erro: "Já existe estoque cadastrado"

**Causa**: Tentando criar estoque duplicado  
**Solução**: Usar o estoque existente ou buscar por produto_id

### Erro 500: "Erro interno do servidor"

**Causa**: Problema na aplicação  
**Solução**: Verificar logs do container
```bash
docker-compose logs estoque --tail=50
```

---

## 📊 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/estoque` | Criar estoque |
| GET | `/estoque` | Listar estoques |
| GET | `/estoque/{id}` | Buscar estoque |
| PUT | `/estoque/{id}` | Atualizar estoque |
| GET | `/estoque/baixo` | Estoque baixo |
| GET | `/estoque/zerado` | Estoque zerado |
| POST | `/estoque/entrada` | Entrada de estoque |
| POST | `/estoque/saida` | Saída de estoque |
| POST | `/estoque/ajuste` | Ajustar estoque |
| POST | `/estoque/reservar` | Reservar estoque |
| POST | `/estoque/liberar-reserva` | Liberar reserva |
| GET | `/estoque/{id}/movimentacoes` | Listar movimentações |
| GET | `/estoque/{id}/lotes` | Listar lotes |
| GET | `/estoque/lotes/vencendo` | Lotes vencendo |
| GET | `/estoque/relatorios/geral` | Relatório geral |
| GET | `/estoque/relatorios/movimentacoes` | Relatório movimentações |

**Total**: 18 endpoints

---

## ✅ Checklist de Validação

- [ ] Health check retorna 200 OK
- [ ] Criar estoque funciona
- [ ] Entrada de estoque funciona
- [ ] Saída de estoque funciona
- [ ] Reserva de estoque funciona
- [ ] Liberação de reserva funciona
- [ ] Ajuste de estoque funciona
- [ ] Criação de lote funciona
- [ ] Listagem de movimentações funciona
- [ ] Alertas de estoque baixo funcionam
- [ ] Relatórios funcionam
- [ ] Integração com Produtos funciona

---

## 🎉 Próximos Passos

Após validar o serviço de Estoque:
1. Implementar Serviço de Vendas
2. Integrar Vendas com Estoque (baixa automática)
3. Implementar eventos RabbitMQ
4. Adicionar testes unitários

---

**Última atualização**: 2026-05-14  
**Versão**: 1.0.0

---

**Dica**: Use o Swagger UI para testar visualmente: http://localhost:8003/docs 🚀
