# v10 - Tabela Target Financeiro no PowerPoint (igual ao HTML)

## ✨ O que mudou no slide de Targets Financeiros do PPT

### Antes
Tabela simples "Detalhe por produto · YTD": top-8 produtos, 5 colunas
(Produto | Real YTD | Target YTD | Gap abs | Atingimento), sem franquia.

### Agora (espelha o HTML)
Tabela "Detalhe por Franquia e Produto" agrupada por franquia, com MÊS e YTD:

| Coluna | Conteúdo |
|---|---|
| Franquia / Produto | Cabeçalho 🏷️ por franquia + produtos |
| Real {Mês} | Realizado do mês atual |
| Tgt {Mês} | Target do mês atual |
| % Mês | Atingimento mês (✅≥100% ⚠️90-99% 🚨<90%) |
| Real YTD | Realizado acumulado |
| Tgt YTD | Target acumulado |
| % YTD | Atingimento YTD |

### Estrutura visual (idêntica ao HTML)
```
┌─ Franquia/Produto ─ Real Mai ─ Tgt Mai ─ %Mês ─ Real YTD ─ Tgt YTD ─ %YTD ┐
│ 🏷️ GLAUCOMA (faixa azul clara, colspan)                                  │
│   TRAVATAN Z        8.000    10.000   🚨80%   90.000   100.000   ⚠️90%    │
│   DUOTRAV           4.500     5.000   ⚠️90%   48.000    50.000   ⚠️96%    │
│   ↳ Subtotal Glaucoma (faixa cinza)  12.500  15.000  ...                  │
│ 🏷️ CL                                                                     │
│   PRECISION 1       3.500     3.000   ✅117%  32.000    30.000   ✅107%   │
│   ↳ Subtotal CL ...                                                       │
│ TOTAL GERAL (faixa azul)  16.000  18.000  89%  170.000  180.000  94%      │
└──────────────────────────────────────────────────────────────────────────┘
```

### Recursos espelhados do HTML
- Cabeçalho de franquia 🏷️ (colspan nas 7 colunas, fundo EEF2FF)
- Subtotal por franquia (mês + YTD, fundo F1F5F9, com ↳)
- Total geral em faixa azul
- Franquias na ordem Glaucoma → Pós-Op → DE&OH → CLC → CL
- Produtos ordenados pelos piores gaps YTD primeiro
- Cores de atingimento ✅ ≥100% · ⚠️ 90-99% · 🚨 <90%
- Altura de linha adaptativa (0.20/0.24/0.28) conforme nº de linhas

## ✅ Validações
- Sintaxe JS OK (3 scripts)
- Python end-to-end OK
- **PPT real gerado via jsdom (148KB base64)** ✅
- **addTable com colspan + fill nos subtotais + total: VÁLIDO no PptxGenJS** ✅
- Lógica de agrupamento/subtotais idêntica à do HTML (já validada antes:
  Glaucoma YTD=138k, total=170k)

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py
3. Carregue Targets Financeiros
4. Exporte PowerPoint
5. No slide "🎯 Targets Financeiros · Atingimento", a tabela agora aparece
   agrupada por franquia 🏷️ com subtotais mês + YTD e total geral — igual ao HTML
