# v10 - PPT: Padronização SI/SO + Análise Franquia no slide 2 + Insight por franquia

## ✨ Mudanças nesta rodada

### 1. KPIs slide 2 · Sell-out IGUAL ao Sell-in
**Problema:** Fontes do SO estavam menores que o SI no slide 2 do PPT.

**Correção:**
| Elemento | Antes (SO) | Depois (SO) |
|---|---|---|
| Valor | fontSize: 14 | **fontSize: 20** (igual SI) |
| Label | fontSize: 8 | **fontSize: 9** (igual SI) |
| Cor | azul claro (1E40AF) | **azul escuro (AZUL_ESCURO)** igual SI |
| Ícone | ↗️ (subir) | **🏪** (farmácia/loja) |
| cardHeight | 2.3 | **2.6** (acomoda fonte maior) |
| Variação % | direita superior | **abaixo do valor** (visual melhor) |

Também o ícone do SI mudou de ↘ para **🏭** (fábrica).

### 2. Análise por Franquia YoY integrada ao slide 2
**Antes:** Análise por Franquia estava no slide 19 (final).

**Agora:** Movida para o **slide 2** logo após o Benchmark.
- Slide 2 agora tem: KPIs + Benchmark + Análise por Franquia (Total + cada franquia)
- Visualização compacta com barras horizontais centradas em 0%
- TOTAL BRASIL em destaque
- Cada franquia com variação YoY

O slide 19 (sFrEval) duplicado foi **removido**.

### 3. Insight Rápido em 2 slides (separados por franquia)
**Antes:** 1 slide "💡 Insights Automáticos" com todos os insights misturados.

**Agora:** 
- Renomeado para **"💡 Insight Rápido"** (igual ao HTML)
- **Slide A**: `Insight Rápido · DE&OH + CLC + outras NÃO-PHARMA`
- **Slide B**: `Insight Rápido · PHARMA`

Cada slide tem insights calculados **especificamente para o subconjunto** de franquias:
- 📈 Performance multi-métrica
- 📊 Concentração (Top 5 clientes)
- ✅/🟢/🟡/⚠️/🚨 Performance de cada franquia individual
- 🚀 Maior alavanca
- 🔴 Maior ofensor
- 🔍 Decomposição (Volume/Preço/Mix)

**Detecção automática:** franquias contendo "PHARMA" no nome vão pro slide B, outras pro slide A.

**Fallback:** Se não detectar PHARMA, gera 1 slide único.

---

## ✅ Validações
- Sintaxe JS OK (ambos scripts inline)
- Sintaxe Python OK
- Python rodou end-to-end
- Slide sFrEval duplicado removido (65 linhas)

## 🧪 Como testar

1. Substitua **dashboard_template_v10.html** no projeto
2. Rode `python sales_dashboard_v10.py`
3. Clique em **📊 Exportar PowerPoint**
4. Verifique:
   - **Slide 2 (KPIs)**:
     - Cards Sell-in e Sell-out com **MESMO tamanho** ✅
     - Ícones 🏭 (SI) e 🏪 (SO) ✅
     - **Análise por Franquia YoY** aparece logo abaixo do Benchmark ✅
   - **Slide 3 e 4**:
     - "💡 Insight Rápido · DE&OH + CLC"
     - "💡 Insight Rápido · PHARMA"
     - Conteúdo específico de cada subgrupo ✅
