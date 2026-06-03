# v10 - Unificar "complete" + "complete mdpf" nas tabelas de crescimento

## ✨ Ajuste
Nas duas tabelas de crescimento do PowerPoint (sell-in e sell-out), os
produtos "complete" e "complete mdpf" agora são somados numa ÚNICA linha
"COMPLETE".

## 🔧 Como funciona
Helper `canonProduto(nome)` no exportPPTX:
- Qualquer produto cujo nome COMEÇA com "complete" (complete, Complete,
  COMPLETE MDPF, complete mdpf 120ml...) → unificado como "COMPLETE"
- Usa fronteira de palavra (\b) → "Completex" ou outros NÃO são afetados
- Demais produtos ficam intactos

Aplicado em:
1. Slide "📈 Crescimento por Produto" (sell-in): agregação de realizado,
   target e mapa de franquia
2. Slide "📦 Crescimento Sell-out por Produto" (MAT/YTD/TRI): agregação de
   unidades, target e franquia

Resultado: complete e complete mdpf aparecem como uma linha só, com os
valores somados (real, target e crescimentos calculados sobre o total).

## ✅ Validações
- Sintaxe JS OK (3 scripts)
- Python end-to-end OK
- canonProduto testado:
  - complete / Complete / COMPLETE MDPF / complete mdpf → "COMPLETE" ✅
  - Completex → intacto (não casa) ✅
  - TRAVATAN e demais → intactos ✅
- PPT completo: 22 slides, zero erros ✅

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py, exporte PowerPoint
3. Nas tabelas de crescimento (sell-in e sell-out), "complete" e
   "complete mdpf" aparecem como uma linha única "COMPLETE" com soma
