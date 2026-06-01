# v10 - Target USD adicionado

## ✨ Suporte a TARGET_USD

### Antes
O dashboard só comparava em BRL e Unidades. Se você selecionasse USD no topo,
aparecia mensagem "Target USD não disponível".

### Agora
USD é métrica de primeira classe: mesma estrutura de BRL e UNID.

## 📝 Mudanças

### 1. Modelo Excel (Targets_Financeiros_modelo.xlsx)
Adicionada coluna **TARGET_USD** (com fundo verde claro pra destacar).
Estrutura final: 7 colunas

| FRANQUIA | PRODUTO | ANO | MES_NUM | TARGET_BRL | TARGET_UNID | TARGET_USD |

### 2. Carregamento do arquivo
- Novo campo `TARGET_USD` lido do arquivo (opcional, default = 0)
- Mensagem de erro atualizada para incluir a nova coluna
- **Retrocompatível**: arquivos antigos sem TARGET_USD continuam funcionando

### 3. Renderização do card
Lógica refatorada com mapa de métricas:
```js
mapCampo = {UNID: 'TARGET_UNID', BRL: 'TARGET_BRL', USD: 'TARGET_USD'}
mapLabel = {UNID: 'Unidades', BRL: 'Reais (BRL)', USD: 'Dólares (USD)'}
```

### 4. Aviso quando coluna vazia (melhorado)
Agora detecta TODAS as métricas preenchidas, não só uma:
- Se UNID vazia mas BRL e USD preenchidos → "✅ Há targets em: Reais (BRL) · Dólares (USD)"
- Cobertura completa dos 3 cenários (UNID/BRL/USD)

## ✅ Validações
- Sintaxe JS OK
- Python rodou end-to-end (HTML 0.60 MB)
- Modelo Excel validado (180 linhas, 7 colunas, 2 abas)
- Teste do cenário "BRL + USD preenchidos, UNID vazio":
  - BRL → dashboard normal ✅
  - UNID → aviso sugerindo BRL e USD ✅
  - USD → dashboard normal ✅

## 🧪 Como testar

### Para usar o novo modelo
1. Use o novo arquivo **Targets_Financeiros_modelo.xlsx** (ou adicione coluna TARGET_USD no seu arquivo atual)
2. Preencha os valores em USD nos meses/produtos que quiser
3. Aponte o PATH_TARGETS_FIN do Python pro arquivo

### Para validar no dashboard
1. Substitua **dashboard_template_v10.html**
2. Rode `python sales_dashboard_v10.py`
3. Abra o card "Targets Financeiros"
4. Clique no toggle **USD** no topo da tela
5. Veja atingimento em USD (Real USD vs Target USD)
6. Tabela "Detalhe por Produto" também respeita USD

## 💡 Flexibilidade
Você pode preencher apenas as métricas que precisar:
- Só BRL → atingimento em Reais
- Só USD → atingimento em Dólares (NOVO)
- Mix de BRL + USD → mude o toggle conforme a apresentação
- Pular UNID se não tem target em unidades
