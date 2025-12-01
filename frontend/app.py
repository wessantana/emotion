import os
from datetime import datetime, timedelta

import requests
import streamlit as st
import pandas as pd

# CONFIGURAÇÃO BÁSICA

st.set_page_config(
    page_title="EduEngage – Sistema de Engajamento",
    page_icon="🧠",
    layout="wide"
)

DEFAULT_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ESTILIZAÇÃO GLOBAL (TEMA EDUENGAGE / EDUVISION)

st.markdown(
    """
    <style>
    :root {
        --edu-primary: #6366f1;    /* Indigo */
        --edu-secondary: #ec4899;  /* Pink */
        --edu-bg: #020617;         /* Slate-950 */
        --edu-surface: #020617;
        --edu-border: #1f2937;
        --edu-text: #e5e7eb;
        --edu-muted: #9ca3af;
    }

    .stApp {
        background: radial-gradient(circle at top left, rgba(99,102,241,0.18), transparent 55%),
                    radial-gradient(circle at bottom right, rgba(236,72,153,0.18), transparent 55%),
                    var(--edu-bg);
        color: var(--edu-text);
        font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* HEADER PRINCIPAL */
    .main-title {
        font-size: 2.2rem;
        font-weight: 750;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: linear-gradient(120deg, var(--edu-primary), var(--edu-secondary));
        -webkit-background-clip: text;
        color: transparent;
    }
    .main-title-icon {
        font-size: 2.4rem;
    }
    .main-subtitle {
        font-size: 0.9rem;
        color: var(--edu-muted);
        margin-bottom: 0.4rem;
    }

    /* CARDS */
    .section-card {
        background: rgba(15,23,42,0.9);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        border: 1px solid rgba(99,102,241,0.35);
        box-shadow: 0 18px 45px rgba(15,23,42,0.9),
                    0 0 0 1px rgba(15,23,42,0.7);
        backdrop-filter: blur(12px);
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--edu-text);
    }

    .section-title span.icon {
        font-size: 1.4rem;
    }

    .section-subtitle {
        font-size: 0.85rem;
        color: var(--edu-muted);
        margin-bottom: 0.6rem;
    }

    /* BOTÃO EDUENGAGE */
    .stButton>button {
        width: 100%;
        border-radius: 999px;
        padding-top: 0.8rem;
        padding-bottom: 0.8rem;
        font-weight: 600;
        border: none;
        background: linear-gradient(135deg, var(--edu-primary), var(--edu-secondary));
        color: #f9fafb;
        box-shadow: 0 12px 30px rgba(15,23,42,0.9);
        letter-spacing: 0.02em;
    }
    .stButton>button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #020617 0%, #020617 50%, #020617 100%);
        border-right: 1px solid #020617;
        box-shadow: 6px 0 20px rgba(15,23,42,0.9);
    }

    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .sidebar-title span.logo {
        width: 26px;
        height: 26px;
        border-radius: 8px;
        background: radial-gradient(circle at 10% 0%, var(--edu-secondary), transparent 55%),
                    radial-gradient(circle at 90% 100%, var(--edu-primary), transparent 60%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .sidebar-subtitle {
        font-size: 0.78rem;
        color: var(--edu-muted);
        margin-bottom: 0.9rem;
    }

    .sidebar-section-title {
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 1.3rem;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: var(--edu-muted);
    }

    /* MÉTRICAS */
    [data-testid="stMetricValue"] {
        color: var(--edu-primary);
    }

    /* INPUTS */
    .stTextInput>div>div>input,
    .stTextArea textarea {
        background-color: #020617 !important;
        border-radius: 10px !important;
        border: 1px solid #111827 !important;
        color: var(--edu-text) !important;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea textarea:focus {
        border-color: rgba(99,102,241,0.7) !important;
        box-shadow: 0 0 0 1px rgba(99,102,241,0.7) !important;
    }

    /* RADIO INLINE */
    .stRadio>div {
        gap: 0.7rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ESTADO GLOBAL

if "backend_url" not in st.session_state:
    st.session_state["backend_url"] = DEFAULT_BACKEND_URL

if "analysis_count" not in st.session_state:
    st.session_state["analysis_count"] = 0


# FUNÇÕES AUXILIARES (SEM MOCK)

def call_analyze_api(image_bytes: bytes, text_input: str, backend_url: str):
    """
    Chama POST /analyze no backend real.
    """
    url = backend_url.rstrip("/") + "/analyze"
    files = {"image": ("image.jpg", image_bytes, "image/jpeg")}
    data = {"text_input": text_input}

    try:
        resp = requests.post(url, files=files, data=data, timeout=60)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao chamar backend em /analyze: {e}")
        return None

    try:
        return resp.json()
    except ValueError:
        st.error("Não foi possível decodificar o JSON retornado pelo backend.")
        return None


def call_history_api(backend_url: str):
    """
    Chama GET /history no backend real.
    """
    url = backend_url.rstrip("/") + "/history"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao chamar backend em /history: {e}")
        return []


def map_engagement_to_score(level: str):
    if not isinstance(level, str):
        return None
    level = level.strip().lower()
    mapping = {"baixo": 0, "médio": 1, "medio": 1, "alto": 2}
    return mapping.get(level)


# SIDEBAR – EDUENGAGE

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title"><span class="logo">🧠</span>'
        '<span>EduEngage</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sidebar-subtitle">Monitoramento inteligente de engajamento em sala de aula.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-section-title">Navegação</div>', unsafe_allow_html=True)
    page = st.radio(
        "",
        ("📸 Página do Aluno", "📈 Dashboard do Professor"),
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-section-title">Configurações</div>', unsafe_allow_html=True)
    backend_url = st.text_input(
        "URL do Backend",
        value=st.session_state["backend_url"],
        help="Ex: http://localhost:8000"
    )
    st.session_state["backend_url"] = backend_url

    st.markdown('<div class="sidebar-section-title">Estatísticas</div>', unsafe_allow_html=True)
    st.metric("Total de Análises", st.session_state["analysis_count"])


# PÁGINA – ALUNO

if page == "📸 Página do Aluno":
    st.markdown(
        '<div class="main-title"><span class="main-title-icon">📷</span>'
        '<span>EduEngage – Análise de Engajamento do Aluno</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="main-subtitle">Combine expressão facial e sentimento do texto para entender como o aluno está se engajando com o conteúdo.</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    col_left, col_right = st.columns(2)

    # Coluna esquerda: imagem 
    with col_left:
        st.markdown(
            """
            <div class="section-card">
              <div class="section-title">
                <span class="icon">📸</span>
                <span>Captura de Imagem</span>
              </div>
              <div class="section-subtitle">
                Escolha a fonte da imagem e envie uma foto do rosto do aluno.
              </div>
            """,
            unsafe_allow_html=True
        )

        image_source = st.radio(
            "Escolha a fonte da imagem:",
            ["Upload de arquivo", "Webcam"],
            horizontal=True,
            label_visibility="visible"
        )

        camera_photo = None
        uploaded_file = None

        if image_source == "Webcam":
            camera_photo = st.camera_input("Webcam")
        else:
            uploaded_file = st.file_uploader(
                "Selecione uma imagem",
                type=["jpg", "jpeg", "png", "webp"],
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # Coluna direita: texto 
    with col_right:
        st.markdown(
            """
            <div class="section-card">
              <div class="section-title">
                <span class="icon">✍️</span>
                <span>Resposta do Aluno</span>
              </div>
              <div class="section-subtitle">
                Digite a resposta ou comentário do aluno sobre o conteúdo.
              </div>
            """,
            unsafe_allow_html=True
        )

        text_input = st.text_area(
            "Digite sua resposta ou comentário:",
            placeholder="Ex: Não entendi muito bem a explicação de hoje...",
            height=210,
            label_visibility="visible"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    analyze_button = st.button("🔎  Analisar Engajamento")

    if analyze_button:
        image_bytes = None
        if image_source == "Webcam" and camera_photo is not None:
            image_bytes = camera_photo.getvalue()
        elif image_source == "Upload de arquivo" and uploaded_file is not None:
            image_bytes = uploaded_file.read()

        if image_bytes is None:
            st.warning("Selecione uma imagem pelo upload ou webcam.")
            st.stop()

        if not text_input.strip():
            st.warning("Digite a resposta ou comentário do aluno.")
        else:
            with st.spinner("Analisando engajamento com EduEngage..."):
                result = call_analyze_api(image_bytes, text_input, backend_url)

            if result is not None:
                st.session_state["analysis_count"] += 1

                facial_emotion = result.get("facial_emotion", "N/D")
                text_sentiment = result.get("text_sentiment", "N/D")
                engagement_level = result.get("engagement_level", "N/D")
                suggestions = result.get("suggestions", "")

                if isinstance(facial_emotion, set):
                    facial_emotion = ", ".join(list(facial_emotion))
                if isinstance(text_sentiment, set):
                    text_sentiment = ", ".join(list(text_sentiment))
                if isinstance(engagement_level, set):
                    engagement_level = ", ".join(list(engagement_level))

                st.success("Análise concluída com sucesso!")

                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Emoção Facial", str(facial_emotion))
                with m2:
                    st.metric("Sentimento do Texto", str(text_sentiment))
                with m3:
                    st.metric("Nível de Engajamento", str(engagement_level))

                st.markdown("### 🎯 Recomendações")
                if suggestions:
                    st.info(suggestions)
                else:
                    st.write("Nenhuma recomendação retornada pelo backend.")

                with st.expander("Ver JSON completo"):
                    st.json(result)


# PÁGINA – PROFESSOR

if page == "📈 Dashboard do Professor":
    st.markdown(
        '<div class="main-title"><span class="main-title-icon">📈</span>'
        '<span>EduEngage – Dashboard do Professor</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="main-subtitle">Acompanhe padrões de engajamento, emoções e sentimentos ao longo do tempo.</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    if st.button("🔄 Atualizar dados"):
        st.experimental_rerun()

    history_data = call_history_api(backend_url)

    if not history_data:
        st.warning("Nenhum dado de histórico encontrado.")
    else:
        df = pd.DataFrame(history_data)

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        else:
            df["timestamp"] = pd.NaT

        if "engagement" not in df.columns and "engagement_level" in df.columns:
            df["engagement"] = df["engagement_level"]
        if "emotion" not in df.columns and "facial_emotion" in df.columns:
            df["emotion"] = df["facial_emotion"]
        if "sentiment" not in df.columns and "text_sentiment" in df.columns:
            df["sentiment"] = df["text_sentiment"]

        df = df.dropna(subset=["timestamp"])
        df["engagement_score"] = df["engagement"].apply(map_engagement_to_score)

        st.markdown("### 📊 Visão Geral")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Registros analisados", len(df))
        with c2:
            last = df.sort_values("timestamp").iloc[-1]
            st.metric(
                "Último engajamento",
                str(last.get("engagement", "N/D")),
                help=f"Registrado em {last['timestamp']}"
            )
        with c3:
            dist = df["engagement"].value_counts()
            if not dist.empty:
                st.metric(
                    "Engajamento mais frequente",
                    f"{dist.index[0]} ({dist.iloc[0]} registros)"
                )
            else:
                st.metric("Engajamento mais frequente", "N/D")

        st.markdown("### 📈 Evolução do Engajamento")
        if df["engagement_score"].notna().any():
            df_plot = df.dropna(subset=["engagement_score"]).sort_values("timestamp")
            st.line_chart(
                data=df_plot.set_index("timestamp")["engagement_score"],
                height=300
            )
            st.caption("Escala: 0 = Baixo, 1 = Médio, 2 = Alto")
        else:
            st.info("Ainda não há dados suficientes para o gráfico.")

        g1, g2 = st.columns(2)
        with g1:
            st.markdown("#### Distribuição de Engajamento")
            st.bar_chart(df["engagement"].value_counts())
        with g2:
            st.markdown("#### Distribuição de Emoções")
            if "emotion" in df.columns:
                st.bar_chart(df["emotion"].value_counts())
            else:
                st.write("Coluna `emotion` não encontrada.")

        st.markdown("### 📋 Registros Detalhados")
        cols_to_show = [c for c in ["timestamp", "engagement", "emotion", "sentiment"] if c in df.columns]
        st.dataframe(df[cols_to_show].sort_values("timestamp", ascending=False))
