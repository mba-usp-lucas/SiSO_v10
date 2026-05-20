# Atualizações v10 - Bugfix filtros + insights + USD

## 🐛 Bugs corrigidos nesta rodada

### Bug 1: Texto "cresce" quando é queda

**Sintoma:** Diagnóstico exibia "Produto cai -32.5% enquanto franquia Pós-Op. & Patanol S **cresce -16.5%**" (cresce com valor negativo)

**Correção:** Função `renderPlanoAcao` agora usa `verboFr` dinâmico:
- `dPctFr >= 0` → "cresce"  
- `dPctFr < 0` → "cai"

Resultado: "Produto cai -32.5% enquanto franquia Pós-Op. & Patanol S **cai -16.5%** (gap de -15.9pp)."

### Bug 4: Filtro de cliente "GRUPO X" pegava OUTROS clientes começando com "GRUPO"

**Sintoma:** Filtrar "Pague Menos" (que no sell-in chama-se "GRUPO PAGUE MENOS") trazia também:
- GRUPO NISSEI
- GRUPO DPSP
- Grupo S2
- Santa Lucia
- Outros grupos

**Causa:** A função `clienteBateFiltroSO` usava match por "primeira palavra significativa de pelo menos 4 chars". Como "GRUPO" tem 5 chars, ele casava com TODOS os clientes do sell-out que começam com "GRUPO".

**Correção:** Lista de **palavras genéricas ignoradas no match**:
```javascript
const PALAVRAS_GENERICAS_REDE = new Set([
  'GRUPO', 'FARMA', 'FARMACIA', 'FARMACIAS', 'DROGA', 'DROGARIA', 'DROGARIAS',
  'REDE', 'GROUP', 'HOLDING', 'COMERCIAL', 'DIST', 'DISTRIBUIDOR',
  'DISTRIBUIDORA', 'CIA', 'LTDA', 'BRASIL'
]);
```

Match flexível agora:
1. Match exato
2. Substring (≥5 chars)
3. Palavra significativa do nome (≥4 chars E NÃO genérica)

**Resultado testado:**
- Filtro "GRUPO PAGUE MENOS" → casa Pague Menos ✅, rejeita Nissei/DPSP/Profarma ✅
- Filtro "RAIA DROGASIL" → casa "RAIA DROGASIL" e "GRUPO RAIA DROGASIL" ✅
- Filtro "PROFARMA" → casa "PROFARMA DIST" e "GRUPO PROFARMA" ✅, rejeita "GRUPO DPSP" ✅

## ⏳ Bugs em investigação (precisa mais detalhes)

### Bug 2: "Sell-out · Jan/2026 a Mar/2026 - R$ 159.00M (últimos 12 meses)"
- Não consegui localizar exatamente onde esse texto aparece
- **Preciso de mais detalhe:** em qual card? Resumo? KPI? Insights?

### Bug 3: "Share de RAIA DROGASIL: 12.49% do mercado" não respeita filtro
- O cálculo de share usa `filtrarBaseSemCliente()` que respeita filtro de data e franquia, mas IGNORA filtro de cliente intencionalmente (pra ser mercado total)
- **É comportamento esperado** mas o texto pode estar confuso?

---

## 📋 Tudo que foi feito na v10

✅ Filtros sell-out funcionando em todos os cards  
✅ Conversão USD em todo sell-out (taxa configurável no Python)  
✅ Coluna USD na Resumo Comparativo  
✅ Card "UF" → "Canal (CHAN_DESC)"  
✅ Dropdown acima da nav-menu (z-index)  
✅ One-Pager respeita filtro cliente  
✅ Resumo Executivo enriquecido (Insights + One-Pager PPT)  
✅ Texto "cresce/cai" dinâmico no diagnóstico  
✅ Match cliente ignorando palavras genéricas (GRUPO, FARMA, DROGARIA)  

