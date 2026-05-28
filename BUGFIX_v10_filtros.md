# v10 - Target Financeiro por Produto: modelo + tabela detalhada

## ✅ Resposta à pergunta: SIM, o comparativo é automático

Ao preencher o target financeiro por produto, o dashboard calcula automaticamente:
- Atingimento do MÊS atual (Real vs Target)
- Atingimento YTD (acumulado Jan→mês)
- Atingimento ANUAL (projeção anualizada)
- **Atingimento POR PRODUTO** (tabela detalhada - melhorada nesta versão)

## ✨ Entregas desta rodada

### 1. Modelo Excel: Targets_Financeiros_modelo.xlsx
Arquivo pronto pra preencher com:
- **Aba "Targets"**: 180 linhas (15 produtos × 12 meses de 2026)
  - Produtos de exemplo das 4 franquias (Glaucoma, Pós-Op, DE&OH, CLC)
  - Colunas amarelas (TARGET_BRL, TARGET_UNID) = preencher
  - Estrutura mensal completa
- **Aba "Instruções"**: como preencher + dicas + o que o dashboard calcula

Colunas obrigatórias: FRANQUIA, PRODUTO, ANO, MES_NUM, TARGET_BRL, TARGET_UNID

⚠️ Os produtos são EXEMPLOS — ajuste para sua base real. O nome em PRODUTO deve
bater exatamente com o que aparece no dashboard (após De-Para).

### 2. Tabela "Detalhe por Produto" enriquecida
A tabela já existia, mas foi melhorada com:

| Coluna | Novo? |
|---|---|
| Produto | já tinha |
| Real YTD | já tinha |
| Target YTD | já tinha |
| **Gap (abs)** | NOVO - diferença absoluta R$/unid |
| Gap % | já tinha |
| **% Atingido** | NOVO - quanto % da meta foi atingido |

Adicionados também:
- **Contadores de status** no topo: ✅ N no alvo · ⚠️ N em alerta · 🚨 N crítico
- **Linha de TOTAL** consolidando todos os produtos
- **Legenda** explicando os critérios (✅ no alvo · ⚠️ até -10% · 🚨 abaixo)
- Ordenação pelos piores gaps primeiro (já tinha)

## Como funciona o comparativo automático

1. Você preenche TARGET_BRL e TARGET_UNID por produto/mês
2. Carrega o arquivo no dashboard (botão de upload de targets financeiros)
3. O dashboard cruza automaticamente:
   - Real (do sell-in) vs Target (do seu arquivo)
   - Por produto, somando os meses do período YTD
4. Mostra gap absoluto, gap % e % atingido com cores

### Regras importantes
- Target é a nível EMPRESA (não por cliente) → com cliente filtrado mostra N/A
- USD não tem target (só BRL e UNID)
- Produtos sem target cadastrado aparecem como "—"
- Respeita filtros de franquia e produto

---

## ✅ Validações
- Sintaxe JS OK (ambos scripts inline)
- Python rodou end-to-end
- Modelo Excel validado (180 linhas, 2 abas)

## 🧪 Como testar

1. Substitua **dashboard_template_v10.html** no projeto
2. Preencha **Targets_Financeiros_modelo.xlsx** (colunas amarelas)
3. Renomeie/aponte para seu PATH_TARGETS_FIN
4. Rode `python sales_dashboard_v10.py`
5. Abra o card "Targets Financeiros"
6. Veja: 3 cards de atingimento (mês/YTD/ano) + tabela detalhada por produto
7. A tabela mostra: Real, Target, Gap abs, Gap %, % Atingido + linha TOTAL
