# v10 - Aviso comparativo SI×SO no PPT: janela SO correta (YTD)

## 🐛 Problema reportado
No card/slide "Análise Comparativa · Sell-in × Sell-out", o aviso mostrava:
  "...× Sell-out (Abr/2026 vs Abr/2025)"  ❌ (só 1 mês)
Deveria mostrar:
  "...× Sell-out (Jan-Abr/2026 vs Mesmos meses de 2025)"  ✅ (janela YTD)

## 🔍 Causa
- HTML: o card já usava construirPeriodoSO (correto) desde a correção do YTD.
  Se ainda aparecia errado, era versão antiga do arquivo.
- PPT: o slide comparativo montava o aviso com apenas o ÚLTIMO mês de SO
  (selloutUltimoPeriodo), em vez da janela completa.

## ✅ Correção
O aviso do slide comparativo no PPT agora usa construirPeriodoSO(per):
- YTD: Sell-out (Jan/2026 a Abr/2026 vs Jan/2025 a Abr/2025)
- MAT: Sell-out (Mai/2025 a Abr/2026 vs Mai/2024 a Abr/2025)
Espelha exatamente o aviso do HTML.

Mantido intacto: o KPI "Sell-out · Abr/2026 vs Abr/2025" (variação MoM do mês
mais recente) — esse é mensal por definição e está correto.

## ✅ Validações
- Sintaxe JS OK (3 scripts)
- Python end-to-end OK
- Teste do cenário YTD:
  - HTML: Sell-out (Jan/2026 a Abr/2026 vs Jan/2025 a Abr/2025) ✅
  - PPT:  Sell-out (Jan/2026 a Abr/2026 vs Jan/2025 a Abr/2025) ✅

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py
3. Selecione YTD
4. Card "Análise Comparativa": aviso mostra Sell-out (Jan-Abr/2026 vs Jan-Abr/2025)
5. Exporte PPT: o slide comparativo mostra o mesmo período no aviso
