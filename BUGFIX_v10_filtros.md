# v10 - Plano de Recuperação INTEGRADO ao HTML

## ✨ Novo card "🚀 Plano de Recuperação" no dashboard

Espelha a lógica dos 6 slides do PPT, mas dentro do HTML com interatividade.

### Estrutura do card
- **Toggle entre 3 grupos** de franquias:
  - 1️⃣ DE&OH + CLC
  - 2️⃣ Glaucoma + Pós-Op/Patanol S
  - 3️⃣ CL (Lentes)
- Botões automaticamente desabilitados se o grupo não tem franquias na base
- Tooltip mostra quais franquias estão em cada grupo

### Para cada grupo, dois blocos

**📊 Diagnóstico (100% dados reais)**
- 4 KPIs: SI Atual, Variação YoY, Volume UNID, Franquias
- Decomposição V × P × Mix (com barras de % do efeito)
- SI × SO da franquia (variação + diagnóstico empurrado/demanda/alinhado)
- Top 3 produtos em queda (com valor e %)
- Top 3 clientes em queda (com valor e %)

**🎯 Plano de Ação (fixas + dinâmicas)**
- Tabela com 4-6 ações priorizadas (P1/P2/P3)
- **Ações DINÂMICAS** (marcadas com tag amarela): usam o nome real do top ofensor
  - "Plano de defesa de [PRODUTO REAL]"
  - "Reativar [CLIENTE REAL]"
  - Impacto $ = 40-50% da queda observada
- **Ações FIXAS**: sugestões padrão por tipo de franquia (farma, DE&OH/CLC, lentes)
- Impacto total estimado em destaque verde
- Disclaimer metodológico explicando como interpretar

### Export Excel completo
Botão "📥 Excel" no card gera arquivo com 4 abas:
- **Sumário**: visão geral dos 3 grupos (SI, var %, impacto)
- **Diagnóstico**: KPIs, decomposição, SI×SO e tops por grupo
- **Plano de Ação**: todas as ações de todos os grupos (com tipo Fixa/Dinâmica)
- **Metodologia**: explicação completa da lógica

## 🔧 Bugfix lateral
- `window.__perAtual` agora é salvo (estava sendo lido em vários lugares mas nunca atribuído — bug pré-existente)

## ✅ Validações
- Sintaxe JS OK (ambos scripts inline)
- Python rodou end-to-end (HTML 0.60 MB)
- Card aparece no nav: 🚀 Recuperação
- Toggle entre grupos funcional

## 🧪 Como testar

1. Substitua **dashboard_template_v10.html** no projeto
2. Rode `python sales_dashboard_v10.py`
3. Abra o HTML
4. No nav, clique em **🚀 Recuperação**
5. Use os botões para alternar entre os 3 grupos
6. Veja: diagnóstico com dados reais + plano de ação com 1-2 ações dinâmicas (com nome do top ofensor)
7. Clique em **📥 Excel** para exportar tudo (4 abas)

## 📌 Paridade com o PPT
O card HTML tem a MESMA lógica dos 6 slides do PPT:
- Mesmas franquias agrupadas
- Mesma estrutura de diagnóstico
- Mesmas regras de ações dinâmicas
- Mesmo cálculo de impacto (40-50% da queda)

Diferença: o HTML mostra um grupo por vez (com toggle), o PPT mostra os 3 grupos em sequência (6 slides).
