# v10 - Atingimento como gap, colunas YoY, e termo "estoque crescendo"

## ✨ Ajuste 1: Atingimento como GAP (HTML + PPT)
A coluna de atingimento agora mostra a diferença vs target, não o índice:
- 110% → **+10%**
- 90% → **-10%**
- 100% → **+0%**
Cores: ✅ ≥0% (no alvo ou acima) · ⚠️ -10% a 0% · 🚨 abaixo de -10%

## ✨ Ajuste 2: Colunas de variação vs ano anterior (HTML + PPT)
A tabela de Target Financeiro ganhou 2 colunas YoY (só o %):
- **vs {ano-1} Mês**: real do mês atual vs mesmo mês do ano passado
- **vs {ano-1} YTD**: real YTD vs mesmo YTD do ano passado
Formato: ▲ +X% (cresceu) / ▼ -X% (caiu) / "novo" (sem base no ano anterior)

Tabela agora tem 9 colunas:
Franquia/Produto | Real Mês | Tgt Mês | vs Tgt Mês | vs {ano-1} Mês |
Real YTD | Tgt YTD | vs Tgt YTD | vs {ano-1} YTD

Aplicado em produtos, subtotais por franquia e total geral.

## ✨ Ajuste 3: "estoque empurrado" → "estoque crescendo"
Todos os textos visíveis trocados (8 ocorrências):
- Cards de comparativo SI×SO (HTML e PPT)
- Insights, avisos, rodapés
- Bloco "ESTOQUE CRESCENDO" no slide PPT
(A classe CSS interna 'empurrado' foi preservada — não é visível.)

## ✨ Bônus: slide SI×SO no PPT alinhado ao HTML
O slide "Análise Comparativa · Sell-in × Sell-out" agora mostra até 3 itens
por categoria/nível (antes 2), aproximando do card HTML. Mesmo formato:
📦 Produto / 🏪 Rede / 🔬 Franquia · SI +X% · SO +Y% · Gap ±Zpp,
nos 4 quadrantes (Estoque Crescendo, Ruptura, Saudável, Ambos em Queda).

## ✅ Validações
- Sintaxe JS OK (3 scripts)
- Python end-to-end OK
- Termo "empurrado" visível: 0 ocorrências
- Atingimento gap: 120/100=+20% ✅, 90/100=-10% ✅, 80/100=-20% ✅
- YoY: 120/100=▲+20% ✅, 80/100=▼-20% ✅, sem base="novo" ✅
- PPT tabela 9 colunas gerado e validado via jsdom (131KB) ✅
- Larguras das colunas somam 12.5 pol (cabem no slide) ✅

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py, carregue Targets Financeiros
3. HTML: tabela mostra atingimento como +X%/-X% e 2 colunas vs ano anterior
4. Exporte PowerPoint: slide 2 de Targets tem a tabela com gap + YoY
5. Cards SI×SO mostram "Estoque Crescendo" (não mais "empurrado")
