# Atualizações v10 - Bugfix PPT comparativo + análise SO dinâmica

## 🐛 Bugs corrigidos nesta rodada

### Bug 1: PPT Comparativo Sell-in × Sell-out não filtrava cliente

**Sintoma:** No HTML o filtro funcionava normal. Mas ao exportar o PPT (slide "🔄 Análise Comparativa Sell-in × Sell-out"), o sell-in trazia TODAS as redes mesmo com cliente filtrado.

**Causa:** No loop de agregação do sell-in (linha ~7140) faltava o filtro de cliente:
```javascript
// ANTES (sem filtro cliente)
for(const r of rawData){
  if(fontesSetC && !fontesSetC.has(...)) continue;
  if(franquiasSetC && !franquiasSetC.has(...)) continue;
  if(tipoSetC && !tipoSetC.has(...)) continue;
  if(produtoSetC && !produtoSetC.has(...)) continue;
  // ← faltava filtro cliente aqui
```

**Correção:** Adicionado `clienteSetC` e filtro:
```javascript
const clienteSetC = clientesSelecionados.length ? new Set(clientesSelecionados) : null;
...
if(clienteSetC && !clienteSetC.has(r[COLS.CLIENTE])) continue;
```

O sell-out já tinha o filtro (via `clienteBateFiltroSO`). Agora ambos respeitam.

---

### Bug 2: Análise de quedas/crescimento Sell-out sempre mostrava M-2

**Sintoma:** Quando filtrava período YTD/MAT/range no dashboard, o card "Top 15 Quedas" e "Top 15 Crescimentos" em modo SO **sempre mostrava só Mar/2026** (último mês M-2) em vez de respeitar o filtro selecionado.

**Causa:** A função `agregarSellout(groupBy)` hardcodava `kAtual = ultMes` e `kComp = ultMes-1ano`, ignorando o `per` do filtro do dashboard.

**Correção:**

1. **`agregarSellout` agora aceita parâmetro `per` opcional:**
```javascript
function agregarSellout(groupBy, per){
  // Se per foi passado, usa período do filtro (cortado pra M-2)
  // Senão, fallback ao comportamento antigo (só último mês)
}
```

2. **12 chamadas atualizadas** para passar `per`:
   - renderTopClientesSO ✅
   - renderTopProdutosSO ✅
   - renderCrescimento (SO) ✅
   - renderQueda (SO) ✅
   - renderDiagnosticoCresce (SO) ✅
   - renderDiagnosticoQueda (SO) ✅
   - exportPPTX top clientes/produtos SO ✅

3. **Avisos visuais ajustados** para mostrar o período correto:
   - Antes: `🛒 Sell-out · Mar/2026 · M-2`
   - Agora: `🛒 Sell-out · Jan/2026 a Mar/2026 · M-2` (se filtro for YTD)

### Comportamento esperado agora
| Filtro do dashboard | Análise Quedas SO mostra |
|---|---|
| Mar/2026 único | Mar/2026 vs Mar/2025 |
| YTD 2026 | Jan-Mar/2026 vs Jan-Mar/2025 (cortado M-2) |
| MAT 12m | Abr/25-Mar/26 vs Abr/24-Mar/25 (cortado M-2) |
| Range Jan-Mar/2026 | Jan-Mar/2026 vs Jan-Mar/2025 |
| Range Jan-Mai/2026 | Jan-Mar/2026 vs Jan-Mar/2025 (avisa M-2) |

---

## ✅ Validações
- Sintaxe JS OK
- Sintaxe Python OK
- Python end-to-end rodou (0.61 MB gerado)
- 12 chamadas agregarSellout agora passam per
- 0 chamadas sem per

## 🧪 Como testar

1. Substitua `dashboard_template_v10.html` no projeto
2. Rode `python sales_dashboard_v10.py`
3. **Teste PPT comparativo:**
   - Filtre por uma rede específica (ex: RAIA DROGASIL)
   - Exporte PPT
   - Verifique slide "🔄 Análise Comparativa" — deve mostrar apenas RAIA no sell-in ✅
4. **Teste análise quedas SO com período YTD:**
   - Selecione YTD 2026 (Jan-Mar/2026)
   - Vá ao card "Top 15 Quedas e Crescimentos"
   - Troque fonte para Sell-Out
   - Verifique aviso: `🛒 Sell-out · Jan/2026 a Mar/2026 · ⚠️ M-2 · ≥50 unid`
   - Os valores na tabela devem refletir os 3 meses YTD acumulados ✅
