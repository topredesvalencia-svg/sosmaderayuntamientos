"""SOS Madera · Seguimiento de contacto con ayuntamientos (Streamlit)."""
from __future__ import annotations

import datetime as dt
import io
import urllib.parse
from pathlib import Path

import pandas as pd
import streamlit as st

import textos as T

BASE = Path(__file__).parent
DATA_CSV = BASE / "data" / "municipios.csv"
LOGO = BASE / "assets" / "logo.png"
LOGO_CLARO = BASE / "assets" / "logo_light.png"
ICON = BASE / "assets" / "icon.png"
DOSSIER = BASE / "assets" / "dossier_sosmadera_ayuntamientos.pdf"

COLUMNAS = ["Municipio", "Tipo", "Provincia", "Comarca", "Tanda", "Motivo", "Edificios",
            "Contacto", "Cargo", "Email", "Telefono", "Fecha envio", "Estado",
            "Fecha seguimiento", "Notas"]
ESTADOS = ["Pendiente", "Enviado", "Llamado", "Visita concertada", "Presupuesto enviado",
           "Adjudicado", "Descartado"]
CERRADOS = {"Adjudicado", "Descartado"}
COLOR_ESTADO = {"Pendiente": "#D6BE96", "Enviado": "#B08D5E", "Llamado": "#8B6F47",
                "Visita concertada": "#5C4A31", "Presupuesto enviado": "#4F6D8A",
                "Adjudicado": "#2C3E50", "Descartado": "#B9C0C7"}
FECHAS = ["Fecha envio", "Fecha seguimiento"]
DIAS_SEGUIMIENTO = 8

st.set_page_config(page_title="SOS Madera · Ayuntamientos", page_icon=str(ICON), layout="wide")

# ---------------------------------------------------------------- estilo
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bitter:wght@500;700&family=Source+Sans+3:wght@400;600&display=swap');
:root { --wood:#8B6F47; --dark:#5C4A31; --steel:#2C3E50; --light:#D6BE96; --paper:#F2EFEA; }
html, body, [class*="css"], .stMarkdown, p, li, label { font-family:'Source Sans 3', sans-serif; }
h1, h2, h3, h4 { font-family:'Bitter', serif !important; color:var(--dark) !important; letter-spacing:-0.01em; }
section[data-testid="stSidebar"] { background:var(--dark); }
section[data-testid="stSidebar"] * { color:#F2EFEA !important; }
section[data-testid="stSidebar"] [data-baseweb="radio"] div[aria-checked="true"] { background:var(--light) !important; }
div[data-testid="stMetric"] { background:white; border-left:4px solid var(--wood); padding:12px 16px; border-radius:4px; }
div[data-testid="stMetricValue"] { font-family:'Bitter', serif; color:var(--dark); }
.sm-hero { border-bottom:3px solid var(--wood); padding-bottom:6px; margin-bottom:18px; }
.sm-hero p { color:var(--steel); margin:0; }
.sm-aviso { background:var(--paper); border-left:4px solid var(--light); padding:10px 14px; color:var(--steel); }
.stDownloadButton button, .stButton button[kind="primary"] { background:var(--dark); border-color:var(--dark); color:white; }
</style>
""", unsafe_allow_html=True)



# ---------------------------------------------------------------- acceso
def secreto(clave, defecto=None):
    try:
        return st.secrets.get(clave, defecto)
    except Exception:
        return defecto


def acceso() -> bool:
    clave = secreto("app_password")
    if not clave or st.session_state.get("ok"):
        return True
    st.image(str(LOGO), width=360)
    pwd = st.text_input("Contraseña", type="password")
    if st.button("Entrar", type="primary"):
        if pwd == clave:
            st.session_state.ok = True
            st.rerun()
        st.error("Contraseña incorrecta.")
    return False


if not acceso():
    st.stop()


# ---------------------------------------------------------------- datos
def es_fecha(x) -> bool:
    return isinstance(x, dt.date) and not pd.isna(x)


def usa_sheets() -> bool:
    try:
        return "gcp_service_account" in st.secrets and "sheet_url" in st.secrets
    except Exception:
        return False


@st.cache_resource
def hoja():
    import gspread
    gc = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
    return gc.open_by_url(st.secrets["sheet_url"]).sheet1


def normalizar(df: pd.DataFrame) -> pd.DataFrame:
    for c in COLUMNAS:
        if c not in df.columns:
            df[c] = ""
    df = df[COLUMNAS].copy()
    for c in COLUMNAS:
        if c not in FECHAS and c != "Tanda":
            df[c] = df[c].fillna("").astype(str)
    df["Tanda"] = pd.to_numeric(df["Tanda"], errors="coerce").fillna(1).astype(int)
    for c in FECHAS:
        fechas = pd.to_datetime(df[c], errors="coerce")
        df[c] = pd.Series([f.date() if pd.notna(f) else None for f in fechas], index=df.index, dtype=object)
    df.loc[~df["Estado"].isin(ESTADOS), "Estado"] = "Pendiente"
    return df.reset_index(drop=True)


def cargar() -> pd.DataFrame:
    if usa_sheets():
        filas = hoja().get_all_records()
        if not filas:
            df = normalizar(pd.read_csv(DATA_CSV))
            guardar(df)
            return df
        return normalizar(pd.DataFrame(filas))
    return normalizar(pd.read_csv(DATA_CSV))


def a_texto(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in FECHAS:
        out[c] = out[c].apply(lambda d: d.isoformat() if es_fecha(d) else "")
    return out


def guardar(df: pd.DataFrame):
    out = a_texto(df)
    if usa_sheets():
        ws = hoja()
        ws.clear()
        ws.update([out.columns.tolist()] + out.astype(str).values.tolist())
    else:
        out.to_csv(DATA_CSV, index=False)
    st.session_state.df = df


if "df" not in st.session_state:
    st.session_state.df = cargar()
df: pd.DataFrame = st.session_state.df
hoy = dt.date.today()

# ---------------------------------------------------------------- navegación
with st.sidebar:
    st.image(str(LOGO_CLARO), width="stretch")
    st.write("")
    seccion = st.radio("Sección", ["Panel", "Seguimiento", "Generar carta", "Kit de contacto",
                                   "Dossier", "Datos"], label_visibility="collapsed")
    st.divider()
    st.caption(f"{T.EMPRESA['gerentes']}\n\n{T.EMPRESA['tel']}\n\n{T.EMPRESA['email']}")
    if not usa_sheets():
        st.caption("Modo local: los cambios se pierden al reiniciar la app. "
                   "Conecta Google Sheets (ver README) o descarga una copia en Datos.")


def cabecera(titulo, sub):
    st.markdown(f"<div class='sm-hero'><h1>{titulo}</h1><p>{sub}</p></div>", unsafe_allow_html=True)


def seguimientos_vencidos(d):
    return d[d["Fecha seguimiento"].apply(lambda x: es_fecha(x) and x <= hoy)
             & ~d["Estado"].isin(CERRADOS)]


# ================================================================ PANEL
if seccion == "Panel":
    cabecera("Contacto con ayuntamientos", "Estado de la campaña de presentación de SOS Madera.")
    contactados = df[df["Estado"] != "Pendiente"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Entidades en la lista", len(df))
    c2.metric("Contactadas", f"{len(contactados)} · {len(contactados) / max(len(df), 1):.0%}")
    c3.metric("Visitas concertadas", int(df["Estado"].isin(["Visita concertada", "Presupuesto enviado", "Adjudicado"]).sum()))
    c4.metric("Adjudicadas", int((df["Estado"] == "Adjudicado").sum()))

    venc = seguimientos_vencidos(df)
    st.subheader(f"Llamadas pendientes hoy ({len(venc)})")
    if venc.empty:
        st.markdown("<div class='sm-aviso'>No hay seguimientos vencidos. Registra envíos en "
                    "<b>Seguimiento</b> y la llamada se programa sola.</div>", unsafe_allow_html=True)
    else:
        st.dataframe(venc[["Municipio", "Contacto", "Telefono", "Email", "Estado", "Fecha envio",
                           "Fecha seguimiento", "Notas"]].sort_values("Fecha seguimiento"),
                     hide_index=True, width="stretch",
                     column_config={"Fecha envio": st.column_config.DateColumn("Envío", format="DD/MM/YYYY"),
                                    "Fecha seguimiento": st.column_config.DateColumn("Seguimiento", format="DD/MM/YYYY")})

    izq, der = st.columns([3, 2])
    with izq:
        st.subheader("Avance por tanda")
        tabla = pd.crosstab(df["Tanda"].map(lambda t: f"Tanda {t}"), df["Estado"]).reindex(columns=[e for e in ESTADOS if e in df["Estado"].unique()])
        st.bar_chart(tabla, horizontal=True, height=260, stack=True,
                     color=[COLOR_ESTADO[e] for e in tabla.columns])
    with der:
        st.subheader("Próximos envíos")
        sig = df[(df["Estado"] == "Pendiente")].sort_values(["Tanda", "Tipo"], ascending=[True, False]).head(10)
        faltan = sig["Email"].eq("") & sig["Telefono"].eq("")
        sig = sig.assign(Contacto_listo=~faltan)
        st.dataframe(sig[["Municipio", "Tanda", "Contacto_listo"]], hide_index=True, width="stretch",
                     column_config={"Contacto_listo": st.column_config.CheckboxColumn("Contacto listo")})

# ================================================================ SEGUIMIENTO
elif seccion == "Seguimiento":
    cabecera("Seguimiento", "Edita directamente en la tabla y pulsa «Guardar cambios».")

    with st.container(border=True):
        st.markdown("**Registrar un envío**")
        a, b, c = st.columns([3, 2, 1])
        mun = a.selectbox("Entidad", df["Municipio"].tolist(), key="reg_mun")
        fecha = b.date_input("Fecha de envío", hoy, format="DD/MM/YYYY")
        c.write("")
        if c.button("Registrar", type="primary", width="stretch"):
            i = df.index[df["Municipio"] == mun][0]
            df.at[i, "Fecha envio"] = fecha
            df.at[i, "Fecha seguimiento"] = fecha + dt.timedelta(days=DIAS_SEGUIMIENTO)
            if df.at[i, "Estado"] == "Pendiente":
                df.at[i, "Estado"] = "Enviado"
            guardar(df)
            st.toast(f"Envío registrado: {mun}. Llamada programada para el "
                     f"{(fecha + dt.timedelta(days=DIAS_SEGUIMIENTO)).strftime('%d/%m/%Y')}.")
            st.rerun()

    f1, f2, f3, f4 = st.columns([1, 2, 1, 2])
    tandas = f1.multiselect("Tanda", sorted(df["Tanda"].unique()))
    estados = f2.multiselect("Estado", ESTADOS)
    tipo = f3.selectbox("Tipo", ["Todos", "Ayuntamiento", "Organismo"])
    texto = f4.text_input("Buscar", placeholder="Municipio, comarca, contacto…")

    vista = df.copy()
    if tandas:
        vista = vista[vista["Tanda"].isin(tandas)]
    if estados:
        vista = vista[vista["Estado"].isin(estados)]
    if tipo != "Todos":
        vista = vista[vista["Tipo"] == tipo]
    if texto:
        m = vista.apply(lambda r: texto.lower() in " ".join(map(str, r.values)).lower(), axis=1)
        vista = vista[m]

    editado = st.data_editor(
        vista, hide_index=True, width="stretch", height=520, num_rows="fixed",
        disabled=["Municipio"],
        column_config={
            "Tipo": st.column_config.SelectboxColumn(options=["Ayuntamiento", "Organismo"], width="small"),
            "Tanda": st.column_config.SelectboxColumn(options=[1, 2, 3], width="small"),
            "Estado": st.column_config.SelectboxColumn(options=ESTADOS, required=True),
            "Fecha envio": st.column_config.DateColumn("Envío", format="DD/MM/YYYY"),
            "Fecha seguimiento": st.column_config.DateColumn("Seguimiento", format="DD/MM/YYYY"),
            "Motivo": st.column_config.TextColumn(width="medium"),
            "Edificios": st.column_config.TextColumn(width="medium"),
            "Notas": st.column_config.TextColumn(width="large"),
        },
        column_order=["Municipio", "Tanda", "Estado", "Contacto", "Cargo", "Email", "Telefono",
                      "Fecha envio", "Fecha seguimiento", "Notas", "Edificios", "Motivo",
                      "Comarca", "Provincia", "Tipo"],
        key="editor",
    )
    if st.button("Guardar cambios", type="primary"):
        df.loc[editado.index, editado.columns] = editado
        guardar(df)
        st.toast("Cambios guardados.")
        st.rerun()

    with st.expander("Añadir o quitar una entidad"):
        with st.form("nuevo", clear_on_submit=True):
            a, b, c, d = st.columns(4)
            nombre = a.text_input("Municipio u organismo")
            ntipo = b.selectbox("Tipo", ["Ayuntamiento", "Organismo"])
            prov = c.selectbox("Provincia", ["Valencia", "Castellón", "Alicante"])
            ntanda = d.selectbox("Tanda", [1, 2, 3])
            comarca = a.text_input("Comarca")
            edif = st.text_input("Edificios a revisar")
            motivo = st.text_input("Por qué es prioritario")
            if st.form_submit_button("Añadir", type="primary") and nombre.strip():
                if nombre.strip() in df["Municipio"].values:
                    st.error(f"{nombre} ya está en la lista.")
                else:
                    fila = {c: "" for c in COLUMNAS} | {
                        "Municipio": nombre.strip(), "Tipo": ntipo, "Provincia": prov, "Comarca": comarca,
                        "Tanda": ntanda, "Edificios": edif, "Motivo": motivo, "Estado": "Pendiente",
                        "Fecha envio": None, "Fecha seguimiento": None}
                    guardar(pd.concat([df, pd.DataFrame([fila])], ignore_index=True))
                    st.rerun()
        quitar = st.selectbox("Quitar de la lista", [""] + df["Municipio"].tolist())
        if quitar and st.button(f"Quitar {quitar}"):
            guardar(df[df["Municipio"] != quitar].reset_index(drop=True))
            st.rerun()

# ================================================================ CARTA
elif seccion == "Generar carta":
    cabecera("Generar carta", "Carta de presentación personalizada para cada entidad.")
    izq, der = st.columns([2, 3])
    with izq:
        mun = st.selectbox("Entidad", df["Municipio"].tolist())
        fila = df[df["Municipio"] == mun].iloc[0]
        valenciano_por_defecto = fila["Comarca"] in {"La Costera", "Safor", "Ribera Alta", "Vall d'Albaida",
                                                     "Canal de Navarrés", "Els Ports", "Camp de Túria", "Horta Nord", "Camp de Morvedre"}
        idioma = st.radio("Idioma", ["Castellano", "Valenciano"], horizontal=True,
                          index=1 if valenciano_por_defecto else 0,
                          help="Por defecto en valenciano en comarcas valencianoparlantes.")
        destinatario = st.text_input("A la atención de",
                                     " · ".join(x for x in [fila["Contacto"], fila["Cargo"]] if x)
                                     or T.DESTINATARIO_DEFECTO[idioma])
        saludo = st.text_input("Saludo", f"Estimado/a {fila['Contacto']}" if fila["Contacto"] and idioma == "Castellano"
                               else (f"Benvolgut/da {fila['Contacto']}" if fila["Contacto"] else T.SALUDO_DEFECTO[idioma]))
        edificios = st.text_input("Edificios a mencionar", fila["Edificios"].lower() if fila["Tipo"] == "Ayuntamiento" else "",
                                  help="Escríbelo en el idioma de la carta. Déjalo vacío para no incluir la frase personalizada.")
    personal = T.PERSONALIZACION[idioma].format(edificios=edificios) if edificios.strip() else ""
    nombre_mun = mun if fila["Tipo"] == "Ayuntamiento" else mun
    carta = T.CARTA[idioma].format(destinatario=destinatario, municipio=nombre_mun,
                                   saludo=saludo, personalizacion=personal)
    if fila["Tipo"] == "Organismo":
        carta = carta.replace(f"Ayuntamiento de {mun}", mun).replace(f"Ajuntament de {mun}", mun)
    with der:
        st.markdown(f"**Asunto:** {T.ASUNTO[idioma]}")
        carta = st.text_area("Carta (editable)", carta, height=520)
        a, b = st.columns(2)
        a.download_button("Descargar .txt", carta.encode("utf-8"),
                          file_name=f"carta_sosmadera_{mun.replace(' ', '_')}.txt", width="stretch")
        if fila["Email"]:
            link = f"mailto:{fila['Email']}?subject={urllib.parse.quote(T.ASUNTO[idioma])}&body={urllib.parse.quote(carta)}"
            b.link_button("Abrir en el correo", link, width="stretch")
        else:
            b.button("Abrir en el correo", disabled=True, width="stretch",
                     help="Añade el email de la entidad en Seguimiento.")
        st.caption("Recuerda adjuntar el dossier PDF (sección Dossier).")

# ================================================================ KIT
elif seccion == "Kit de contacto":
    cabecera("Kit de contacto", "Plan de acción: a quién contactar, qué enviar y dónde preguntar.")
    t1, t2, t3, t4, t5 = st.tabs(["A quién", "Qué enviar", "Dónde y cómo", "Calendario", "Documentación"])
    with t1:
        st.markdown(T.QUIEN)
    with t2:
        st.markdown(T.QUE)
        st.markdown(T.CONSEJOS)
    with t3:
        st.markdown(T.DONDE)
        st.markdown("#### Cómo conseguir el contacto de cada ayuntamiento")
        st.markdown(T.COMO_CONTACTO)
    with t4:
        st.dataframe(pd.DataFrame(T.CALENDARIO, columns=["Cuándo", "Acción"]), hide_index=True,
                     width="stretch")
    with t5:
        st.caption("Lista de comprobación antes del primer envío (se guarda solo durante la sesión).")
        hechos = sum(st.checkbox(item, key=f"doc_{i}") for i, item in enumerate(T.DOCUMENTACION))
        st.progress(hechos / len(T.DOCUMENTACION), f"{hechos} de {len(T.DOCUMENTACION)} listos")

# ================================================================ DOSSIER
elif seccion == "Dossier":
    cabecera("Dossier de presentación", "PDF de 4 páginas para adjuntar a cada envío.")
    st.markdown("Portada · Quiénes somos y qué hacemos · Casos reales · Cómo trabajamos con ayuntamientos.")
    st.markdown("<div class='sm-aviso'>Antes de enviarlo, sustituye los recuadros de foto y los datos "
                "entre corchetes de la página de casos por obras reales.</div>", unsafe_allow_html=True)
    st.write("")
    if DOSSIER.exists():
        st.download_button("Descargar dossier PDF", DOSSIER.read_bytes(),
                           file_name="dossier_sosmadera_ayuntamientos.pdf", mime="application/pdf", type="primary")
    nuevo = st.file_uploader("Subir versión final del dossier (PDF)", type="pdf")
    if nuevo is not None:
        DOSSIER.write_bytes(nuevo.getvalue())
        st.success("Dossier actualizado para esta sesión. Súbelo también al repositorio para que sea permanente.")

# ================================================================ DATOS
elif seccion == "Datos":
    cabecera("Datos", "Copia de seguridad e importación de la lista.")
    st.markdown("**Almacenamiento:** " + ("Google Sheets (permanente)." if usa_sheets()
                                          else "archivo local (se pierde al reiniciar la app en Streamlit Cloud)."))
    out = a_texto(df)
    a, b = st.columns(2)
    a.download_button("Descargar CSV", out.to_csv(index=False).encode("utf-8-sig"),
                      file_name=f"ayuntamientos_{hoy.isoformat()}.csv", width="stretch")
    buf = io.BytesIO()
    out.to_excel(buf, index=False, sheet_name="Ayuntamientos")
    b.download_button("Descargar Excel", buf.getvalue(), file_name=f"ayuntamientos_{hoy.isoformat()}.xlsx",
                      width="stretch")
    st.divider()
    sub = st.file_uploader("Importar CSV (sustituye la lista actual)", type="csv")
    if sub is not None and st.button("Sustituir lista", type="primary"):
        guardar(normalizar(pd.read_csv(sub)))
        st.success("Lista importada.")
        st.rerun()
    if st.button("Recargar desde el almacenamiento"):
        st.session_state.pop("df", None)
        st.rerun()
