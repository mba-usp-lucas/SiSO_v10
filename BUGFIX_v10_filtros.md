# v10 - Fix dropdown clientes + Análise por Tipo de Cliente (Rede/Distribuidor)

## 🐛 1. Dropdown de Clientes não abria
### Causa
Os nomes de cliente eram inseridos crus no HTML do dropdown. Nomes com
caracteres especiais (& < > " ') quebravam a estrutura do dropdown,
travando a renderização da lista — comum em redes farmacêuticas
(ex: "Drogasil & Cia", "A&P").

### Correção
Escape completo de HTML em cada item do dropdown (& < > " '), aplicado a
TODOS os filtros searchable (cliente, produto, franquia, fonte, tipo).
O match interno continua correto (o browser desescapa o data-val).

## ✨ 2. Novo card/slide: Análise por Tipo de Cliente (HTML + PPT)
Espelha a "Análise por Franquia", porém agrupando por TIPO_CLIENTE
(Rede / Distribuidor) com variação YoY.

### HTML
Novo card "🏪 Análise por Tipo de Cliente" (logo abaixo do de Franquia):
- Barras de variação YoY: Total + Rede + Distribuidor
- Tabela detalhada: SI Atual, SI Δ%, SO Δ%, Gap SI-SO
- Resumo executivo (quem cresce / quem recua)
- Detecção robusta: DISTRIB* → Distribuidor; REDE/VAREJO/FARM* → Rede

### PPT
Novo slide "🏪 Análise por Tipo de Cliente · Variação YoY":
- 3 cards no topo: Total + Rede + Distribuidor (valor + Δ% YoY)
- Tabela: Tipo | SI Atual | SI Δ% YoY | SO Δ% YoY | Gap SI-SO

## ✅ Validações
- Sintaxe JS OK (3 scripts)
- Python end-to-end OK
- Runtime jsdom:
  - Dropdown cliente ABRE ✅
  - Card tipo cliente no DOM + renderTipoCliente ✅
  - Escape testado com nomes "Drogasil & Cia", "A<B", aspas ✅
- PPT completo: 21 slides (era 20, +1 tipo cliente), ZERO erros ✅

## 🧪 Como testar
1. Substitua dashboard_template_v10.html (leve o xlsx.mini.min.js junto)
2. Rode python sales_dashboard_v10.py
3. Clique no filtro "Cliente" → o dropdown agora abre normalmente
4. Veja o novo card "🏪 Análise por Tipo de Cliente" (abaixo de Franquia)
5. Exporte PowerPoint → novo slide de Tipo de Cliente com YoY
