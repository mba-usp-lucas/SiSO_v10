# v10 - Target Financeiro no PPT + diagnóstico de libs

## 1️⃣ Target Financeiro no PowerPoint (NOVO)

### Antes
O PPT exportado não tinha slide de Targets Financeiros, mesmo se o arquivo
de targets estivesse carregado.

### Agora
Se o arquivo `Targets_Financeiros.xlsx` tem dados na métrica atual,
o PPT gera **1 slide completo** com:

- **3 cards principais** (cor adaptativa: verde/laranja/vermelho)
  - 📅 Atingimento do mês atual (Real vs Target)
  - 📊 YTD (Jan→mês: Real acumulado vs Target acumulado)
  - 🎯 Ano completo (projeção anualizada vs Target ano)
- **Tabela detalhada por produto** (Top 8 piores gaps primeiro)
  - Produto · Real YTD · Target YTD · Gap absoluto · Atingimento %
  - Cada linha colorida pelo status (✅⚠️🚨)

O slide é gerado entre os slides de Decomposição e os de Plano de Recuperação.

### Respeita filtros
- Filtro de franquia do dashboard é aplicado também no slide
- Métrica selecionada (BRL/UNID/USD) define qual coluna de target usar
- Se nenhuma target preenchida na métrica → o slide não é gerado

## 2️⃣ Banner de diagnóstico se libs não carregaram

### Problema
Se uma das libs (SheetJS, Chart.js, PptxGenJS) não carregar no browser,
o usuário só descobre quando clica num botão de export e dá alert.

### Correção
Adicionado um **banner no topo do dashboard** que detecta automaticamente
quais libs estão faltando ao carregar a página. Se algo falhar, aparece:

```
⚠️ Bibliotecas JavaScript não carregaram
Faltam: SheetJS (exportar Excel), Chart.js (gráficos)
Algumas funções podem não funcionar. Regere o HTML com a pasta libs_local/
ao lado do script Python.
```

Console também loga:
```
✅ Todas as bibliotecas carregadas: SheetJS, Chart.js, PptxGenJS
```
ou
```
❌ Bibliotecas não carregadas: SheetJS (exportar Excel)
```

## 3️⃣ Sobre o erro do Excel
Se você está com erro "SheetJS não carregada":
1. Abra o HTML no browser
2. Olha se aparece o banner vermelho no topo
3. Se aparecer → o HTML gerado pelo Python está sem a lib embutida
4. Volte ao terminal e olhe o output do `python sales_dashboard_v10.py`
5. Procure pela seção `EMBEDDING DE BIBLIOTECAS EXTERNAS`
6. Confirme que aparece `[LOCAL] SheetJS (xlsx): 639,123 bytes`

Se aparecer **`AVISO: pasta NAO existe`** → o `libs_local/` não está ao lado do `.py`
Se aparecer **`arquivo NAO encontrado`** → o `xlsx.full.min.js` não está dentro de libs_local
Se aparecer **`CRITICO: tags <script src=cdn>`** → mande print pra eu olhar

## ✅ Validações
- Sintaxe JS OK (3 scripts inline)
- Python rodou end-to-end (HTML 2.15 MB)
- 0 tags CDN no HTML final
- SheetJS embutido confirmado
- Slide Target Financeiro presente no exportPPTX
- Banner de erro adicionado e funcional

## 🧪 Como testar

1. Substitua `dashboard_template_v10.html`
2. Rode `python sales_dashboard_v10.py`
3. **Confirme no console**: aparece `[LOCAL] SheetJS (xlsx): 639,123 bytes`
4. Abra o HTML
5. **No topo da página**: NÃO deve aparecer banner vermelho (se aparecer, falta lib)
6. Console do browser (F12): deve aparecer `✅ Todas as bibliotecas carregadas`
7. Clique em exportar Excel → funciona ✅
8. Clique em exportar PowerPoint → role até o slide "Targets Financeiros" ✅
