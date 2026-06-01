# v10 - Insight Rápido enriquecido no PowerPoint

## 🎯 Problema
O card "Insight Rápido" do HTML mostrava análise rica (MACRO Brasil com
Performance, Decomposição, Concentração, Sell-out cruzado), mas no PPT
o bloco GERAL estava resumido a 2-3 linhas.

## ✅ Correção
O bloco GERAL (consolidado) de cada slide de Insight Rápido no PPT agora
traz os MESMOS insights do MACRO do HTML:

### Antes (PPT)
- Variação % do grupo
- UNID/BRL
- Decomposição (só %)

### Agora (PPT) - igual ao HTML
1. **Variação consolidada** (cabeçalho)
2. **Performance** com driver (volume vs preço/mix, com pp de diferença)
3. **Decomposição** Volume/Preço/Mix COM valores absolutos (não só %)
4. **Concentração** Top 5 clientes do grupo (com alerta se ≥80%)
5. **Sell-out cruzado**: diagnóstico de estoque empurrado / demanda /
   ruptura / equilíbrio (mesma lógica do HTML)

### Detalhe por franquia (mantido)
Cada franquia continua com suas 6 dimensões (Performance, Driver, SI×SO,
Top produtos, Movers, Top clientes).

## 🔧 Implementação
- Nova função `calcularSOFranquiaMulti()` no exportPPTX: consolida sell-out
  de um conjunto de franquias (para o bloco GERAL do grupo)
- Bloco GERAL reescrito com os 5 insights do MACRO
- Fonte adaptativa: se o slide tem muitos bullets (>14), reduz a fonte
  automaticamente (13→12 header, 11→10→9.5 bullets) para caber tudo

## ✅ Validações
- Sintaxe JS OK (3 scripts inline)
- Python rodou end-to-end (HTML gerado)
- Fonte adaptativa evita overflow do slide

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (e leve o xlsx.mini.min.js)
2. Rode python sales_dashboard_v10.py
3. Exporte PowerPoint
4. Veja os 3 slides de Insight Rápido:
   - Slide 1 (GERAL + DE&OH + CLC): bloco GERAL agora tem Performance,
     Decomposição com valores, Concentração e Sell-out cruzado
   - Compare com o card "Insight Rápido" do HTML → mesmos insights
