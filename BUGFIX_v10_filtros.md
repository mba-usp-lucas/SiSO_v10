# v10 - 2 correções

## 1️⃣ Bug do Resumo × KPI · agora batem 100%

### Causa real
A função `clienteBate` no Resumo usava match por palavra-chave SEMPRE,
mesmo quando havia filtro de cliente ativo. Isso causava divergência
quando alguma linha tinha nome diferente da keyword (ex: "Sta Cruz",
"Santa Cruz Drogarias", etc).

### Correção
A função agora tem 2 modos:
- **Sem filtro de cliente**: usa palavra-chave (consolida grupo econômico) ✓
- **Com filtro de cliente**: usa **match exato dos selecionados** (igual KPI) ✓

Quando você filtra "Santa Cruz" no KPI, o Resumo agora soma EXATAMENTE
os mesmos registros (cliente.toUpperCase() === "SANTA CRUZ"). Outras linhas
do Resumo (Brasil/Raia/DPSP/etc) aparecem zeradas ou só com o que foi
selecionado.

### Aviso atualizado
Não diz mais "pode haver diferença" - agora diz:
> ✅ Filtro ativo · valores alinhados com o KPI

## 2️⃣ libs_local não carregando

### Causa
O Python procurava `libs_local` como caminho RELATIVO. Se você rodava o
script de outra pasta (ex: VSCode aberto na pasta pai), ele não encontrava
a pasta mesmo estando ao lado do `.py`.

### Correção (3 melhorias)

#### a) Caminho absoluto baseado na localização do .py
```python
LIBS_LOCAL_DIR = Path(__file__).parent / "libs_local"
```
Agora sempre acha, independente de onde você rodou.

#### b) Diagnóstico explícito no console
Logo no início, mostra:
- Onde está procurando (caminho completo)
- Se a pasta existe
- Quais arquivos .js tem dentro

Exemplo do que aparece agora:
```
  EMBEDDING DE BIBLIOTECAS EXTERNAS
  Pasta local: C:\Users\PEREILU3\OneDrive\...\libs_local
  Arquivos .js encontrados: 4
    - chart.umd.min.js
    - chartjs-plugin-datalabels.min.js
    - pptxgen.bundle.js
    - xlsx.full.min.js
```

#### c) Aviso CRÍTICO se sobrou tag CDN no HTML
Se por qualquer motivo o embed falhou e ficou `<script src="cdn...">`
no HTML, o console grita:
```
!!! CRITICO: 4 tag(s) <script src=cdn...> ainda no HTML!
!  HTML NAO funcionara em ambientes que bloqueiam CDN.
!  Verifique se libs_local/ tem todos os arquivos .js corretos.
```

Agora você não fica adivinhando: o console diz exatamente o problema
e a solução.

## ✅ Validações
- Sintaxe Python e JS OK
- Cenário COM libs_local: 4 embutidas, 0 CDN, console limpo ✅
- Cenário SEM libs_local: 4 avisos críticos visíveis ✅
- Teste alinhamento KPI × Resumo: bate 100% com filtro ativo ✅

## 🧪 Como testar (no seu PC corporativo)

1. Substitua `sales_dashboard_v10.py`
2. Substitua `dashboard_template_v10.html`
3. Confirme que `libs_local/` está na MESMA pasta do `.py` (não em subpasta)
4. Rode `python sales_dashboard_v10.py`
5. **Olhe o console**: deve aparecer `[LOCAL] SheetJS (xlsx): 639,123 bytes`
   - Se aparecer "AVISO: pasta NAO existe" → caminho errado
   - Se aparecer "[LOCAL] X: arquivo NAO encontrado" → faltam arquivos na pasta
   - Se aparecer "CRITICO: tags <script src=cdn...>" → não embutiu corretamente
6. Abra o HTML → exportar Excel → funciona ✅
7. Selecione um cliente no filtro → KPI e Resumo mostram o mesmo número ✅

## 💡 Se ainda der erro de SheetJS
Mande print do console exatamente como aparece após `EMBEDDING DE BIBLIOTECAS`.
Com esse log eu identifico o problema em 1 minuto.
