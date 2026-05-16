# Atualizações v10 - Resumo Executivo + USD + Bugfixes

## 📋 Mudanças nesta versão

### 🌎 1. Taxa BRL→USD configurável
- **Variável `TAXA_BRL_USD` no topo do `sales_dashboard_v10.py`** (default: 5.37)
- Para atualizar a cotação, basta editar essa linha e rodar de novo
- Exposta ao JS via `window.TAXA_BRL_USD`

### 💵 2. Conversão USD aplicada em todo sell-out
- Função global `getValorSO(r)` que respeita a métrica selecionada
- Para USD em sell-out (que não tem USD nativo): converte BRL_PPP / taxa
- Aplicada em **12 pontos do código**:
  - renderKPIs (KPIs principais)
  - renderInsights, renderTargets, renderChartSellout
  - renderDecomposicao, renderUF, renderComparativo, renderPlanoAcao
  - agregarSellout (Top 15)
  - exportPPTX (3 slides)

### 📊 3. Coluna USD na tabela Resumo Comparativo (por rede)
- **Sell-in**: usa USD nativo (Vendas_USD)
- **Sell-out**: converte BRL_PPP pela taxa (mostra `R$5.37/US$` no header)
- 3 linhas em cada seção: Unidades + Reais (R$) + USD

### 💡 4. Card Insights Automáticos enriquecido (Dashboard)
Adicionado no topo do card:
- 📈 **Performance multi-métrica**: UNID + BRL + driver (volume/preço)
- 🔍 **Decomposição** V×P×M com valores absolutos
- 📊 **Concentração** Top 5 + variação por franquia

Adicionado no final:
- 🔴 **Alerta crítico** (top crítico do Plano de Ação)
- 🚀 **Oportunidade** (top oportunidade do Plano de Ação)

### 📑 5. Resumo Executivo do One-Pager (PPT) enriquecido
Função `gerarStoryExecutivo` agora produz 5 bullets verticais:
- ▌ Performance multi-métrica (BRL + UNID)
- ▌ Decomposição Volume + Preço + Mix
- ▌ Maior alavanca + maior ofensor
- ▌ Concentração Top 5 + franquias com variação
- ▌ Alerta crítico (se houver)

Caixa do resumo ampliada (h:1.55) com bullets formatados.

### 🔄 6. Ordem de render ajustada
`renderDecomposicao` + `renderPlanoAcao` agora rodam **antes** de `renderInsights`.
Isso garante que os dados estejam disponíveis para o card Insights enriquecido.

---

## 🐛 Bugfixes anteriores (v10)

### Filtros Sell-out ignoravam cliente
- `clienteBateFiltroSO` movida para escopo GLOBAL
- Filtro de cliente aplicado em 7 cards de sell-out

### Card "UF" → "Canal (CHAN_DESC)"
- Título, tabela, ranking e insights atualizados
- Removido mapa de 27 estados (não faz sentido para canal)

### One-Pager mostrava total Brasil em vez do filtrado
- Adicionados 4 filtros antes do loop sell-out no `exportOnePager`

### Dropdown abria atrás da barra NAVEGAR
- `.searchable-list` z-index: 100 → 500
- `.filters` e `.filters-wrapper` ganham `position:relative; z-index:200`
- `.nav-menu` z-index: 100 → 50

---

## ✅ Validações
- Sintaxe JS OK (ambos scripts inline)
- Sintaxe Python OK
- Python rodou end-to-end (605 KB HTML gerado)
- 12 pontos com `getValorSO()` confirmados

## 🧪 Como testar

1. Substitua ambos arquivos no seu projeto:
   - `dashboard_template_v10.html`
   - `sales_dashboard_v10.py`

2. (Opcional) Atualize `TAXA_BRL_USD` no Python se a cotação mudou

3. Rode `python sales_dashboard_v10.py`

4. Abra o HTML gerado e teste:

   **Card "💡 Insights Automáticos"** (deve ter linhas como):
   ```
   📈 Performance: crescimento moderado de +12% em BRL (UNID +8% · BRL +12%)...
   🔍 Decomposição (BRL): Volume contribui 60%... Preço 30%... Mix 10%...
   📊 Concentração: Top 5 clientes = 65% · Franquias: PHARMA +14%, LENTES +8%
   ...
   🔴 Alerta crítico: DPSP DROGARIAS com impacto de -R$1.2M...
   🚀 Oportunidade: TOTAL 30 com impacto positivo de +R$800k...
   ```

   **Tabela "Resumo Comparativo"** (3 linhas em cada seção):
   ```
   📦 SELL-IN
   - Unidades: 1.5M    +8%
   - Reais (R$): R$48M  +12%
   - USD: US$8.9M       +12%
   
   🛒 SELL-OUT
   - Unidades: 1.2M    +6%
   - Reais (R$): R$38M  +8%
   - USD (R$5.37/US$): US$7.1M  +8%
   ```

   **One-Pager (PPT)** - bloco "📊 RESUMO EXECUTIVO":
   ```
   ▌ Performance: forte crescimento de +12% em BRL (UNID +8%) vs Mai/24-Abr/25.
   ▌ Decomposição: Volume 60% + Preço 30% + Mix 10%.
   ▌ maior alavanca CLARIL (+R$5M); maior ofensor TRAVATAN Z (-R$2M).
   ▌ Top 5 clientes = 65% do faturamento. Franquias: PHARMA +14%, LENTES +8%.
   ▌ Alerta crítico: DPSP DROGARIAS (-R$1.2M, -28%).
   ```
