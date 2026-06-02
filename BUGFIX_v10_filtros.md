# v10 - 4 novos recursos: SI×SO unidades, Top15 por canal, plano segmentado, Systane Family

## ✨ 1. Gráfico SI×SO 12 meses em UNIDADES (HTML + PPT)
- HTML: card "Sell-in vs Sell-out · Diferença" agora tem 2 gráficos:
  o de valor (métrica atual) E um novo abaixo em UNIDADES
- PPT: o slide de diferença SI×SO ganhou um 2º slide com a mesma visão
  em unidades (gap total em unidades no rodapé)

## ✨ 2. Top 15 Produtos por CANAL (PPT) - 2 slides
Antes: 1 slide só com SI×SO de todos os produtos.
Agora: 2 slides separados por TIPO_CLIENTE:
- Slide A: Top 15 produtos no canal REDE (Farmácias) · SI×SO lado a lado
- Slide B: Top 15 produtos no canal DISTRIBUIDOR · SI×SO lado a lado
Detecção robusta: "DISTRIB*" → Distribuidor; "REDE/VAREJO/FARM*" → Rede.
Sell-out usa a janela correta (construirPeriodoSO).

## ✨ 3. Plano de Ação segmentado (PPT) - 2 tabelas
Antes: 1 tabela com produtos e clientes misturados (coluna "Tipo").
Agora: 2 tabelas lado a lado no mesmo slide:
- 📦 Ações por PRODUTO (esquerda)
- 🏪 Ações por CLIENTE (direita)
Cada uma com até 7 ações ordenadas por score, com categoria (🔴🟠🟢),
impacto, Δ% e diagnóstico+ação.

## ✨ 4. Família Systane (HTML + PPT)
O card/slide "Tendência por Systane" (5 gráficos) ganhou um 6º:
- 🔷 FAMÍLIA SYSTANE = soma de TODOS os Systane EXCETO Lid Wipes
- Aparece como PRIMEIRO card, destacado (borda/fundo azul Alcon)
- Mesma visão de sparkline 12m + variação YoY

## ✅ Validações
- Sintaxe JS OK (3 scripts)
- Python end-to-end OK
- Runtime jsdom: XLSX ✅, canvas unidades no DOM ✅, sem ReferenceError ✅
- **PPT completo gerado: 20 slides, ZERO erros estruturais** ✅
  (inclui os novos: diff unidades, Top15 Rede, Top15 Distribuidor,
   plano 2 tabelas, Systane family)

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py
3. HTML:
   - Card "SI vs SO · Diferença": 2 gráficos (valor + unidades)
   - Card "Tendência Systane": 1º card = 🔷 Família Systane (destacado)
4. Exporte PowerPoint:
   - 2 slides de diferença SI×SO (valor + unidades)
   - 2 slides Top 15 Produtos (Rede / Distribuidor)
   - Slide Plano de Ação com 2 tabelas (produto / cliente)
   - Slide Systane com 6 cards (Família + 5 produtos)
