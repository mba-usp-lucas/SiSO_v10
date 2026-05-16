# Correções aplicadas em v10 (bugfix filtros sell-out)

## Problema
Filtro de cliente no Sell-in funcionava, mas no Sell-out NÃO. Quando filtrava "RAIA DROGASIL":
- Card Resumo: OK (intencional - mostra todas redes)
- Card Top 15 Clientes SO: OK
- Outros cards: traziam dados de TODOS os clientes ❌

## Causa raiz
A função `clienteBateFiltroSO` estava declarada DENTRO da função `renderComparativo` (escopo local).
Quando outras funções (`renderKPIs`, `renderInsights`, `renderTargets`, `renderChartSellout`,
`agregarSellout`, `exportPPTX`) tentavam usar essa função, o JavaScript falhava silenciosamente
ou retornava sempre `true` (não filtrava).

## Correção
1. **clienteBateFiltroSO movida para escopo GLOBAL** (linha ~1115)
   - Função agora é acessível por TODAS as outras funções
   - Lê `clientesSelecionados` direto (variável global)
   - Mantém o match flexível (RAIA → GRUPO RAIA DROGASIL)

2. **Filtro de cliente adicionado em 6 pontos do código**:
   - renderKPIs (linha 3812)
   - renderInsights (linha 4065)
   - renderTargets (linha 4450)
   - renderChartSellout (gráfico - linha 4863)
   - agregarSellout (linha 5200)
   - exportPPTX (3 pontos: 6532, 6966, 7363, 7771)

3. **Card "Diagnóstico por UF" → "Diagnóstico por Canal (CHAN_DESC)"**:
   - Título do menu: "🗺️ UF" → "🗺️ Canal"
   - Título do card: "Diagnóstico por UF" → "Diagnóstico por Canal (CHAN_DESC)"
   - Cabeçalho tabela: "UF" e "Estado" → apenas "Canal"
   - Insight: "São Paulo lidera..." → "{nome} lidera..."
   - Top 5: removido "(nome estado)" das colunas
   - Removido mapa hardcoded de 27 UFs (não faz mais sentido)

## Validações
- Sintaxe JS: ✅ ambos scripts inline (node --check)
- Funções globais existem: ✅ clienteBateFiltroSO, clienteEhDistribuidor, selloutCanalOk, renderUF, renderComparativo, renderKPIs, renderInsights
- Teste de match flexível:
  - Sem filtro → aceita qualquer cliente ✅
  - Filtro RAIA DROGASIL → aceita GRUPO RAIA DROGASIL ✅
  - Filtro RAIA DROGASIL → rejeita DPSP, PAGUE MENOS ✅
  - Filtro PROFARMA DIST → aceita PROFARMA ✅

## Como testar
1. Substitua dashboard_template_v10.html no seu projeto
2. Rode `python sales_dashboard_v10.py`
3. Abra HTML gerado, filtre por cliente (ex: RAIA DROGASIL)
4. Confira que TODOS os cards de sell-out agora respondem ao filtro:
   - KPIs principais
   - Insights automáticos
   - Targets (FOCO)
   - Gráfico sell-out
   - Top 15 produtos (já funcionava)
   - Crescimento/Queda (já funcionava via agregarSellout)
