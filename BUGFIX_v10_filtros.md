# v10 - PPT: Novas visualizações + ícones + padronização SI/SO

## ✨ Mudanças nesta rodada

### 1. Novos slides no PPT exportado
Foram adicionados **4 novos slides** ao `exportPPTX` (botão "📊 Exportar PowerPoint"):

#### 📊 SLIDE: Análise por Franquia · Variação YoY (Evaluation)
Slide dedicado com:
- TOTAL BRASIL em destaque (fundo azul claro)
- Cada franquia abaixo
- Barras horizontais centradas em 0%
- Verde = crescimento (direita) · Vermelho = queda (esquerda)
- Escala adaptativa (±50% ou maior se necessário)
- Valores e % visíveis para cada franquia

#### 📈 SLIDE: Tendência por Systane · Últimos 12 meses
- Grid 2x2 com até 4 produtos Systane
- Cada produto: nome + total 12m + gráfico de linha
- Cores diferentes por produto
- Aplica filtros de cliente, franquia, tipo, fonte (não produto)

#### 🔀 SLIDE: Sell-in vs Sell-out · Diferença · Últimos 12 meses
- Gráfico de linha duplo: SI (azul) + SO (verde)
- Aviso de gap total embaixo com indicador (SI>SO ou SO>SI)
- Cores conforme tipo (empurrado vs demanda)
- Aplica filtros de cliente, produto, franquia, tipo

#### 🚀 SLIDE: Movers · Onde estava → Onde está
- Gráfico de linhas com 2 pontos por franquia
- Eixo X: Período Comparado | Período Atual
- Cada franquia em sua cor
- Labels com valores nas pontas

### 2. Ícones padronizados no PPT
- **🏭 SELL-IN** (substitui 📦) em todos os slides
- **💊 SELL-OUT** (substitui 🛒) em todos os slides
- Visual mais claro: fábrica (origem) → farmácia (destino)

Mudanças aplicadas em:
- One-Pager (slide único)
- s6 (Top Clientes), s7 (Top Produtos)
- s8 (Top Crescimentos), s9 (Top Quedas)
- Slide Targets (SO badges)

### 3. Padronização visual SI ↔ SO
**Cores padronizadas:** SI e SO agora usam **MESMA cor azul institucional** (`#003595`) em todos os títulos de slides:
- s6, s7, s8, s9 padronizados
- Antes: SI azul escuro + SO azul claro
- Depois: ambos no mesmo tom institucional

**Tamanhos de fonte iguais:**
- Títulos de seção: fontSize 13 (ambos)
- Resumo SI×SO no One-Pager: fontSize 12 (label) + 13 (valor) para ambos

### 4. Resumo SI×SO no One-Pager melhorado
Antes:
```
Sell-in: +5.4%  │  Sell-out: +3.5%  │  Gap: +1.9pp
```
Depois:
```
🏭 Sell-in: +5.4%  │  💊 Sell-out: +3.5%  │  Gap: +1.9pp
```

Cores das labels: azul institucional (003595) — antes era azul claro (0369A1).

---

## ✅ Validações
- Sintaxe JS OK (ambos scripts inline)
- Sintaxe Python OK
- Python rodou end-to-end (0.67 MB)
- 4 novos slides adicionados no PPT
- 10+ substituições de ícones aplicadas
- 4 padronizações de cor aplicadas

## 🧪 Como testar

1. Substitua **dashboard_template_v10.html** no projeto
2. Rode `python sales_dashboard_v10.py`
3. Abra HTML gerado
4. Clique em **📊 Exportar PowerPoint**
5. No PPT exportado, role pelos slides:
   - Confira **🏭 SELL-IN** e **💊 SELL-OUT** em todos
   - Cor uniforme nos títulos (azul institucional)
   - Novos slides ao final:
     - 📊 Análise por Franquia
     - 📈 Tendência por Systane
     - 🔀 SI vs SO Diferença
     - 🚀 Movers
6. Clique em **📄 One-Pager**
   - Resumo SI×SO com ícones 🏭/💊
   - Fonte e cor padronizadas
