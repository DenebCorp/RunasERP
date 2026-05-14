# Estimativa de Horas - MVP ERP Runas

Estimativa detalhada de tempo para implementação completa do MVP do ERP Runas.

## 📊 Resumo Executivo

| Categoria | Horas Estimadas |
|-----------|----------------|
| **Infraestrutura e Setup** | 16h |
| **API Gateway** | 24h |
| **Serviço de Clientes** | 40h |
| **Serviço de Produtos** | 48h |
| **Serviço de Estoque** | 32h |
| **Serviço de Vendas** | 56h |
| **Serviço Financeiro** | 40h |
| **Serviço de Notificações** | 32h |
| **Integrações Externas** | 24h |
| **Testes (100% cobertura)** | 80h |
| **Documentação** | 24h |
| **Deploy e DevOps** | 16h |
| **Buffer (20%)** | 86h |
| **TOTAL** | **518 horas** |

---

## 1. Infraestrutura e Setup (16h)

### 1.1 Docker e Docker Compose (6h)
- [x] Configuração do docker-compose.yml completo - **2h**
- [ ] Configuração de networks e volumes - **1h**
- [ ] Health checks para todos os serviços - **2h**
- [ ] Docker Compose override para dev - **1h**

### 1.2 Configuração de Bancos de Dados (4h)
- [x] Setup PostgreSQL para cada serviço - **1h**
- [x] Configuração pgAdmin com servidores - **1h**
- [ ] Scripts de backup automatizado - **2h**

### 1.3 Mensageria e Cache (4h)
- [x] Configuração RabbitMQ - **1h**
- [x] Configuração Redis - **1h**
- [ ] Setup Celery Worker e Beat - **2h**

### 1.4 Makefile e Scripts (2h)
- [x] Comandos básicos (up, down, logs) - **0.5h**
- [x] Comandos de desenvolvimento - **0.5h**
- [ ] Scripts de migração e seed - **1h**

---

## 2. API Gateway (24h)

### 2.1 Autenticação JWT (10h)
- [x] Modelos de usuário - **2h**
- [x] Geração e validação de tokens - **3h**
- [x] OAuth2 password flow - **2h**
- [x] Refresh token com Redis - **2h**
- [ ] Logout e blacklist - **1h**

### 2.2 Middlewares (6h)
- [x] Logging estruturado - **2h**
- [x] Rate limiting - **2h**
- [ ] CORS configurável - **1h**
- [ ] Error handling global - **1h**

### 2.3 Roteamento (4h)
- [ ] Proxy reverso para microsserviços - **2h**
- [ ] Validação de permissões por rota - **2h**

### 2.4 Testes (4h)
- [ ] Testes de autenticação - **2h**
- [ ] Testes de middlewares - **1h**
- [ ] Testes de integração - **1h**

---

## 3. Serviço de Clientes (40h)

### 3.1 Modelos e Schemas (6h)
- [ ] Modelo Cliente com validações - **2h**
- [ ] Modelo Endereco - **1h**
- [ ] Schemas Pydantic completos - **2h**
- [ ] Migrations Alembic - **1h**

### 3.2 Validações de Negócio (8h)
- [ ] Validação de CPF (algoritmo) - **2h**
- [ ] Validação de telefone E.164 - **1h**
- [ ] Cálculo de crédito disponível - **2h**
- [ ] Regras de bloqueio automático - **2h**
- [ ] Validação de soft delete - **1h**

### 3.3 Repositories (6h)
- [ ] ClienteRepository completo - **3h**
- [ ] EnderecoRepository - **2h**
- [ ] Queries otimizadas - **1h**

### 3.4 Services (8h)
- [ ] ClienteService com regras de negócio - **4h**
- [ ] Gestão de crédito - **2h**
- [ ] Histórico de crédito - **2h**

### 3.5 Routers (6h)
- [ ] CRUD de clientes - **2h**
- [ ] Endpoints de endereços - **2h**
- [ ] Endpoints de crédito - **1h**
- [ ] Endpoints de bloqueio - **1h**

### 3.6 Testes (6h)
- [ ] Testes de validação CPF - **1h**
- [ ] Testes de crédito - **2h**
- [ ] Testes de soft delete - **1h**
- [ ] Testes de integração - **2h**

---

## 4. Serviço de Produtos (48h)

### 4.1 Modelos e Schemas (10h)
- [ ] Modelo Categoria - **1h**
- [ ] Modelo Produto - **2h**
- [ ] Modelo Variante com atributos - **3h**
- [ ] Modelo CatalogoConfig e Fotos - **2h**
- [ ] Modelo Fornecedor e relacionamentos - **2h**

### 4.2 Validações de Negócio (8h)
- [ ] Validação de CNPJ (algoritmo) - **2h**
- [ ] Cálculo automático de preço de venda - **2h**
- [ ] Validação de SKU único - **1h**
- [ ] Regra de fornecedor principal - **2h**
- [ ] Validação de categoria com produtos - **1h**

### 4.3 Repositories (8h)
- [ ] CategoriaRepository - **1h**
- [ ] ProdutoRepository - **2h**
- [ ] VarianteRepository - **2h**
- [ ] FornecedorRepository - **2h**
- [ ] CatalogoRepository - **1h**

### 4.4 Services (10h)
- [ ] ProdutoService com regras - **4h**
- [ ] VarianteService com cálculo de preço - **3h**
- [ ] CatalogoService com integração estoque - **2h**
- [ ] FornecedorService - **1h**

### 4.5 Routers (8h)
- [ ] CRUD de categorias - **1h**
- [ ] CRUD de produtos - **2h**
- [ ] Endpoints de variantes - **2h**
- [ ] Endpoints de catálogo (admin) - **1h**
- [ ] Endpoints de catálogo (público) - **1h**
- [ ] Endpoints de fornecedores - **1h**

### 4.6 Testes (4h)
- [ ] Testes de validação CNPJ - **1h**
- [ ] Testes de cálculo de preço - **1h**
- [ ] Testes de catálogo - **1h**
- [ ] Testes de integração - **1h**

---

## 5. Serviço de Estoque (32h)

### 5.1 Modelos e Schemas (4h)
- [ ] Modelo Estoque - **1h**
- [ ] Modelo Movimentacao - **2h**
- [ ] Schemas Pydantic - **1h**

### 5.2 Validações de Negócio (6h)
- [ ] Validação de quantidade não negativa - **1h**
- [ ] Imutabilidade de movimentações - **2h**
- [ ] Transações atômicas - **2h**
- [ ] Alerta de estoque mínimo - **1h**

### 5.3 Repositories (4h)
- [ ] EstoqueRepository - **2h**
- [ ] MovimentacaoRepository - **2h**

### 5.4 Services (8h)
- [ ] EstoqueService com regras - **3h**
- [ ] Entrada de mercadoria - **1h**
- [ ] Saída de mercadoria - **1h**
- [ ] Ajuste de inventário - **1h**
- [ ] Publicação de eventos - **2h**

### 5.5 Routers (6h)
- [ ] Endpoints de consulta - **2h**
- [ ] Endpoints de movimentação - **2h**
- [ ] Endpoints de alertas - **1h**
- [ ] Histórico de movimentações - **1h**

### 5.6 Testes (4h)
- [ ] Testes de entrada/saída - **1h**
- [ ] Testes de validação - **1h**
- [ ] Testes de eventos - **1h**
- [ ] Testes de integração - **1h**

---

## 6. Serviço de Vendas (56h)

### 6.1 Modelos e Schemas (12h)
- [ ] Modelo Carrinho e ItemCarrinho - **3h**
- [ ] Modelo Pedido e ItemPedido - **3h**
- [ ] Modelo EnderecoEntrega - **1h**
- [ ] Modelo Pagamento completo - **3h**
- [ ] Schemas Pydantic complexos - **2h**

### 6.2 Validações de Negócio (12h)
- [ ] Expiração de carrinho (24h) - **2h**
- [ ] Validação de estoque disponível - **2h**
- [ ] Snapshot de preços - **2h**
- [ ] Validação de crédito (fiado) - **2h**
- [ ] Cálculo de troco - **1h**
- [ ] Validação de frete - **1h**
- [ ] Regras de status de pedido - **2h**

### 6.3 Repositories (8h)
- [ ] CarrinhoRepository - **2h**
- [ ] PedidoRepository - **3h**
- [ ] PagamentoRepository - **2h**
- [ ] Queries complexas - **1h**

### 6.4 Services (14h)
- [ ] CarrinhoService - **3h**
- [ ] CheckoutService (fluxo completo) - **5h**
- [ ] PedidoService com status - **3h**
- [ ] PagamentoService - **2h**
- [ ] Integração com outros serviços - **1h**

### 6.5 Routers (6h)
- [ ] Endpoints de carrinho (público) - **2h**
- [ ] Endpoint de checkout - **2h**
- [ ] Endpoints de pedidos (admin) - **1h**
- [ ] Webhook Mercado Pago - **1h**

### 6.6 Testes (4h)
- [ ] Testes de carrinho - **1h**
- [ ] Testes de checkout - **1h**
- [ ] Testes de webhook - **1h**
- [ ] Testes de integração - **1h**

---

## 7. Serviço Financeiro (40h)

### 7.1 Modelos e Schemas (6h)
- [ ] Modelo ContaReceber - **2h**
- [ ] Modelo PagamentoFiado - **2h**
- [ ] Schemas Pydantic - **2h**

### 7.2 Validações de Negócio (10h)
- [ ] Cálculo de data de vencimento - **2h**
- [ ] Cálculo de saldo devedor - **2h**
- [ ] Regras de quitação - **2h**
- [ ] Atualização de crédito do cliente - **2h**
- [ ] Regras de status - **2h**

### 7.3 Repositories (4h)
- [ ] ContaReceberRepository - **2h**
- [ ] PagamentoFiadoRepository - **2h**

### 7.4 Services (10h)
- [ ] FinanceiroService - **4h**
- [ ] Registro de pagamentos - **2h**
- [ ] Integração com clientes - **2h**
- [ ] Publicação de eventos - **2h**

### 7.5 Jobs Celery (6h)
- [ ] Job de vencimento diário - **3h**
- [ ] Job de lembrete (3 dias antes) - **2h**
- [ ] Configuração Celery Beat - **1h**

### 7.6 Routers (2h)
- [ ] Endpoints de contas - **1h**
- [ ] Endpoints de pagamentos - **1h**

### 7.7 Testes (2h)
- [ ] Testes de pagamento - **1h**
- [ ] Testes de jobs - **1h**

---

## 8. Serviço de Notificações (32h)

### 8.1 Modelos e Schemas (4h)
- [ ] Modelo Notificacao - **2h**
- [ ] Schemas Pydantic - **1h**
- [ ] Enums de tipos - **1h**

### 8.2 Consumer RabbitMQ (10h)
- [ ] Setup consumer base - **2h**
- [ ] Handler pedido.confirmado - **1h**
- [ ] Handler pedido.cancelado - **1h**
- [ ] Handler estoque.minimo - **1h**
- [ ] Handler cobranca.lembrete - **1h**
- [ ] Handler cobranca.vencida - **1h**
- [ ] Handler conta.quitada - **1h**
- [ ] Routing e binding - **2h**

### 8.3 Integração Evolution API (8h)
- [ ] Cliente HTTP Evolution API - **2h**
- [ ] Envio de mensagens WhatsApp - **2h**
- [ ] Tratamento de erros - **2h**
- [ ] Retry com backoff - **2h**

### 8.4 Deduplicação Redis (4h)
- [ ] Sistema de deduplicação - **2h**
- [ ] TTL e limpeza - **1h**
- [ ] Testes de deduplicação - **1h**

### 8.5 Repositories e Services (4h)
- [ ] NotificacaoRepository - **2h**
- [ ] NotificacaoService - **2h**

### 8.6 Testes (2h)
- [ ] Testes de envio - **1h**
- [ ] Testes de retry - **1h**

---

## 9. Integrações Externas (24h)

### 9.1 Mercado Pago (12h)
- [ ] Cliente HTTP Mercado Pago - **2h**
- [ ] Geração de QR Code PIX - **3h**
- [ ] Validação de webhook HMAC - **2h**
- [ ] Consulta de status de pagamento - **2h**
- [ ] Tratamento de erros - **2h**
- [ ] Testes com sandbox - **1h**

### 9.2 Evolution API (8h)
- [ ] Setup e configuração - **2h**
- [ ] Autenticação e instância - **2h**
- [ ] Templates de mensagens - **2h**
- [ ] Testes de envio - **2h**

### 9.3 Validações (4h)
- [ ] Biblioteca validate-docbr - **1h**
- [ ] Integração CPF/CNPJ - **2h**
- [ ] Testes de validação - **1h**

---

## 10. Testes - 100% Cobertura (80h)

### 10.1 Testes Unitários (40h)
- [ ] API Gateway - **6h**
- [ ] Serviço Clientes - **6h**
- [ ] Serviço Produtos - **8h**
- [ ] Serviço Estoque - **4h**
- [ ] Serviço Vendas - **8h**
- [ ] Serviço Financeiro - **4h**
- [ ] Serviço Notificações - **4h**

### 10.2 Testes de Integração (30h)
- [ ] Fluxo completo de checkout - **6h**
- [ ] Fluxo de crédito e cobrança - **6h**
- [ ] Fluxo de estoque e movimentação - **4h**
- [ ] Integração entre serviços - **8h**
- [ ] Testes de eventos RabbitMQ - **6h**

### 10.3 Testes E2E (10h)
- [ ] Cenários de usuário completos - **6h**
- [ ] Testes de performance básicos - **2h**
- [ ] Testes de carga leve - **2h**

---

## 11. Documentação (24h)

### 11.1 Documentação Técnica (12h)
- [x] README principal - **2h**
- [ ] Guia de instalação - **2h**
- [ ] Guia de desenvolvimento - **2h**
- [ ] Arquitetura e diagramas - **3h**
- [ ] API Reference - **3h**

### 11.2 Documentação de Negócio (8h)
- [ ] Regras de negócio detalhadas - **3h**
- [ ] Fluxos de processo - **2h**
- [ ] Manual de usuário básico - **3h**

### 11.3 Documentação de Deploy (4h)
- [ ] Guia de deploy - **2h**
- [ ] Troubleshooting - **1h**
- [ ] FAQ - **1h**

---

## 12. Deploy e DevOps (16h)

### 12.1 CI/CD (8h)
- [ ] GitHub Actions / GitLab CI - **3h**
- [ ] Pipeline de testes - **2h**
- [ ] Pipeline de build - **2h**
- [ ] Pipeline de deploy - **1h**

### 12.2 Monitoramento (4h)
- [ ] Health checks avançados - **2h**
- [ ] Logs centralizados - **1h**
- [ ] Métricas básicas - **1h**

### 12.3 Segurança (4h)
- [ ] Secrets management - **2h**
- [ ] SSL/TLS - **1h**
- [ ] Hardening básico - **1h**

---

## 13. Buffer e Imprevistos (86h)

Buffer de 20% sobre o total para:
- Refatorações necessárias
- Bugs não previstos
- Ajustes de requisitos
- Code review e melhorias
- Otimizações de performance

---

## 📈 Cronograma Sugerido

### Sprint 1 (2 semanas - 80h)
- Infraestrutura completa
- API Gateway
- Serviço de Clientes (parcial)

### Sprint 2 (2 semanas - 80h)
- Serviço de Clientes (completo)
- Serviço de Produtos (parcial)

### Sprint 3 (2 semanas - 80h)
- Serviço de Produtos (completo)
- Serviço de Estoque

### Sprint 4 (2 semanas - 80h)
- Serviço de Vendas (parcial)

### Sprint 5 (2 semanas - 80h)
- Serviço de Vendas (completo)
- Serviço Financeiro (parcial)

### Sprint 6 (2 semanas - 80h)
- Serviço Financeiro (completo)
- Serviço de Notificações

### Sprint 7 (1 semana - 40h)
- Integrações externas
- Testes de integração

### Sprint 8 (1 semana - 40h)
- Testes E2E
- Documentação
- Deploy

**Total: ~13 semanas (3 meses) com 1 desenvolvedor full-time**

---

## 👥 Estimativa com Equipe

### Equipe de 2 Desenvolvedores
- **Duração**: ~7 semanas (1.5 meses)
- **Divisão**: Um foca em backend core, outro em integrações

### Equipe de 3 Desenvolvedores
- **Duração**: ~5 semanas (1 mês)
- **Divisão**: Backend core, integrações, testes/documentação

---

## ⚠️ Observações Importantes

1. **Estimativas são baseadas em**:
   - Desenvolvedor sênior Python/FastAPI
   - Conhecimento prévio de microsserviços
   - Ambiente de desenvolvimento configurado
   - Requisitos estáveis

2. **Não incluído**:
   - Frontend
   - Design de UI/UX
   - Infraestrutura de produção complexa
   - Monitoramento avançado (APM, tracing)
   - Features além do MVP

3. **Riscos que podem aumentar o tempo**:
   - Mudanças de requisitos
   - Problemas de integração com APIs externas
   - Necessidade de otimizações de performance
   - Complexidade não prevista nas regras de negócio

---

## ✅ Checklist de Conclusão

- [ ] Todos os microsserviços implementados
- [ ] 100% de cobertura de testes
- [ ] Documentação completa
- [ ] CI/CD configurado
- [ ] Deploy em ambiente de staging
- [ ] Testes E2E passando
- [ ] Performance aceitável
- [ ] Segurança validada
- [ ] Code review completo
- [ ] Handover para equipe de operações

---

**Última atualização**: 2026-05-14
**Versão**: 1.0
