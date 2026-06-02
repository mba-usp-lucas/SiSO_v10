# v10 - CORREÇÃO: janela MAT do Sell-out (trazia 11 meses)

## 🐛 Problema reportado
Ao selecionar MAT, o sell-out trazia 11 meses (jun/25 a abr/26) em vez de 12.
O sell-in estava certo (jun/25 a mai/26, pois tem dado suficiente).

## 🔍 Causa raiz
O sell-out apenas CORTAVA os meses do sell-in que não tinham dado em SO:
- SI MAT: jun/25 → mai/26 (12 meses)
- SO disponível até abr/26
- Lógica antiga: filtrava SI removendo mai/26 (não tem SO) → sobravam 11 meses

## ✅ Correção
Nova função `construirPeriodoSO(per)` que monta a janela SO CORRETA:
- Usa a MESMA QUANTIDADE de meses do período de sell-in (MAT=12, QTR=3, etc.)
- Mas TERMINANDO no último mês de SO disponível (desloca a janela inteira)

Resultado para o caso MAT:
- SI: jun/25 → mai/26 (12 meses)
- SO: **mai/25 → abr/26 (12 meses completos)** ✅
- Comp SO: mai/24 → abr/25 (12 meses)

## 🔧 Aplicação
A regra foi aplicada em TODOS os ~18 pontos do código que calculavam janela SO:
- Card Comparativo SI×SO
- KPIs principais
- Resumo por rede
- Top Clientes / Top Produtos SO
- Crescimento / Queda SO
- Insights (macro + por franquia)
- Decomposição
- Slides do PowerPoint (SI×SO, Targets)
- calcularSOFranquia / calcularSOFranquiaMulti

Antes cada lugar tinha a lógica duplicada (function temNoSO + filter + fallback).
Agora todos chamam `construirPeriodoSO(per)` — fonte única de verdade.

## ✅ Validações
- Sintaxe JS OK (3 scripts inline)
- Python end-to-end OK
- Runtime no browser simulado (jsdom): XLSX ✅, sem ReferenceError ✅
- 0 ocorrências da lógica antiga restantes
- Teste do cenário MAT (jun/25→mai/26, SO até abr/26):
  - 12 meses (não 11) ✅
  - Começa em mai/25 ✅
  - Termina em abr/26 ✅
  - Comp começa em mai/24 ✅
- Teste QTR (3 meses): fev/26 a abr/26 ✅

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py
3. Selecione MAT no filtro de período
4. Veja o aviso do sell-out: "Sell-out (Mai/2025 a Abr/2026 ...)" = 12 meses
5. O comparativo SI×SO agora usa 12 meses de cada lado, deslocados pela defasagem M-2

## 💡 Nota sobre o aviso M-2
Quando o último mês de SO é diferente do último mês do SI (defasagem normal),
o aviso passa a dizer "Janela do Sell-out deslocada para os meses disponíveis"
em vez de "filtro cortado" — refletindo que agora é janela completa, não corte.
