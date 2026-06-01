# v10 - Solução para erro "SheetJS não carregada" em ambiente corporativo

## 🐛 Problema reportado
Ao clicar em exportar Excel: "Biblioteca de exportação (SheetJS) não carregada".

## 🔍 Causa raiz
1. As bibliotecas JS (Chart.js, SheetJS, PptxGenJS, etc.) eram carregadas via CDN
2. Computadores corporativos da Alcon bloqueiam CDNs externos (firewall)
3. Quando o Python rodava no corporativo, falhava em baixar do CDN
4. HTML era gerado SEM as libs embutidas → comportamento quebrado

## ✅ Correção implementada

### 1. Pasta local de libs (fallback robusto)
Python agora procura as libs em `./libs_local/` ANTES de tentar o CDN:
```
INSIGHTS/
├── sales_dashboard_v10.py
├── libs_local/             ← NOVA PASTA
│   ├── xlsx.full.min.js
│   ├── chart.umd.min.js
│   ├── pptxgen.bundle.js
│   └── chartjs-plugin-datalabels.min.js
```

### 2. Função `carregar_lib` em camadas
- 1º: tenta pasta local (`libs_local/`)
- 2º: fallback para CDN
- 3º: se ambos falharem, imprime aviso BEM visível no console

### 3. Aviso claro quando libs faltam
Console agora mostra:
```
!!! ATENCAO: 1 biblioteca(s) NAO embutida(s) !!!
!  - SheetJS (xlsx)
!  Funcoes que dependem destas libs vao falhar no HTML.
!  SOLUCAO: copie os arquivos .js para ./libs_local/
```

### 4. Mensagens de erro melhoradas no HTML
Antes: "Biblioteca de exportação (SheetJS) não carregada."
Agora explica: precisa rodar com `libs_local/` ou regerar em outro ambiente.

### 5. Fallback CDN dinâmico removido do exportOnePager
Havia código que tentava carregar PptxGenJS via CDN em runtime se não estivesse
disponível (também falharia no corporativo). Substituído por mensagem clara.

## 📦 Arquivos entregues

### libs_local.zip (536K)
ZIP com as 4 bibliotecas .js. Você descompacta e coloca a pasta `libs_local/`
ao lado do `sales_dashboard_v10.py`.

### LEIA_PRIMEIRO_libs_local.md
Instruções passo-a-passo de como configurar.

### dashboard_template_v10.html + sales_dashboard_v10.py
Versões atualizadas.

## ✅ Validações
- Sintaxe Python OK
- Sintaxe JS OK
- Teste end-to-end com libs locais:
  - 4 libs embutidas ✅
  - 0 referências a CDN no HTML final ✅
  - SheetJS confirmado embutido (9 refs internas) ✅
  - HTML 2.14 MB (inclui as libs)

## 🧪 Como aplicar a correção (no seu PC corporativo)

1. Baixe **libs_local.zip**
2. Descompacte na MESMA pasta do seu `sales_dashboard_v10.py`
   → vai criar a pasta `libs_local/` com 4 arquivos .js
3. Substitua **sales_dashboard_v10.py** pela nova versão
4. Substitua **dashboard_template_v10.html** pela nova versão
5. Rode o Python: `python sales_dashboard_v10.py`
6. No console verá `[LOCAL]` em vez de `Baixando do CDN`
7. Abra o HTML gerado
8. Clique em exportar Excel → vai funcionar ✅

## 💡 Vantagem permanente
Depois dessa correção, NUNCA mais vai depender de CDN. O HTML gerado
funciona 100% offline. Bom pra:
- Mandar por email para outros usuários
- Apresentar em lugares sem internet
- Funcionar mesmo se o firewall corporativo mudar políticas
