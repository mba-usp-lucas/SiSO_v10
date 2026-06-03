# v10 - Slide Crescimento Sell-out: 3 blocos MAT · YTD · Trimestre (UNIDADES)

## ✨ Slide "📦 Crescimento Sell-out por Produto · MAT · YTD · Trimestre · UNIDADES"
Reformulado para 3 blocos de comparação, cada um com anterior | atual | crescimento%.
Tudo SEMPRE em unidades (campo UNID), mesmo com métrica BRL/USD no filtro.

### Estrutura da tabela (10 colunas)
| Franquia/Produto | MAT ant | MAT atual | MAT % | YTD ant | YTD atual | YTD % | TRI ant | TRI atual | TRI % |

### Definição dos períodos (terminando no último mês de sell-out)
- **MAT**: 12 meses terminando no último SO (ex: Mai/25→Abr/26)
  vs 12 meses imediatamente anteriores (Mai/24→Abr/25)
- **YTD**: Jan→último mês de SO do ano (Jan-Abr/26) vs mesmos meses do ano anterior (Jan-Abr/25)
- **TRI**: últimos 3 meses de SO (Fev-Abr/26) vs 3 meses imediatamente anteriores (Nov/25-Jan/26)

### Características
- Sempre em UNIDADES de sell-out
- Respeita apenas o filtro de franquia
- Produtos com target → detalhados; sem target → "Outros" por franquia
- Subtotal por franquia + Total geral
- Blocos com cores distintas no cabeçalho (MAT azul-escuro, YTD azul-médio, TRI cinza)
- Crescimento: verde (+) / vermelho (-) / "novo"
- autoPage liga se houver muitos produtos

## ✅ Validações
- Sintaxe JS OK (3 scripts)
- Python end-to-end OK
- Janelas validadas (último SO = Abr/2026):
  - MAT atual = Mai/25→Abr/26 · MAT ant = Mai/24→Abr/25 ✅
  - YTD = Jan-Abr/26 vs Jan-Abr/25 ✅
  - TRI atual = Fev-Abr/26 · TRI ant = Nov/25-Jan/26 ✅
- Larguras das colunas somam ~12.1 pol (cabem no slide wide) ✅
- PPT completo gerado: 22 slides, zero erros (métrica = BRL, valores em unidades) ✅

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py
3. Exporte PowerPoint
4. Veja o slide "📦 Crescimento Sell-out por Produto" com 3 blocos:
   MAT (ant/atual/%) · YTD (ant/atual/%) · TRI (ant/atual/%), em unidades
