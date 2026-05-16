"""
Alcon Sales Insights - Gerador de HTML standalone (v5.9)
========================================================
v5.9: - Franquias case+punct insensitive (GLAUCOMA -> Glaucoma)
      - CHAN_DESC substitui UF (UF vazio no sell-out)
      - Sem fuzzy client match (so DePara explicito)
      - Dummy injection clientes SO
      - CDN embedding + Google Fonts -> Segoe UI
      - Filtro canal farmacia MANTIDO
"""

from pathlib import Path
import pandas as pd
import json
import re
from datetime import datetime
import urllib.request
import ssl

# =========================================================
# CONFIGURACAO
# =========================================================
PATH_XLSX = r"C:\Users\PEREILU3\OneDrive - Alcon\AdHoc_IC\Projeto\INSIGHTS\f_SELLIN.xlsx"
PATH_TARGETS = r"C:\Users\PEREILU3\OneDrive - Alcon\AdHoc_IC\Projeto\INSIGHTS\Targets.xlsx"
PATH_TARGETS_FIN = r"C:\Users\PEREILU3\OneDrive - Alcon\AdHoc_IC\Projeto\INSIGHTS\Targets_Financeiros.xlsx"
PATH_SELLOUT = r"C:\Users\PEREILU3\OneDrive - Alcon\AdHoc_IC\Projeto\INSIGHTS\f_SELLOUT_GERENCIAL.xlsx"
PATH_DEPARA = r"C:\Users\PEREILU3\OneDrive - Alcon\AdHoc_IC\Projeto\INSIGHTS\DePara_Produtos.xlsx"
PATH_DEPARA_CLIENTES = r"C:\Users\PEREILU3\OneDrive - Alcon\AdHoc_IC\Projeto\INSIGHTS\DePara_Clientes.xlsx"
PATH_OUTPUT = r"dashboard_sales_insightsv10.html"
PATH_TEMPLATE = r"dashboard_template_v10.html"
PATH_NAO_MAPEADOS = r"produtos_nao_mapeados.csv"

EMBUTIR_LIBS = True

# Filtro de canal: "farmacia" = so farmacia | "" = todos os canais
FILTRO_CANAL_PADRAO = "farmacia"

CDN_LIBS = [
    {"name": "Chart.js", "version": "4.4.0",
     "url": "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js",
     "pattern": r'<script\s+src="https://cdn\.jsdelivr\.net/npm/chart\.js@4\.4\.0/dist/chart\.umd\.min\.js"\s*>\s*</script>'},
    {"name": "SheetJS (xlsx)", "version": "0.18.5",
     "url": "https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js",
     "pattern": r'<script\s+src="https://cdn\.jsdelivr\.net/npm/xlsx@0\.18\.5/dist/xlsx\.full\.min\.js"\s*>\s*</script>'},
    {"name": "PptxGenJS", "version": "3.12.0",
     "url": "https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js",
     "pattern": r'<script\s+src="https://cdn\.jsdelivr\.net/npm/pptxgenjs@3\.12\.0/dist/pptxgen\.bundle\.js"\s*>\s*</script>'},
    {"name": "ChartJS DataLabels", "version": "2.2.0",
     "url": "https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js",
     "pattern": r'<script\s+src="https://cdn\.jsdelivr\.net/npm/chartjs-plugin-datalabels@2\.2\.0/dist/chartjs-plugin-datalabels\.min\.js"\s*>\s*</script>'},
]

GOOGLE_FONTS_PATTERNS = [
    r'<link\s+rel="preconnect"\s+href="https://fonts\.googleapis\.com"\s*/?>',
    r'<link\s+rel="preconnect"\s+href="https://fonts\.gstatic\.com"\s+crossorigin\s*/?>',
    r'<link\s+href="https://fonts\.googleapis\.com/css2\?family=Open\+Sans[^"]*"\s+rel="stylesheet"\s*/?>',
]

FONT_FALLBACK_CSS = """<style>
  body, * {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
  }
</style>"""

COLS = {
    "ANO": "ANO", "MES_NUM": "MES_NUM",
    "CLIENTE": "GRUPO_CLIENTE_FINAL", "TIPO_CLIENTE": "TIPO_CLIENTE_FINAL",
    "FRANQUIA": "FRANQUIA", "PRODUTO": "PRODUTO", "FONTE": "FONTE",
    "VALOR_UNID": "Vendas_Unid", "VALOR_BRL": "Vendas_BRL",
    "VALOR_USD": "Vendas_USD", "MOEDA": None,
}

COLS_SELLOUT = {
    "GRUPO_PAINEL": "GRUPO_PAINEL", "FRANQUIA": "FRANQUIA",
    "TIPO_CLIENTE": "TIPO_CLIENTE", "PRODUTO": "PROD_DESC",
    "MEDIDA": "MEDIDA", "CHAN_DESC": "CHAN_DESC",
    "UF": "CHAN_DESC",  # <<< v5.9: CHAN_DESC substitui UF (UF vazio no sell-out)
}
MEDIDA_REAIS = "Reais_PPP"
MEDIDA_UNID = "Unidades"


# =========================================================
# HELPERS
# =========================================================

def _norm_franq(s):
    """Normaliza franquia: upper, remove pontuacao, unifica espacos.
    'POS. OP & PATANOL S' e 'Pos-Op. & Patanol S' -> 'POS OP & PATANOL S'
    """
    if pd.isna(s):
        return ""
    t = str(s).strip().upper()
    t = re.sub(r'[.\-_,;:!?/\\()]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


# =========================================================
# EMBEDDING
# =========================================================

def baixar_lib(url, name):
    print(f"  Baixando {name}...")
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            content = resp.read().decode("utf-8")
            print(f"     OK {name}: {len(content):,} bytes")
            return content
    except Exception as e:
        print(f"     ERRO {name}: {e}")
        return None


def embutir_libs_externas(html_content):
    print("\n" + "=" * 60)
    print("  EMBEDDING DE BIBLIOTECAS EXTERNAS")
    print("=" * 60)
    html = html_content
    ok = 0
    erros = 0
    for lib in CDN_LIBS:
        js = baixar_lib(lib["url"], lib["name"])
        if js:
            tag = '<script>\n/* ' + lib["name"] + ' v' + lib["version"] + ' */\n' + js + '\n</script>'
            m = re.search(lib["pattern"], html, flags=re.IGNORECASE)
            if m:
                html = html.replace(m.group(0), tag)
                ok += 1
            else:
                html = html.replace("</head>", tag + "\n</head>", 1)
                ok += 1
        else:
            erros += 1
    for pat in GOOGLE_FONTS_PATTERNS:
        m = re.search(pat, html, flags=re.IGNORECASE)
        while m:
            html = html.replace(m.group(0), "")
            m = re.search(pat, html, flags=re.IGNORECASE)
    html = html.replace("</head>", FONT_FALLBACK_CSS + "\n</head>", 1)
    cdn = len(re.findall(r'cdn\.jsdelivr\.net', html))
    gf = len(re.findall(r'fonts\.googleapis\.com', html))
    print(f"  CDN: {cdn} {'OK' if cdn==0 else 'VERIFICAR'} | Google: {gf} {'OK' if gf==0 else 'VERIFICAR'}")
    print("=" * 60)
    return html, ok, erros


# =========================================================
# DEPARA
# =========================================================

def ler_depara(path):
    if not Path(path).exists():
        return {}, set()
    print(f"[OK] DePara Produtos: {path}")
    df = pd.read_excel(path)
    for c in ["PRODUTO_SELLIN", "PRODUTO_SELLOUT"]:
        if c not in df.columns:
            return {}, set()
    if "INCLUIR_DASHBOARD" not in df.columns:
        df["INCLUIR_DASHBOARD"] = "SIM"
    def norm(s):
        if pd.isna(s): return ""
        return str(s).strip().upper()
    mapa = {}
    ignorar = set()
    for _, row in df.iterrows():
        si = norm(row["PRODUTO_SELLIN"])
        so = norm(row["PRODUTO_SELLOUT"])
        incl = norm(row.get("INCLUIR_DASHBOARD", "SIM"))
        if not so: continue
        if incl == "NAO":
            ignorar.add(so); continue
        if so not in mapa:
            mapa[so] = si if si else so
    print(f"     Pares: {len(mapa)} | Ignorar: {len(ignorar)}")
    return mapa, ignorar


def ler_depara_clientes(path):
    if not Path(path).exists():
        print("[INFO] DePara Clientes nao encontrado")
        return {}
    print(f"[OK] DePara Clientes: {path}")
    df = pd.read_excel(path)
    if "CLIENTE_SELLOUT" not in df.columns or "CLIENTE_SELLIN_SUGESTAO" not in df.columns:
        return {}
    def norm(s):
        if pd.isna(s): return ""
        return str(s).strip().upper()
    m = {}
    for _, row in df.iterrows():
        so = norm(row["CLIENTE_SELLOUT"])
        si = norm(row["CLIENTE_SELLIN_SUGESTAO"])
        if so and si:
            m[so] = si
    print(f"     Pares: {len(m)}")
    return m


def aplicar_depara_clientes(df_so, map_cli):
    """Aplica APENAS DePara explicito. Sem fuzzy. Sem match mantem nome SO."""
    if df_so is None or len(df_so) == 0:
        return df_so
    def norm(s):
        if pd.isna(s): return ""
        return str(s).strip().upper()
    df_so["CLIENTE_ORIGINAL"] = df_so["GRUPO_PAINEL"]
    df_so["_CN"] = df_so["GRUPO_PAINEL"].apply(norm)
    df_so["GRUPO_PAINEL"] = df_so["_CN"].map(map_cli).fillna(df_so["GRUPO_PAINEL"])
    mapped = df_so["_CN"].isin(map_cli.keys()).sum()
    not_mapped = len(df_so) - mapped
    cli_m = df_so[df_so["_CN"].isin(map_cli.keys())]["_CN"].nunique()
    cli_n = df_so[~df_so["_CN"].isin(map_cli.keys())]["_CN"].nunique()
    print(f"     Clientes mapeados: {cli_m} ({mapped:,} linhas)")
    print(f"     Clientes sem DePara: {cli_n} ({not_mapped:,} linhas) - mantidos com nome SO")
    df_so = df_so.drop(columns=["_CN"])
    return df_so


def aplicar_depara_e_relatorio(df_so, mapeamento, ignorar, path_csv):
    if df_so is None or len(df_so) == 0:
        return df_so
    if not mapeamento and not ignorar:
        df_so["PRODUTO_CANONICO"] = df_so["PRODUTO"]
        return df_so
    def norm(s):
        if pd.isna(s): return ""
        return str(s).strip().upper()
    df_so["_PN"] = df_so["PRODUTO"].apply(norm)
    antes = len(df_so)
    df_so = df_so[~df_so["_PN"].isin(ignorar)].copy()
    depois = len(df_so)
    if antes != depois:
        print(f"     Filtrados (INCLUIR=NAO): {antes - depois:,}")
    df_so["PRODUTO_CANONICO"] = df_so["_PN"].map(mapeamento).fillna(df_so["PRODUTO"])
    nm = ~df_so["_PN"].isin(mapeamento.keys()) & ~df_so["_PN"].isin(ignorar)
    nao = df_so[nm]
    print(f"     Produtos mapeados: {df_so[~nm]['_PN'].nunique()} | Sem DePara: {nao['_PN'].nunique()} (mantidos)")
    if len(nao) > 0:
        agg = nao.groupby("PRODUTO").agg(BRL=("BRL","sum"),UNID=("UNID","sum"),LINHAS=("PRODUTO","size")).reset_index()
        agg = agg.sort_values("UNID", ascending=False)
        agg["PRODUTO_SELLIN_SUGESTAO"] = ""
        agg["INCLUIR_DASHBOARD"] = "SIM"
        agg = agg.rename(columns={"PRODUTO": "PRODUTO_SELLOUT"})
        agg.to_csv(path_csv, index=False, encoding="utf-8-sig")
        print(f"     CSV: {path_csv} ({len(agg)} produtos)")
    df_so = df_so.drop(columns=["_PN"])
    return df_so


# =========================================================
# LEITURA
# =========================================================

def ler_sellout_gerencial(path, franq_norm_map=None):
    """Le sell-out. Aplica DePara Produtos + Clientes. Normaliza franquias."""
    if not Path(path).exists():
        print("[INFO] Sell-out nao encontrado")
        return [], None, []
    if franq_norm_map is None:
        franq_norm_map = {}

    print(f"[OK] Lendo sell-out: {path}")
    df = pd.read_excel(path)
    print(f"     Linhas raw: {len(df)}")

    cols_meses = [c for c in df.columns if re.match(r"^\d{4}_\d{2}_\d{2}$", str(c))]
    print(f"     Colunas mes: {len(cols_meses)}")
    if not cols_meses:
        return [], None, []

    # Verificar colunas obrigatorias
    for k, cn in COLS_SELLOUT.items():
        if cn not in df.columns:
            if k in ("CHAN_DESC", "UF"):
                continue
            print(f"[ERRO] Coluna '{cn}' ausente")
            return [], None, []

    # Listar franquias RAW antes de qualquer filtro
    col_franquia = COLS_SELLOUT["FRANQUIA"]
    col_chan = COLS_SELLOUT["CHAN_DESC"]
    if col_franquia in df.columns:
        fr_raw = sorted(df[col_franquia].dropna().unique())
        print(f"     Franquias RAW (antes filtro): {fr_raw}")

    # Filtro de canal
    if FILTRO_CANAL_PADRAO and col_chan in df.columns:
        a = len(df)
        df = df[df[col_chan].astype(str).str.contains(
            FILTRO_CANAL_PADRAO, case=False, na=False)].copy()
        print(f"     Filtro canal '{FILTRO_CANAL_PADRAO}': {a:,} -> {len(df):,}")
        if col_franquia in df.columns:
            fr_after = sorted(df[col_franquia].dropna().unique())
            print(f"     Franquias APOS filtro canal: {fr_after}")

    # Montar colunas ID
    cols_id = [COLS_SELLOUT["GRUPO_PAINEL"], COLS_SELLOUT["FRANQUIA"],
               COLS_SELLOUT["TIPO_CLIENTE"], COLS_SELLOUT["PRODUTO"], COLS_SELLOUT["MEDIDA"]]
    if col_chan in df.columns:
        cols_id.append(col_chan)
    # CHAN_DESC = UF neste setup, entao nao duplicar
    cols_id = list(dict.fromkeys(cols_id))  # remove duplicatas mantendo ordem
    df = df[cols_id + cols_meses].copy()

    dl = df.melt(id_vars=cols_id, value_vars=cols_meses, var_name="DR", value_name="V")
    dl["V"] = pd.to_numeric(dl["V"], errors="coerce").fillna(0)
    dl = dl[dl["V"] > 0]
    dl["ANO"] = dl["DR"].str[:4].astype(int)
    dl["MES"] = dl["DR"].str[5:7].astype(int)
    dl = dl.drop(columns=["DR"])

    idx = [COLS_SELLOUT["GRUPO_PAINEL"], COLS_SELLOUT["FRANQUIA"],
           COLS_SELLOUT["TIPO_CLIENTE"], COLS_SELLOUT["PRODUTO"]]
    # Adicionar CHAN_DESC como dimensao de segmentacao (substitui UF)
    tc = col_chan in dl.columns
    if tc and col_chan not in idx:
        idx.append(col_chan)
    idx += ["ANO", "MES"]
    idx = list(dict.fromkeys(idx))  # remove duplicatas

    dp = dl.pivot_table(index=idx, columns=COLS_SELLOUT["MEDIDA"],
                        values="V", aggfunc="sum").reset_index()
    dp.columns.name = None
    for co, cn in [(MEDIDA_REAIS, "BRL"), (MEDIDA_UNID, "UNID")]:
        if co in dp.columns: dp = dp.rename(columns={co: cn})
        else: dp[cn] = 0
    dp["BRL"] = dp["BRL"].fillna(0)
    dp["UNID"] = dp["UNID"].fillna(0)

    # Renomear colunas para nomes padrao
    rm = {COLS_SELLOUT["GRUPO_PAINEL"]: "GRUPO_PAINEL",
          COLS_SELLOUT["FRANQUIA"]: "FRANQUIA",
          COLS_SELLOUT["TIPO_CLIENTE"]: "TIPO_CLIENTE",
          COLS_SELLOUT["PRODUTO"]: "PRODUTO"}
    if tc:
        rm[col_chan] = "UF"  # CHAN_DESC vira "UF" para o template
    dp = dp.rename(columns=rm)

    # DE-PARA PRODUTOS
    mapa, ignorar = ler_depara(PATH_DEPARA)
    dp["PRODUTO_ORIGINAL"] = dp["PRODUTO"]
    dp = aplicar_depara_e_relatorio(dp, mapa, ignorar, PATH_NAO_MAPEADOS)
    if dp is None or len(dp) == 0:
        return [], None, []
    dp["PRODUTO"] = dp["PRODUTO_CANONICO"]
    dp = dp.drop(columns=["PRODUTO_CANONICO"])

    # v5.9: NORMALIZAR FRANQUIAS (case + punct insensitive)
    if franq_norm_map:
        antes_fr = sorted(dp["FRANQUIA"].unique())
        def map_franq(x):
            key = _norm_franq(x)
            return franq_norm_map.get(key, x)
        dp["FRANQUIA"] = dp["FRANQUIA"].apply(map_franq)
        depois_fr = sorted(dp["FRANQUIA"].unique())
        print(f"\n     v5.9: Normalizacao de Franquias")
        print(f"     ANTES:  {antes_fr}")
        print(f"     DEPOIS: {depois_fr}")

    # DE-PARA CLIENTES (somente explicito)
    map_cli = ler_depara_clientes(PATH_DEPARA_CLIENTES)
    dp = aplicar_depara_clientes(dp, map_cli)

    # ESTRUTURAS
    gp = ["GRUPO_PAINEL", "FRANQUIA", "TIPO_CLIENTE", "PRODUTO", "ANO", "MES"]
    dprin = dp.groupby(gp, dropna=False).agg(BRL=("BRL","sum"), UNID=("UNID","sum")).reset_index()

    # Estrutura por UF (= CHAN_DESC neste setup)
    tu = "UF" in dp.columns
    duf = None
    if tu:
        duf = dp.groupby(gp[:4]+["UF"]+gp[4:], dropna=False).agg(
            BRL=("BRL","sum"), UNID=("UNID","sum")).reset_index()

    um = dprin.sort_values(["ANO","MES"], ascending=False).iloc[0]
    up = {"ano": int(um["ANO"]), "mes": int(um["MES"])}

    print(f"\n     PRINCIPAL: {len(dprin):,} | BRL: R$ {dprin['BRL'].sum():,.0f}")
    rf = dprin.groupby("FRANQUIA")["BRL"].sum().sort_values(ascending=False)
    print(f"     Sell-out por Franquia:")
    for fr, v in rf.items():
        print(f"       {fr}: R$ {v:,.0f}")

    if tu and duf is not None:
        print(f"     Estrutura UF (CHAN_DESC): {len(duf):,} linhas")
        print(f"     Canais: {sorted(duf['UF'].dropna().unique())}")

    return dprin.to_dict("records"), up, (duf.to_dict("records") if duf is not None else [])


def ler_sellin(path):
    print(f"[OK] Lendo sell-in: {path}")
    df = pd.read_excel(path)
    print(f"     Linhas: {len(df):,}")
    for c in ["ANO", "MES_NUM"]:
        if c not in df.columns:
            raise ValueError(f"Coluna '{c}' ausente")
    for c in ["Vendas_Unid", "Vendas_BRL", "Vendas_USD"]:
        if c not in df.columns: df[c] = 0
    for c, d in [("GRUPO_CLIENTE_FINAL","\u2014"),("TIPO_CLIENTE_FINAL","\u2014"),
                 ("FRANQUIA","\u2014"),("PRODUTO","\u2014"),("FONTE","\u2014")]:
        if c not in df.columns: df[c] = d
    return df


def ler_targets(path):
    if not Path(path).exists(): return {}
    df = pd.read_excel(path)
    if "PRODUTO" not in df.columns or "TARGET_PCT" not in df.columns: return {}
    if "FLAG" in df.columns:
        df = df[df["FLAG"].astype(str).str.upper() == "FOCO"]
    t = {}
    for _, r in df.iterrows():
        t[str(r["PRODUTO"]).strip()] = float(r["TARGET_PCT"])
    print(f"[OK] {len(t)} targets FOCO")
    return t


def ler_targets_fin(path):
    if not Path(path).exists(): return []
    df = pd.read_excel(path)
    if not all(c in df.columns for c in ["FRANQUIA","PRODUTO","ANO","MES_NUM"]): return []
    for c in ["TARGET_BRL","TARGET_UNID"]:
        if c not in df.columns: df[c] = 0
    print(f"[OK] {len(df)} targets financeiros")
    return df.to_dict("records")


# =========================================================
# GERAR HTML
# =========================================================

def gerar_html():
    df = ler_sellin(PATH_XLSX)
    targets = ler_targets(PATH_TARGETS)
    targets_fin = ler_targets_fin(PATH_TARGETS_FIN)

    # v5.9: franq norm map {NORMALIZADO -> case_original_do_sellin}
    franq_norm_map = {}
    for f in df[COLS["FRANQUIA"]].dropna().unique():
        fs = str(f).strip()
        key = _norm_franq(fs)
        franq_norm_map[key] = fs
    franquias_si = sorted(set(franq_norm_map.values()))
    print(f"\n     Franquias sell-in: {franquias_si}")
    print(f"     Mapa normalizado: {franq_norm_map}")

    sellout, ultimo_so, sellout_uf = ler_sellout_gerencial(PATH_SELLOUT, franq_norm_map)

    depara_ok = Path(PATH_DEPARA).exists()

    # v5.7: DUMMY INJECTION
    si_norm = set(str(c).strip().upper() for c in df[COLS["CLIENTE"]].dropna().unique())
    so_info = {}
    for r in sellout:
        gp = str(r.get("GRUPO_PAINEL", "")).strip()
        if gp and gp.upper() not in si_norm:
            if gp not in so_info:
                so_info[gp] = {"tipo": "", "franquias": set(), "produtos": set()}
            so_info[gp]["franquias"].add(r.get("FRANQUIA", "\u2014"))
            so_info[gp]["produtos"].add(r.get("PRODUTO", "\u2014"))
            if r.get("TIPO_CLIENTE"):
                so_info[gp]["tipo"] = r["TIPO_CLIENTE"]

    if so_info:
        ano_ref = int(df["ANO"].max())
        dummy = []
        for cli, info in so_info.items():
            tp = info["tipo"] if info["tipo"] else "SELL-OUT"
            for fr in info["franquias"]:
                for pr in info["produtos"]:
                    dummy.append({
                        "ANO": ano_ref, "MES_NUM": 1,
                        "GRUPO_CLIENTE_FINAL": cli, "TIPO_CLIENTE_FINAL": tp,
                        "FRANQUIA": fr, "PRODUTO": pr, "FONTE": "SELLOUT_REF",
                        "Vendas_Unid": 0, "Vendas_BRL": 0, "Vendas_USD": 0,
                    })
        df = pd.concat([df, pd.DataFrame(dummy)], ignore_index=True)
        print(f"\n  v5.7: {len(so_info)} clientes SO injetados ({len(dummy)} dummy)")

    # cliente -> tipo
    ctm = {}
    for cli, tipo in df.groupby([COLS["CLIENTE"], COLS["TIPO_CLIENTE"]]).groups.keys():
        if cli and tipo:
            ctm[str(cli).strip().upper()] = str(tipo).strip().upper()

    template = Path(PATH_TEMPLATE).read_text(encoding="utf-8")
    ts = datetime.now().strftime("%d/%m/%Y %H:%M")
    dj = json.dumps(df.to_dict("records"), ensure_ascii=False, default=str)
    cj = json.dumps(COLS, ensure_ascii=False)
    tj = json.dumps(targets, ensure_ascii=False)
    tfj = json.dumps(targets_fin, ensure_ascii=False, default=str)
    sj = json.dumps(sellout, ensure_ascii=False, default=str)
    suj = json.dumps(sellout_uf, ensure_ascii=False, default=str) if sellout_uf else "[]"
    usj = json.dumps(ultimo_so, ensure_ascii=False) if ultimo_so else "null"
    ctj = json.dumps(ctm, ensure_ascii=False)

    print(f"\nJSON SI: {len(dj)/1024:.0f} KB | SO: {len(sj)/1024:.0f} KB | UF: {len(suj)/1024:.0f} KB")

    pc = re.compile(r"const\s+COLS\s*=\s*\{[^}]+\};", re.DOTALL)
    t2, nc = pc.subn("const COLS = window.__ALCON_COLS_EMBED__;", template, count=1)
    if nc == 0: raise ValueError("Nao achei 'const COLS = {...}'")
    template = t2

    mk = "const COLS = window.__ALCON_COLS_EMBED__;"
    si = (
        f"window.__ALCON_DATA_EMBED__ = {dj};\n"
        f"window.__ALCON_COLS_EMBED__ = {cj};\n"
        f"window.__ALCON_TARGETS_EMBED__ = {tj};\n"
        f"window.__ALCON_TARGETS_FIN_EMBED__ = {tfj};\n"
        f"window.__ALCON_SELLOUT_EMBED__ = {sj};\n"
        f"window.__ALCON_SELLOUT_UF_EMBED__ = {suj};\n"
        f"window.__ALCON_SELLOUT_ULTIMO__ = {usj};\n"
        f"window.__ALCON_CLIENTE_TIPO_MAP__ = {ctj};\n"
        f"window.__ALCON_DEPARA_OK__ = {str(depara_ok).lower()};\n"
        f'window.__ALCON_META_EMBED__ = {{ registros: {len(df)}, sellout_registros: {len(sellout)}, timestamp: "{ts}" }};\n'
        f"{mk}"
    )
    template = template.replace(mk, si, 1)

    pi = re.compile(r"rawData\s*=\s*gerarDadosExemplo\(\)\s*;", re.DOTALL)
    init_n = (
        "rawData = window.__ALCON_DATA_EMBED__.map(function(r){"
        "return Object.assign({}, r, {"
        "[COLS.ANO]: +r[COLS.ANO],"
        "[COLS.MES_NUM]: +r[COLS.MES_NUM],"
        "[COLS.VALOR_UNID]: +r[COLS.VALOR_UNID] || 0,"
        "[COLS.VALOR_BRL]: +r[COLS.VALOR_BRL] || 0,"
        "[COLS.VALOR_USD]: +r[COLS.VALOR_USD] || 0,"
        "[COLS.TIPO_CLIENTE]: r[COLS.TIPO_CLIENTE] || '-'"
        "});});"
        "if(window.__ALCON_TARGETS_EMBED__){mapTargets = window.__ALCON_TARGETS_EMBED__;}"
        "if(window.__ALCON_TARGETS_FIN_EMBED__){targetsFinanceiros = window.__ALCON_TARGETS_FIN_EMBED__;}"
        "if(window.__ALCON_SELLOUT_EMBED__){rawDataSellout = window.__ALCON_SELLOUT_EMBED__.map(function(r){return Object.assign({},r,{ANO:+r.ANO,MES:+r.MES,BRL:+r.BRL||0,UNID:+r.UNID||0});});}"
        "if(window.__ALCON_SELLOUT_UF_EMBED__){window.__rawDataSelloutUF = window.__ALCON_SELLOUT_UF_EMBED__.map(function(r){return Object.assign({},r,{ANO:+r.ANO,MES:+r.MES,BRL:+r.BRL||0,UNID:+r.UNID||0});});}"
        "if(window.__ALCON_SELLOUT_ULTIMO__){selloutUltimoPeriodo = window.__ALCON_SELLOUT_ULTIMO__;}"
        "if(window.__ALCON_CLIENTE_TIPO_MAP__){window.__clienteTipoMap = window.__ALCON_CLIENTE_TIPO_MAP__;}"
        "if(window.__ALCON_DEPARA_OK__ === false && rawDataSellout && rawDataSellout.length > 0){var b=document.getElementById('deparaBanner');if(b)b.style.display='block';}"
    )
    t3, n2 = pi.subn(init_n, template, count=1)
    if n2 == 0: raise ValueError("Nao achei 'rawData = gerarDadosExemplo()'")
    template = t3

    pf = re.compile(r"function\s+gerarDadosExemplo\s*\(\s*\)\s*\{.*?^\}", re.DOTALL | re.MULTILINE)
    template = pf.sub("// gerarDadosExemplo() removida", template, count=1)

    sm = f"{len(df):,} SI + {len(sellout):,} SO - {ts}"
    template = template.replace('<span id="statusText">Carregando...</span>',
                                f'<span id="statusText">{sm}</span>')

    # EMBUTIR LIBS
    if EMBUTIR_LIBS:
        template, lok, lerr = embutir_libs_externas(template)
    else:
        print("\n[INFO] EMBUTIR_LIBS = False")

    Path(PATH_OUTPUT).write_text(template, encoding="utf-8")
    mb = len(template.encode("utf-8")) / 1024 / 1024
    print(f"\n[OK] Gerado: {PATH_OUTPUT} ({mb:.2f} MB)")
    print(f"\n{'='*60}")
    print(f"  DASHBOARD v5.9 GERADO!")
    print(f"{'='*60}")
    print(f"  Arquivo:    {PATH_OUTPUT}")
    print(f"  Tamanho:    {mb:.2f} MB")
    print(f"  Franquias:  {franquias_si}")
    print(f"  UF/Canal:   CHAN_DESC (substitui UF vazio)")
    print(f"  Filtro:     farmacia mantido")
    print(f"{'='*60}")


if __name__ == "__main__":
    gerar_html()
