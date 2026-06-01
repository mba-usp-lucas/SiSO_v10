# 📦 Pasta `libs_local/` · Solução para erro "SheetJS não carregada"

## 🐛 Problema
Computadores corporativos com firewall bloqueiam CDNs externos (cdn.jsdelivr.net).
Quando o Python tentava baixar as bibliotecas JavaScript (Chart.js, SheetJS, PptxGenJS, etc.)
do CDN para embutir no HTML, falhava silenciosamente.

Resultado: erros do tipo "biblioteca SheetJS não carregada" ao tentar exportar Excel.

## ✅ Solução
Agora o Python procura as libs em uma **pasta local** primeiro, e só usa o CDN se não achar.

## 📁 Como configurar (UMA VEZ SÓ)

### 1. Crie uma pasta `libs_local/` ao lado do seu script Python
```
INSIGHTS/
├── sales_dashboard_v10.py
├── dashboard_template_v10.html
├── libs_local/          ← criar esta pasta
│   ├── xlsx.full.min.js
│   ├── chart.umd.min.js
│   ├── pptxgen.bundle.js
│   └── chartjs-plugin-datalabels.min.js
└── (resto dos arquivos)
```

### 2. Coloque os 4 arquivos `.js` dentro da pasta
Os arquivos estão no ZIP `libs_local.zip` que entreguei.

### 3. Rode o Python normalmente
```bash
python sales_dashboard_v10.py
```

O Python detecta a pasta automaticamente e usa as libs locais.
No console verá:
```
  [LOCAL] Chart.js: 204,948 bytes  (arquivo: libs_local/chart.umd.min.js)
  [LOCAL] SheetJS (xlsx): 639,123 bytes  (arquivo: libs_local/xlsx.full.min.js)
  [LOCAL] PptxGenJS: 477,376 bytes  (arquivo: libs_local/pptxgen.bundle.js)
  [LOCAL] ChartJS DataLabels: 12,937 bytes
  Embutidas: 4  |  Erros: 0
  CDN: 0 OK | Google: 0 OK
```

## 🔄 Como funciona
1. Python lê cada lib da pasta `libs_local/`
2. Embute o JavaScript inteiro dentro do HTML
3. HTML final NÃO precisa de internet pra rodar
4. Excel, PPT, e gráficos funcionam offline

## 💡 Vantagens
- Não depende de CDN (firewall corporativo deixa de ser problema)
- HTML 100% offline
- Funciona em qualquer máquina sem internet
- Carrega mais rápido (sem requisições externas)

## ⚠️ Se aparecer ATENCAO no console
Se o Python imprimir:
```
!!! ATENCAO: 1 biblioteca(s) NAO embutida(s) !!!
!  - SheetJS (xlsx)
```
Significa que tanto a pasta local quanto o CDN falharam.
Verifique se o arquivo `.js` está na pasta `libs_local/` com o nome correto.

## 📌 Versões compatíveis
- xlsx.full.min.js → SheetJS 0.18.5
- chart.umd.min.js → Chart.js 4.4.0
- pptxgen.bundle.js → PptxGenJS 3.12.0
- chartjs-plugin-datalabels.min.js → ChartJS DataLabels 2.2.0
