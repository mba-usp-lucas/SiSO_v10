# v10 - Fix dropdown clientes (lista grande) + Sell-out zerado em CL

## 🐛 BUG 1: Dropdown de clientes não mostrava a lista (3216 de 3216)
### Causa
Com bases grandes (3216 clientes), o dropdown tentava renderizar 3216 divs
+ 3216 listeners de clique de uma vez → travava o navegador. O contador
mostrava "3216 de 3216" mas a lista não aparecia.

### Correção
1. **Renderização limitada a 200 itens** por vez (mostra selecionados
   primeiro). Quando há mais, exibe aviso "+N itens. Digite na busca para
   refinar". A busca filtra normalmente entre todos os clientes.
2. **Event delegation**: UM listener no container em vez de milhares.
3. Escape de HTML mantido (& < > " ') para nomes como "Drogasil & Cia".

Resultado: dropdown abre instantâneo mesmo com 3000+ clientes; busca
funciona; seleção funciona.

## 🐛 BUG 2: Sell-out mostrava valor ao filtrar franquia CL (regressão)
### Causa
CL não tem sell-out. Após a refatoração da janela de SO, o card principal
(KPI) passou a SEMPRE criar o objeto de sell-out (mesmo com soma zero),
exibindo o bloco "Sell-out" indevidamente.

### Correção
No card KPI, se NÃO há nenhum movimento de sell-out para os filtros atuais
(atual + comp + mês + YTD todos zerados), o objeto `so` permanece null e o
bloco de sell-out NÃO é exibido — voltando ao comportamento correto:
- Franquia CL (sem SO) → bloco Sell-out OCULTO ✅
- Franquia Glaucoma (com SO) → bloco Sell-out APARECE ✅
- Sem filtro / todas → bloco Sell-out APARECE ✅

As referências de cálculo (construirPeriodoSO, _franquiaCI, filtros) foram
verificadas e continuam corretas — nenhuma foi perdida.

## ✅ Validações
- Sintaxe JS OK (3 scripts)
- Python end-to-end OK
- Dropdown 3216 itens: renderiza 200, não trava ✅
- _franquiaCI: CL≠CLC≠Glaucoma (match exato) ✅
- KPI: CL oculta SO ✅ · Glaucoma mostra SO ✅ · Todas mostra SO ✅
- PPT completo: 21 slides, zero erros estruturais ✅

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py
3. Clique no filtro "Cliente" → lista abre (200 itens + busca)
4. Selecione franquia CL → card de Sell-out fica OCULTO (correto)
5. Selecione Glaucoma → card de Sell-out aparece normalmente
