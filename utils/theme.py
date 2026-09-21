import streamlit as st

GLOBAL_CSS = """
<style>
    .stApp { background-color: #0a1628; }
    [data-testid="stSidebar"] { background-color: #0d1f3c; }
    [data-testid="stSidebar"] .stRadio > div { gap: 2px; }
    [data-testid="stSidebar"] .stRadio > div > label {
        background: #132744; border-radius: 8px; padding: 8px 12px; margin: 2px 0;
        border: 1px solid transparent; transition: all 0.2s; font-size: 0.85em;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover { border-color: #2ecc71; background: #1a3a5c; }
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] { border-color: #2ecc71; background: #1a3a5c; }
    h1, h2, h3, h4 { color: #e8f4f8 !important; }
    h5, h6 { color: #b8d4e3 !important; }
    .stMarkdown p, .stMarkdown li, .stMarkdown span { color: #c8dce8; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #132744 0%, #1a3a5c 100%);
        border: 1px solid #1e4a6e; border-radius: 12px; padding: 16px;
    }
    [data-testid="stMetricValue"] { color: #2ecc71 !important; font-size: 1.4rem !important; }
    [data-testid="stMetricLabel"] { color: #8bb8d4 !important; }
    [data-testid="stMetricDelta"] { color: #f39c12 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #132744; border-radius: 8px 8px 0 0; color: #8bb8d4;
        border: 1px solid #1e4a6e; border-bottom: none; padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] { background: #1a3a5c !important; color: #2ecc71 !important; border-color: #2ecc71 !important; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2ecc71, #27ae60); color: white;
        border: none; border-radius: 8px; font-weight: bold;
    }
    hr { border-color: #1e4a6e !important; opacity: 0.5; }
    .kpi-card {
        background: linear-gradient(135deg, #132744 0%, #1a3a5c 100%);
        border: 1px solid #1e4a6e; border-radius: 12px; padding: 20px; text-align: center;
    }
    .kpi-value { font-size: 2rem; font-weight: bold; color: #2ecc71; }
    .kpi-label { font-size: 0.85rem; color: #8bb8d4; margin-top: 4px; }
    .kpi-icon { font-size: 1.5rem; margin-bottom: 8px; }
    .page-banner {
        background: linear-gradient(135deg, #132744, #1a3a5c);
        border: 1px solid #1e4a6e; border-radius: 12px; padding: 20px 30px; margin-bottom: 20px;
    }
    .page-banner h2 { margin: 0; color: #e8f4f8; }
    .page-banner p { margin: 4px 0 0 0; color: #8bb8d4; font-size: 0.9em; }
    .green-card {
        background: linear-gradient(135deg, #0d3b2e, #1a5c4a);
        border: 1px solid #2ecc71; border-radius: 12px; padding: 20px; color: white;
    }
    .red-card {
        background: linear-gradient(135deg, #3b0d0d, #5c1a1a);
        border: 1px solid #e74c3c; border-radius: 12px; padding: 20px; color: white;
    }
    .how-step {
        display: flex; align-items: center; gap: 12px; padding: 12px 0;
        border-bottom: 1px solid #1e4a6e;
    }
    .how-step-num {
        width: 36px; height: 36px; border-radius: 50%;
        background: #2ecc71; color: white; display: flex; align-items: center;
        justify-content: center; font-weight: bold; flex-shrink: 0;
    }
    .how-step-text { color: #e8f4f8; }
    .how-step-desc { color: #8bb8d4; font-size: 0.85em; }
</style>
"""

def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def page_header(title, subtitle=""):
    html = f'<div class="page-banner"><h2>{title}</h2>'
    if subtitle:
        html += f'<p>{subtitle}</p>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def kpi_card(icon, value, label):
    return f"""<div class="kpi-card"><div class="kpi-icon">{icon}</div>
    <div class="kpi-value">{value}</div><div class="kpi-label">{label}</div></div>"""
