import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import load_data, COUNTRY_EMISSIONS, ISO_MAP, COUNTRY_NAMES_TR
from utils.calculations import sustainability_score, score_color
from utils.theme import inject_css, page_header, kpi_card

st.set_page_config(page_title="AI Carbon Analyzer", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")
inject_css()

# ═══════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:15px 0;">
    <div style="font-size:2.5em;">🌿</div>
    <h3 style="color:#2ecc71;margin:0;font-size:1.1em;">AI Carbon Analyzer</h3>
    </div>""", unsafe_allow_html=True)
    st.divider()

    page = st.radio("Menü", [
        "Ana Dashboard",
        "Gerçek Dünya Eşdeğerleri",
        "What-If Simülasyonu",
        "Karbon Hesaplayıcı",
        "Model Soy Ağacı",
        "Sıralamalar",
        "Model Pasaportu",
        "Model Karşılaştırma",
        "AI Karbon Evrimi",
        "Görselleştirmeler",
        "XAI Şelale Simülatörü (Tahmini)",
        "Denetim Raporu"
    ], label_visibility="collapsed")

    st.divider()
    st.caption("🟢 Veri güncelleme: 10.08.2025")

# ═══════════════════════════════════════════
# VERİ
# ═══════════════════════════════════════════
df = load_data()

# Hesaplanan alanlar
total_co2 = df["emissions_tCO2e"].sum()
total_energy_mwh = total_co2 * 3.5  # tahmini enerji
total_energy_twh = total_energy_mwh / 1e6
renewable_pct = 42.7  # sabit değer (veri setinde yok)
avg_pue = 1.28  # sabit değer
n_models = len(df)

# Kıtalar
CONTINENT_MAP = {
    "China": "Asya", "Japan": "Asya", "India": "Asya", "South Korea": "Asya",
    "Singapore": "Asya", "Thailand": "Asya", "Vietnam": "Asya", "Indonesia": "Asya",
    "Malaysia": "Asya", "Taiwan": "Asya", "Hong Kong": "Asya", "Pakistan": "Asya",
    "United Arab Emirates": "Asya", "UAE": "Asya", "Qatar": "Asya", "Israel": "Asya",
    "Iran": "Asya", "Kazakhstan": "Asya", "Nepal": "Asya", "Bangladesh": "Asya",
    "Saudi Arabia": "Asya",
    "USA": "Kuzey Amerika", "United States": "Kuzey Amerika", "US": "Kuzey Amerika",
    "Canada": "Kuzey Amerika", "Mexico": "Kuzey Amerika",
    "UK": "Avrupa", "United Kingdom": "Avrupa", "Germany": "Avrupa", "France": "Avrupa",
    "Finland": "Avrupa", "Sweden": "Avrupa", "Norway": "Avrupa", "Italy": "Avrupa",
    "Spain": "Avrupa", "Ireland": "Avrupa", "Denmark": "Avrupa", "Netherlands": "Avrupa",
    "Belgium": "Avrupa", "Switzerland": "Avrupa", "Austria": "Avrupa", "Poland": "Avrupa",
    "Iceland": "Avrupa", "Russia": "Avrupa", "Ukraine": "Avrupa",
    "Turkey": "Avrupa", "Türkiye": "Avrupa", "Portugal": "Avrupa", "Romania": "Avrupa",
    "Croatia": "Avrupa", "Czech Republic": "Avrupa", "Hungary": "Avrupa", "Albania": "Avrupa",
    "Brazil": "Güney Amerika", "Argentina": "Güney Amerika", "Chile": "Güney Amerika",
    "Egypt": "Afrika", "Tunisia": "Afrika", "Algeria": "Afrika", "Morocco": "Afrika",
    "Nigeria": "Afrika", "Kenya": "Afrika", "Ghana": "Afrika", "South Africa": "Afrika",
    "Australia": "Okyanusya", "New Zealand": "Okyanusya", "Antarctica": "Antarktika",
}

# ═══════════════════════════════════════════
# ANA DASHBOARD
# ═══════════════════════════════════════════
if page == "Ana Dashboard":
    st.markdown("""<div style="padding:0 0 10px 0;">
    <h1 style="color:#2ecc71;margin:0;">AI Carbon Analyzer</h1>
    <p style="color:#8bb8d4;margin:5px 0 0 0;font-size:1.05em;">AI Modellerinin Küresel Karbon Ayak İzi</p>
    <p style="color:#c8dce8;margin:4px 0 0 0;font-size:0.9em;">Tüm modellerin eğitim süreçlerinden kaynaklanan tahmini emisyonlar</p></div>""", unsafe_allow_html=True)

    # ÜST KPI SATIRI - 3 büyük
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">🌍</div>
        <div class="kpi-value">{total_co2:,.0f}</div>
        <div class="kpi-label">Toplam CO₂ Emisyonu<br/>ton CO₂e</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-value">{total_energy_twh:,.1f}</div>
        <div class="kpi-label">Tahmini Enerji Tüketimi<br/>TWh (CO₂ × 3.5)</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">♻️</div>
        <div class="kpi-value">{renewable_pct}%</div>
        <div class="kpi-label">Tahmini Yenilenebilir Oran<br/>Senaryo: %42.7</div></div>""", unsafe_allow_html=True)

    # İKİNCİ KPI SATIRI - 2 orta
    k4, k5 = st.columns(2)
    with k4:
        st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">📊</div>
        <div class="kpi-value">{avg_pue}</div>
        <div class="kpi-label">Tahmini PUE<br/>Sabit: 1.28</div></div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">🤖</div>
        <div class="kpi-value">{n_models:,}</div>
        <div class="kpi-label">Toplam Model Sayısı<br/>Model</div></div>""", unsafe_allow_html=True)

    st.caption("Not: Enerji, PUE ve yenilenebilir oran değerleri veri setinden tahmin edilmiştir. Gerçek değerler model ve merkeze göre değişiklik gösterebilir.")

    st.divider()

    # VERİ HAZIRLIĞI
    region_df = df[df["model_region"] != "Unknown"]
    _skip = ["cn", "Vietnam (Vietnamese team)", "International (EleutherAI, likely US-based)",
             "International (decentralized collective, primarily US-based)", "Canada/France",
             "China/USA", "France/USA", "Saudi Arabia/China", "Singapore/China",
             "EU\u2011Ireland", "Germany or international (Flair developed by Zalando Research, based in Germany)",
             "International (BigScience consortium, primarily France)",
             "International (BigScience consortium, primarily France/Europe)",
             "International (BigScience consortium, primarily France/Hugging Face)",
             "International (EleutherAI, global open-source)",
             "International (LAION, Germany-based)",
             "Spain or Latin America (Spanish language model by pysentimiento, a Spanish-speaking research group)",
             "United States or global (Google DeepMind)"]
    region_df = region_df[~region_df["model_region"].isin(_skip)]
    region_df["iso"] = region_df["model_region"].map(ISO_MAP)
    region_df = region_df.dropna(subset=["iso"])
    region_co2 = region_df.groupby("iso")["emissions_tCO2e"].sum().reset_index()
    region_co2.columns = ["iso", "total_co2"]
    region_co2["country"] = region_co2["iso"].map({
        "USA": "ABD", "CHN": "Çin", "GBR": "İngiltere", "DEU": "Almanya",
        "FRA": "Fransa", "JPN": "Japonya", "CAN": "Kanada", "IND": "Hindistan",
        "KOR": "Güney Kore", "NOR": "Norveç", "SWE": "İsveç", "FIN": "Finlandiya",
        "ITA": "İtalya", "ESP": "İspanya", "BRA": "Brezilya", "AUS": "Avustralya",
        "TUR": "Türkiye", "ISR": "İsrail", "NLD": "Hollanda", "CHE": "İsviçre",
        "IRL": "İrlanda", "DNK": "Danimarka", "BEL": "Belçika", "POL": "Polonya",
        "AUT": "Avusturya", "ISL": "İzlanda", "RUS": "Rusya", "UKR": "Ukrayna",
        "ARE": "BAE", "QAT": "Katar", "SGP": "Singapur", "MEX": "Meksika",
        "THA": "Tayland", "VNM": "Vietnam", "IDN": "Endonezya", "MYS": "Malezya",
        "TWN": "Tayvan", "HKG": "Hong Kong", "PAK": "Pakistan", "ARG": "Arjantin",
        "CHL": "Şili", "HRV": "Hırvatistan", "CZE": "Çekya", "EGY": "Mısır",
        "HUN": "Macaristan", "IRN": "İran", "KAZ": "Kazakistan", "NPL": "Nepal",
        "PRT": "Portekiz", "ROU": "Romanya", "SAU": "Suudi Arabistan", "TUN": "Tunus",
        "ALB": "Arnavutluk", "BGD": "Bangladeş",
    })

    region_df["continent"] = region_df["model_region"].map(lambda x: CONTINENT_MAP.get(x, "Diğer"))
    continent_co2 = region_df.groupby("continent")["emissions_tCO2e"].sum().reset_index()
    continent_co2.columns = ["Kıta", "CO₂"]
    total_c = continent_co2["CO₂"].sum()
    continent_co2["Oran"] = (continent_co2["CO₂"] / total_c * 100).round(1)
    continent_co2 = continent_co2.sort_values("CO₂", ascending=False)

    import numpy as np
    region_co2["total_co2_log"] = np.log10(region_co2["total_co2"].clip(lower=0.001))

    # 1. HARİTA (üst)
    st.subheader("🗺️ Harita")
    fig_map = px.choropleth(region_co2, locations="iso", color="total_co2_log", hover_name="country",
                            hover_data={"total_co2": ":,.1f", "total_co2_log": False},
                            color_continuous_scale=[
                                [0.0, "#0d47a1"], [0.1, "#1976d2"], [0.2, "#42a5f5"],
                                [0.3, "#66bb6a"], [0.4, "#aed581"], [0.5, "#ffeb3b"],
                                [0.6, "#ffc107"], [0.7, "#ff9800"], [0.8, "#f44336"],
                                [0.9, "#d32f2f"], [1.0, "#880e4f"],
                            ])
    fig_map.update_layout(
        height=450,
        geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=True, coastlinecolor="#1e4a6e",
                 projection_type="natural earth"),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title=dict(text="ton CO₂e (log)", font=dict(color="#c8dce8")),
            tickfont=dict(color="#c8dce8", size=10),
            tickvals=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4],
            ticktext=["1", "3", "10", "30", "100", "300", "1k", "3k", "10k"],
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.divider()

    # 2. TABLO (orta)
    st.subheader("📊 En yüksek emisyonlu 5 ülke tablosu")
    top_countries = region_co2.nlargest(5, "total_co2").reset_index(drop=True)

    for i, (_, r) in enumerate(top_countries.iterrows()):
        sira = i + 1
        tr_name = r["country"]
        pct = r["total_co2"] / region_co2["total_co2"].sum() * 100
        bar_width = min(pct * 2, 100)
        st.markdown(f"""<div style="padding:8px 0;border-bottom:1px solid #1e4a6e;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="color:#e8f4f8;font-weight:bold;font-size:1.05em;">{sira}. {tr_name}</span>
        <span style="color:#e74c3c;font-weight:bold;font-size:1.1em;">{r['total_co2']:,.0f} tCO₂e</span></div>
        <div style="background:#132744;border-radius:4px;height:16px;overflow:hidden;margin-top:6px;">
        <div style="width:{bar_width}%;height:100%;background:linear-gradient(90deg,#ff9800,#e53935);border-radius:4px;"></div></div></div>""", unsafe_allow_html=True)

    st.divider()

    # 3. PİE CHART (alt)
    st.subheader("🥧 Kıta dağılımı")
    fig_pie = px.pie(continent_co2, names="Kıta", values="CO₂",
                     color_discrete_sequence=["#e53935", "#ff9800", "#2ecc71", "#3498db", "#9b59b6", "#f39c12", "#1abc9c"])
    fig_pie.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8dce8", size=12),
                          legend=dict(font=dict(color="#c8dce8", size=11), orientation="v", x=1.02))
    fig_pie.update_traces(textinfo="label+percent", textfont=dict(color="white", size=12))
    st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # 4. GERÇEK DÜNYA EŞDEĞERLERİ
    st.subheader("🌍 Gerçek Dünya Eşdeğerleri")
    st.caption("Tüm modellerin toplam karbon ayak izi somut karşılıklarla:")

    co2 = total_co2
    ank_ist = co2 / 0.042
    araba_km = co2 / 0.000121
    trees = co2 / 0.022
    home_months = co2 / (4.5 / 12)
    steak_kg = co2 / 0.027
    shower_days = co2 / (0.000056 * 60)

    eq_cards = [
        ("✈️", f"{ank_ist:,.0f}", "Ankara→Istanbul\nuçuşu (tek yön)", "#3498db"),
        ("🚗", f"{araba_km:,.0f}", "km benzinli\naraç sürüşü", "#e74c3c"),
        ("🌳", f"{trees:,.0f}", "ağacın 1 yıllık\nkarbon emilimi", "#2ecc71"),
        ("🏠", f"{home_months:,.0f}", "ay ev elektrik\ntüketimi", "#f39c12"),
        ("🥩", f"{steak_kg:,.0f}", "kg sığır eti\nüretimi", "#9b59b6"),
        ("🚿", f"{shower_days:,.0f}", "gün duş\nsüresi (60dk)", "#1abc9c"),
    ]

    cols = st.columns(6)
    for i, (icon, value, label, color) in enumerate(eq_cards):
        with cols[i]:
            st.markdown(f"""<div style="background:#132744;border:1px solid #1e4a6e;border-radius:12px;
            padding:20px 10px;text-align:center;min-height:160px;">
            <div style="font-size:2em;margin-bottom:8px;">{icon}</div>
            <div style="color:{color};font-size:1.6em;font-weight:bold;margin:5px 0;">{value}</div>
            <div style="color:#8bb8d4;font-size:0.8em;line-height:1.3;">{label}</div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# GERÇEK DÜNYA EŞDEĞERLERİ
# ═══════════════════════════════════════════
elif page == "Gerçek Dünya Eşdeğerleri":
    page_header("Gerçek Dünya Eşdeğerleri", "tCO₂e'yi somut karşılıklara dönüştür")
    from utils.data_loader import COUNTRY_EMISSIONS, get_emission_factor

    col1, col2 = st.columns(2)
    with col1:
        selected_model = st.selectbox("Model seç", sorted(df["model_name"].unique().tolist()), key="eq_model")
    with col2:
        selected_country = st.selectbox("Ülke seç",
                                        sorted(COUNTRY_EMISSIONS.keys()),
                                        index=sorted(COUNTRY_EMISSIONS.keys()).index("France"),
                                        key="eq_country")

    model_row = df[df["model_name"] == selected_model]

    if len(model_row) == 0:
        st.warning("Bu model için veri bulunamadı.")
    else:
        r = model_row.iloc[0]
        current_gpu = r.get("training_gpu_type", "NVIDIA A100")
        real_co2 = float(r["emissions_tCO2e"])
        actual_country = r.get("model_region", "USA")
        ef_actual = get_emission_factor(actual_country)
        ef_target = get_emission_factor(selected_country)
        co2_ton = real_co2 * (ef_target / ef_actual) if ef_actual > 0 else real_co2

        if co2_ton >= 100:
            co2_str = f"{co2_ton:,.0f}"
        elif co2_ton >= 10:
            co2_str = f"{co2_ton:,.1f}"
        elif co2_ton >= 1:
            co2_str = f"{co2_ton:,.2f}"
        elif co2_ton >= 0.01:
            co2_str = f"{co2_ton:,.3f}"
        else:
            co2_str = f"{co2_ton:,.5f}"

        tr_gpu = current_gpu if current_gpu and str(current_gpu) != 'nan' else "Bilinmiyor"

        st.markdown(f"""<div style="text-align:center;background:#132744;border:1px solid #1e4a6e;border-radius:16px;
        padding:30px;margin-bottom:25px;">
        <p style="color:#8bb8d4;margin:0;font-size:0.9em;">{selected_model} — {selected_country}'de eğitilseydi</p>
        <h1 style="color:#e74c3c;margin:8px 0 0 0;font-size:3em;">{co2_str} tCO₂e</h1>
        <p style="color:#c8dce8;margin:5px 0 0 0;">{tr_gpu} ile eğitim</p>
        </div>""", unsafe_allow_html=True)

        ank_ist = co2_ton / 0.042
        araba_km = co2_ton / 0.000121
        agac = co2_ton / 0.022
        ev_ay = co2_ton / (4.5 / 12)
        et_kg = co2_ton / 0.027
        dus = co2_ton / (0.000056 * 60)

        def fmt(v):
            if v < 1:
                return "<1"
            elif v < 100:
                return f"{v:,.1f}"
            else:
                return f"{v:,.0f}"

        eq1, eq2, eq3 = st.columns(3)
        with eq1:
            st.markdown(f"""<div style="background:#132744;border:1px solid #1e4a6e;
            border-radius:12px;padding:25px 15px;text-align:center;">
            <div style="font-size:2.5em;margin-bottom:10px;">✈️</div>
            <div style="color:#3498db;font-size:1.8em;font-weight:bold;">{fmt(ank_ist)} uçuş</div>
            <div style="color:#e8f4f8;font-size:0.9em;margin-top:5px;">Ankara → Istanbul (tek yön)</div>
            </div>""", unsafe_allow_html=True)
        with eq2:
            st.markdown(f"""<div style="background:#132744;border:1px solid #1e4a6e;
            border-radius:12px;padding:25px 15px;text-align:center;">
            <div style="font-size:2.5em;margin-bottom:10px;">🚗</div>
            <div style="color:#e74c3c;font-size:1.8em;font-weight:bold;">{fmt(araba_km)} km</div>
            <div style="color:#e8f4f8;font-size:0.9em;margin-top:5px;">benzinli araç sürüşü</div>
            </div>""", unsafe_allow_html=True)
        with eq3:
            st.markdown(f"""<div style="background:#132744;border:1px solid #1e4a6e;
            border-radius:12px;padding:25px 15px;text-align:center;">
            <div style="font-size:2.5em;margin-bottom:10px;">🌳</div>
            <div style="color:#2ecc71;font-size:1.8em;font-weight:bold;">{fmt(agac)} ağaç</div>
            <div style="color:#e8f4f8;font-size:0.9em;margin-top:5px;">1 yıl boyunca karbon emilimi</div>
            </div>""", unsafe_allow_html=True)

        eq4, eq5, eq6 = st.columns(3)
        with eq4:
            st.markdown(f"""<div style="background:#132744;border:1px solid #1e4a6e;
            border-radius:12px;padding:25px 15px;text-align:center;">
            <div style="font-size:2.5em;margin-bottom:10px;">🏠</div>
            <div style="color:#f39c12;font-size:1.8em;font-weight:bold;">{fmt(ev_ay)} ay</div>
            <div style="color:#e8f4f8;font-size:0.9em;margin-top:5px;">ortalama ev elektrik tüketimi</div>
            </div>""", unsafe_allow_html=True)
        with eq5:
            st.markdown(f"""<div style="background:#132744;border:1px solid #1e4a6e;
            border-radius:12px;padding:25px 15px;text-align:center;">
            <div style="font-size:2.5em;margin-bottom:10px;">🥩</div>
            <div style="color:#9b59b6;font-size:1.8em;font-weight:bold;">{fmt(et_kg)} kg</div>
            <div style="color:#e8f4f8;font-size:0.9em;margin-top:5px;">sığır eti üretimi</div>
            </div>""", unsafe_allow_html=True)
        with eq6:
            st.markdown(f"""<div style="background:#132744;border:1px solid #1e4a6e;
            border-radius:12px;padding:25px 15px;text-align:center;">
            <div style="font-size:2.5em;margin-bottom:10px;">🚿</div>
            <div style="color:#1abc9c;font-size:1.8em;font-weight:bold;">{fmt(dus)} gün</div>
            <div style="color:#e8f4f8;font-size:0.9em;margin-top:5px;">duş süresi (60 dk/gün)</div>
            </div>""", unsafe_allow_html=True)

        st.divider()

        st.subheader("🌍 Tüm Ülkelere Göre Eşdeğer Karşılaştırması")
        all_c = []
        for c, ef_c in sorted(COUNTRY_EMISSIONS.items(), key=lambda x: x[1]):
            co2_c = real_co2 * (ef_c / ef_actual) if ef_actual > 0 else real_co2
            all_c.append({"Ülke": COUNTRY_NAMES_TR.get(c, c), "CO₂ (tCO₂e)": round(co2_c, 4),
                          "Tip": "Seçili" if c == selected_country else "Diğer"})
        cdf = pd.DataFrame(all_c)
        fig_eq = px.bar(cdf, x="Ülke", y="CO₂ (tCO₂e)", color="Tip",
                        color_discrete_map={"Seçili": "#e74c3c", "Diğer": "#1e4a6e"},
                        text="CO₂ (tCO₂e)")
        fig_eq.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             font=dict(color="#c8dce8"), xaxis=dict(tickangle=45, gridcolor="#1e4a6e"),
                             yaxis=dict(gridcolor="#1e4a6e"), showlegend=True)
        st.plotly_chart(fig_eq, use_container_width=True)

# ═══════════════════════════════════════════
# COĞRAFİ KARŞI-GÖLGE
# ═══════════════════════════════════════════
elif page == "What-If Simülasyonu":
    page_header("What-If Simülasyonu", "Senaryo: Yalnızca elektrik şebekesi emisyon faktörü değişirse ne olurdu?")
    st.caption("Not: Bu simülasyon yalnızca bölgesel emisyon faktörü farkını dikkate alır. Donanım, verimlilik ve PUE sabit kabul edilmiştir.")
    from utils.data_loader import GPU_POWER, COUNTRY_EMISSIONS, DEFAULT_GPU_POWER, DEFAULT_EMISSION_FACTOR, get_emission_factor
    from utils.calculations import calc_co2

    col_model, col_country = st.columns(2)
    with col_model:
        selected_model = st.selectbox("Model seç", sorted(df["model_name"].unique().tolist()), key="wi_model")
    with col_country:
        target_country = st.selectbox("Hedef ülke",
                                      sorted(COUNTRY_EMISSIONS.keys()),
                                      index=sorted(COUNTRY_EMISSIONS.keys()).index("France"),
                                      key="wi_target")

    model_row = df[df["model_name"] == selected_model]

    if len(model_row) > 0:
        r = model_row.iloc[0]
        current_country = r.get("model_region", "USA")
        current_gpu = r.get("training_gpu_type", "NVIDIA A100")
        co2_current = r["emissions_tCO2e"]
        ef_current = get_emission_factor(current_country)
        ef_target = get_emission_factor(target_country)
        gw = GPU_POWER.get(current_gpu, DEFAULT_GPU_POWER)

        co2_new = co2_current * (ef_target / ef_current) if ef_current > 0 else co2_current
        saving = ((co2_current - co2_new) / co2_current * 100) if co2_current > 0 else 0

        if st.button("Tahmin Yap", type="primary", use_container_width=True, key="wi_btn"):

            if saving > 0:
                st.markdown(f"""<div style="text-align:center;padding:30px;background:#0d3b2e;border-radius:16px;
                border:2px solid #2ecc71;margin-bottom:20px;">
                <h1 style="color:#2ecc71;margin:0;font-size:3.5em;">%{saving:.1f}</h1>
                <p style="color:#8bb8d4;margin:5px 0 0 0;font-size:1.1em;">KARBON AZALTIMI</p></div>""", unsafe_allow_html=True)
            elif saving < 0:
                st.markdown(f"""<div style="text-align:center;padding:30px;background:#3b0d0d;border-radius:16px;
                border:2px solid #e74c3c;margin-bottom:20px;">
                <h1 style="color:#e74c3c;margin:0;font-size:3.5em;">%{abs(saving):.1f}</h1>
                <p style="color:#8bb8d4;margin:5px 0 0 0;font-size:1.1em;">KARBON ARTIŞI</p></div>""", unsafe_allow_html=True)
            else:
                st.info("İki ülke arasında fark yok.")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""<div style="background:#3b1a1a;border:1px solid #e74c3c;border-radius:12px;padding:20px;text-align:center;">
                <p style="color:#8bb8d4;margin:0;font-size:0.85em;">MEVCUT</p>
                <h2 style="color:#e74c3c;margin:8px 0;">{co2_current:.2f} tCO₂e</h2>
                <p style="color:#c8dce8;">{COUNTRY_NAMES_TR.get(current_country, current_country)}</p>
                <p style="color:#8bb8d4;font-size:0.85em;">{current_gpu}</p></div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div style="background:#0d3b2e;border:1px solid #2ecc71;border-radius:12px;padding:20px;text-align:center;">
                <p style="color:#8bb8d4;margin:0;font-size:0.85em;">TAHMİNİ</p>
                <h2 style="color:#2ecc71;margin:8px 0;">{co2_new:.2f} tCO₂e</h2>
                <p style="color:#c8dce8;">{COUNTRY_NAMES_TR.get(target_country, target_country)}</p>
                <p style="color:#8bb8d4;font-size:0.85em;">{current_gpu}</p></div>""", unsafe_allow_html=True)

            st.divider()
            st.subheader("Tüm Ülkelere Göre")
            all_c = []
            for c, ef in sorted(COUNTRY_EMISSIONS.items(), key=lambda x: x[1]):
                co2_c = co2_current * (ef / ef_current) if ef_current > 0 else co2_current
                all_c.append({"Ülke": COUNTRY_NAMES_TR.get(c, c), "CO₂": round(co2_c, 2),
                              "Tip": "Mevcut" if c == current_country else ("Hedef" if c == target_country else "Diğer")})
            cdf = pd.DataFrame(all_c)
            fig_bar = px.bar(cdf, x="Ülke", y="CO₂", color="Tip",
                             color_discrete_map={"Mevcut": "#e74c3c", "Hedef": "#2ecc71", "Diğer": "#1e4a6e"},
                             text="CO₂")
            fig_bar.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(color="#c8dce8"), xaxis=dict(tickangle=45), showlegend=True)
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Model bulunamadı.")

# ═══════════════════════════════════════════
# KARBON HESAPLAYICI
# ═══════════════════════════════════════════
elif page == "Karbon Hesaplayıcı":
    page_header("Karbon Hesaplayıcı", "Model parametrelerini girin, karbon analizini görün")
    from utils.data_loader import GPU_POWER, get_emission_factor
    from utils.calculations import calc_co2, calc_energy_cost, sustainability_score as calc_score, score_label
    import plotly.graph_objects as go

    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Model Konfigürasyonu")
        h_gpu = st.selectbox("GPU Tipi", list(GPU_POWER.keys()), key="hgpu")
        h_gpu_count = st.number_input("GPU Sayısı", 1, 256, 8, key="hgc")
        h_hours = st.number_input("Eğitim Süresi (Saat)", 1, 2000, 120, key="hh")
        h_country = st.selectbox("Bölge", sorted(COUNTRY_EMISSIONS.keys()),
                                 index=sorted(COUNTRY_EMISSIONS.keys()).index("France"), key="hreg")
        h_calc = st.button("🔬 Hesapla", type="primary", use_container_width=True, key="hcalc")

    with c2:
        st.subheader("Sonuçlar")
        if h_calc:
            gw = GPU_POWER.get(h_gpu, 350)
            ef = get_emission_factor(h_country)
            energy_kwh, co2_kg, co2_ton = calc_co2(h_gpu_count, gw, h_hours, ef)
            cost_usd = calc_energy_cost(energy_kwh, h_country)
            score = calc_score(co2_kg, energy_kwh, cost_usd)
            sc_c = score_color(score)

            if co2_ton >= 100:
                em_display = f"{co2_ton:,.0f}"
            elif co2_ton >= 10:
                em_display = f"{co2_ton:,.1f}"
            elif co2_ton >= 1:
                em_display = f"{co2_ton:,.2f}"
            elif co2_ton >= 0.1:
                em_display = f"{co2_ton:.3f}"
            elif co2_ton >= 0.01:
                em_display = f"{co2_ton:.4f}"
            else:
                em_display = f"{co2_ton:.5f}"

            st.markdown(f"""<div style="text-align:center;padding:30px;background:linear-gradient(135deg,#132744,#1a3a5c);
            border-radius:16px;border:2px solid {sc_c};">
            <p style="color:#8bb8d4;margin:0;">KARBON EMİSYONU</p>
            <h1 style="color:{sc_c};margin:5px 0;font-size:3.5em;">{em_display}</h1>
            <p style="color:#8bb8d4;">tCO₂e</p></div>""", unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("⚡ Enerji", f"{energy_kwh/1000:.1f} MWh")
            m2.metric("🌍 Yoğunluk", f"{co2_ton/(energy_kwh/1000) if energy_kwh > 0 else 0:.3f}")
            m3.metric("💰 Maliyet", f"${cost_usd:,.0f}")
            m4.metric("🌱 Skor", f"{score}/100")

            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=score,
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": sc_c},
                       "steps": [{"range": [0, 30], "color": "#e74c3c"}, {"range": [30, 60], "color": "#f39c12"}, {"range": [60, 100], "color": "#2ecc71"}]}))
            fig_g.update_layout(height=220, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10))
            st.plotly_chart(fig_g, use_container_width=True)
        else:
            st.info("Parametreleri girin ve '🔬 Hesapla' butonuna tıklayın.")

# ═══════════════════════════════════════════
# MODEL SOY AĞACI
# ═══════════════════════════════════════════
elif page == "Model Soy Ağacı":
    page_header("Model Soy Ağacı", "Modeller arasındaki ilişki ve karbon evrimi")
    import re

    def parse_family(name):
        n = str(name).lower()
        for fam in ["llama", "qwen", "gemma", "deepseek", "bert", "t5", "roberta", "gpt", "mistral", "phi", "stable", "openmed", "bge", "deberta", "xlm", "wav2vec", "vit", "granite"]:
            if fam in n:
                ver = ""
                m = re.search(r"(?:^|[- _])" + re.escape(fam) + r"[- _]*(\d+(?:\.\d+)?)", n)
                if m:
                    ver = m.group(1)
                size = ""
                ms = re.search(r"(\d+\.?\d*)\s*[bB]", n)
                if ms:
                    size = ms.group(1)
                return fam.capitalize(), ver, size
        return None, None, None

    parsed_rows = []
    for _, row in df.iterrows():
        fam, ver, size = parse_family(row["model_name"])
        if fam and size:
            parsed_rows.append({
                "aile": fam, "surum": ver, "boyut": size,
                "emisyon": row["emissions_tCO2e"] * 1000,
                "model": row["model_name"]
            })

    if not parsed_rows:
        st.info("Ağa verisi bulunamadı.")
    else:
        tree_df = pd.DataFrame(parsed_rows)
        aileler = sorted(tree_df["aile"].unique())
        secilen_aile = st.selectbox("Model ailesi seçin", aileler, key="tree_aile")

        aile_data = tree_df[tree_df["aile"] == secilen_aile]
        surumler = sorted(aile_data["surum"].unique(), key=lambda x: float(x) if x else 0)

        st.markdown(f"""<div style="text-align:center;margin:20px 0 10px;">
        <span style="background:#2ecc71;color:#0a1628;padding:8px 24px;border-radius:8px;font-weight:bold;font-size:1.1em;">{secilen_aile}</span></div>""", unsafe_allow_html=True)

        if len(surumler) > 1:
            cols = st.columns(len(surumler))
            chart_data = {}
            for i, surum in enumerate(surumler):
                with cols[i]:
                    surum_data = aile_data[aile_data["surum"] == surum]
                    boyutlar = sorted(surum_data["boyut"].unique(), key=lambda x: float(x))
                    st.markdown(f"""<div style="text-align:center;margin-bottom:8px;">
                    <span style="background:#1e4a6e;color:#8bb8d4;padding:4px 16px;border-radius:6px;font-weight:bold;">{secilen_aile} {surum}</span></div>""", unsafe_allow_html=True)

                    for boyut in boyutlar:
                        b_data = surum_data[surum_data["boyut"] == boyut]
                        ort_emisyon = b_data["emisyon"].mean()
                        st.markdown(f"""<div style="text-align:center;background:#132744;border:1px solid #1e4a6e;border-radius:8px;padding:8px;margin:4px 0;">
                        <span style="color:#e8f4f8;font-weight:bold;">{secilen_aile} {surum} {boyut}B</span><br>
                        <span style="color:#2ecc71;font-size:1.1em;font-weight:bold;">{ort_emisyon:.1f} kg</span></div>""", unsafe_allow_html=True)
                        chart_data[f"{surum} {boyut}B"] = ort_emisyon
        else:
            surum = surumler[0] if surumler else ""
            boyutlar = sorted(aile_data["boyut"].unique(), key=lambda x: float(x))
            chart_data = {}
            for boyut in boyutlar:
                b_data = aile_data[aile_data["boyut"] == boyut]
                ort_emisyon = b_data["emisyon"].mean()
                st.markdown(f"""<div style="text-align:center;background:#132744;border:1px solid #1e4a6e;border-radius:8px;padding:8px;margin:4px 0;display:inline-block;">
                <span style="color:#e8f4f8;font-weight:bold;">{secilen_aile} {surum} {boyut}B</span><br>
                <span style="color:#2ecc71;font-size:1.1em;font-weight:bold;">{ort_emisyon:.1f} kg</span></div>""", unsafe_allow_html=True)
                chart_data[f"{surum} {boyut}B"] = ort_emisyon

        if chart_data:
            st.markdown("**KARBON EMİSYONU EVRİMİ (kg CO₂e)**")
            chart_df = pd.DataFrame({"Model": list(chart_data.keys()), "Emisyon (kg CO₂e)": list(chart_data.values())})
            fig_line = px.line(chart_df, x="Model", y="Emisyon (kg CO₂e)", markers=True,
                               color_discrete_sequence=["#2ecc71"])
            fig_line.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                                   plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8dce8"),
                                   xaxis=dict(gridcolor="#1e4a6e"), yaxis=dict(gridcolor="#1e4a6e"))
            st.plotly_chart(fig_line, use_container_width=True)

# ═══════════════════════════════════════════
# SIRALAMALAR
# ═══════════════════════════════════════════
elif page == "Sıralamalar":
    page_header("Sıralamalar", "En çevreci ve en kirletici modeller")
    tab_cevreci, tab_kirletici = st.tabs(["En Çevreci", "En Kirletici"])

    df_rank = df[(df["emissions_tCO2e"] > 0) & (df["training_flops"] > 0)].copy()
    df_rank["co2_per_1k_flops"] = (df_rank["emissions_tCO2e"] / df_rank["training_flops"]) * 1000

    with tab_cevreci:
        st.subheader("EN ÇEVRECİ MODELLER (Compute Başına Karbon Verimliliği)")
        green = df_rank.nsmallest(5, "co2_per_1k_flops")
        for i, (_, r) in enumerate(green.iterrows()):
            ulke = r.get("model_region", "")
            st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #1e4a6e;">
            <div style="display:flex;align-items:center;gap:12px;"><span style="color:#8bb8d4;font-weight:bold;width:24px;">{i+1}</span>
            <span style="color:#e8f4f8;font-weight:bold;">{r['model_name']}</span>
            <span style="color:#8bb8d4;font-size:0.85em;">({ulke})</span></div>
            <span style="color:#2ecc71;font-weight:bold;">{r['co2_per_1k_flops']:.2e} tCO₂e/1K FLOPs</span></div>""", unsafe_allow_html=True)

        st.divider()

        st.subheader("EN ÇEVRECİ ÜLKELER (ortalamа CO₂e)")
        ulke_emisyon = df.groupby("model_region")["emissions_tCO2e"].mean().reset_index()
        ulke_emisyon.columns = ["Ülke", "Ort_Emisyon"]
        ulke_emisyon = ulke_emisyon[ulke_emisyon["Ort_Emisyon"] > 0].nsmallest(5, "Ort_Emisyon")
        for i, (_, r) in enumerate(ulke_emisyon.iterrows()):
            st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #1e4a6e;">
            <div style="display:flex;align-items:center;gap:12px;"><span style="color:#8bb8d4;font-weight:bold;width:24px;">{i+1}</span>
            <span style="color:#e8f4f8;font-weight:bold;">{r['Ülke']}</span></div>
            <span style="color:#2ecc71;font-weight:bold;">{r['Ort_Emisyon']:.1f} tCO₂e</span></div>""", unsafe_allow_html=True)

    with tab_kirletici:
        st.subheader("EN KİRLETİCİ MODELLER (Compute Başına Karbon Verimliliği)")
        dirty = df_rank.nlargest(5, "co2_per_1k_flops")
        for i, (_, r) in enumerate(dirty.iterrows()):
            ulke = r.get("model_region", "")
            st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #1e4a6e;">
            <div style="display:flex;align-items:center;gap:12px;"><span style="color:#8bb8d4;font-weight:bold;width:24px;">{i+1}</span>
            <span style="color:#e8f4f8;font-weight:bold;">{r['model_name']}</span>
            <span style="color:#8bb8d4;font-size:0.85em;">({ulke})</span></div>
            <span style="color:#e74c3c;font-weight:bold;">{r['co2_per_1k_flops']:.2e} tCO₂e/1K FLOPs</span></div>""", unsafe_allow_html=True)

        st.divider()

        st.subheader("EN KİRLETİCİ ÜLKELER (ortalamа CO₂e)")
        ulke_dirty = df.groupby("model_region")["emissions_tCO2e"].mean().reset_index()
        ulke_dirty.columns = ["Ülke", "Ort_Emisyon"]
        ulke_dirty = ulke_dirty.nlargest(5, "Ort_Emisyon")
        for i, (_, r) in enumerate(ulke_dirty.iterrows()):
            st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #1e4a6e;">
            <div style="display:flex;align-items:center;gap:12px;"><span style="color:#8bb8d4;font-weight:bold;width:24px;">{i+1}</span>
            <span style="color:#e8f4f8;font-weight:bold;">{r['Ülke']}</span></div>
            <span style="color:#e74c3c;font-weight:bold;">{r['Ort_Emisyon']:.1f} tCO₂e</span></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# MODEL PASAPORTU
# ═══════════════════════════════════════════
elif page == "Model Pasaportu":
    page_header("Model Pasaportu", "Her model için dijital karbon kimlik kartı")

    model_list = sorted(df["model_name"].unique().tolist())
    secilen_model = st.selectbox("Model seçin", model_list, key="pasaport_model")

    model_satir = df[df["model_name"] == secilen_model]
    if len(model_satir) == 0:
        st.warning("Model bulunamadı.")
    else:
        r = model_satir.iloc[0]

        emisyon = r["emissions_tCO2e"]
        bolge = r.get("model_region", "Bilinmiyor")
        donanim = r.get("training_hardware_type", "Bilinmiyor")
        yontem = r.get("method", "Bilinmiyor")

        # Skor hesapla
        from utils.calculations import sustainability_score, score_color, score_label
        enerji = r.get("disclosed_electricity_used_mwh", 0)
        if pd.isna(enerji) or enerji == 0:
            enerji = emisyon * 100
        maliyet = enerji * 1000 * 0.12  # MWh -> kWh, sonra $/kWh ile çarp
        skor = sustainability_score(emisyon * 1000, enerji * 1000, maliyet)
        skor_renk = score_color(skor)
        skor_ad = score_label(skor)

        if emisyon < 1:
            guven = "YÜKSEK"
            guven_renk = "#2ecc71"
        elif emisyon < 10:
            guven = "ORTA"
            guven_renk = "#f39c12"
        else:
            guven = "DÜŞÜK"
            guven_renk = "#e74c3c"

        kart_col1, kart_col2 = st.columns([1, 1])

        with kart_col1:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0d1f3c,#132744);border:2px solid {skor_renk};border-radius:20px;padding:30px;text-align:center;max-width:400px;margin:0 auto;">
                <p style="color:#2ecc71;font-size:0.9em;margin:0;letter-spacing:3px;">AI CARBON PASSPORT</p>
                <div style="margin:20px 0;">
                    <div style="width:60px;height:60px;margin:0 auto;background:#1e4a6e;border-radius:50%;display:flex;align-items:center;justify-content:center;">
                        <span style="font-size:1.8em;">🌱</span>
                    </div>
                </div>
                <h2 style="color:#e8f4f8;margin:5px 0;font-size:1.4em;">{secilen_model.upper()}</h2>
                <p style="color:#8bb8d4;margin:0;font-size:0.85em;">SÜRDÜRÜLEBİLİRLİK</p>
                <h1 style="color:{skor_renk};margin:5px 0;font-size:3em;">{skor}</h1>
                <p style="color:#8bb8d4;margin:0;">/ 100</p>
                <div style="margin-top:20px;">
                    <table style="width:100%;color:#c8dce8;font-size:0.9em;">
                        <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:8px 0;color:#8bb8d4;">Karbon</td><td style="text-align:right;font-weight:bold;color:#2ecc71;">{emisyon:.1f} tCO₂e</td></tr>
                        <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:8px 0;color:#8bb8d4;">Donanım</td><td style="text-align:right;font-weight:bold;">{donanim}</td></tr>
                        <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:8px 0;color:#8bb8d4;">Bölge</td><td style="text-align:right;font-weight:bold;">{bolge}</td></tr>
                        <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:8px 0;color:#8bb8d4;">Yöntem</td><td style="text-align:right;font-weight:bold;">{yontem}</td></tr>
                        <tr><td style="padding:8px 0;color:#8bb8d4;">Güven</td><td style="text-align:right;font-weight:bold;color:{guven_renk};">{guven}</td></tr>
                    </table>
                </div>
                <div style="margin-top:20px;padding:10px;border:2px solid {skor_renk};border-radius:10px;">
                    <p style="color:{skor_renk};margin:0;font-weight:bold;letter-spacing:2px;">{skor_ad.upper()} AI</p>
                </div>
            </div>""", unsafe_allow_html=True)

        with kart_col2:
            st.subheader("Detaylar")
            detaylar = {
                "Model Adı": secilen_model,
                "Emisyon (tCO₂e)": f"{emisyon:.4f}",
                "Bölge": bolge,
                "Donanım Türü": donanim,
                "Eğitim Yöntemi": yontem,
                "Modality": r.get("modality", "Bilinmiyor"),
                "Tür": r.get("type", "Bilinmiyor"),
                "MoE": "Evet" if r.get("is_moe", False) else "Hayır",
                "Parametre": r.get("parameter_values", "Bilinmiyor"),
                "Eğitim Token": f"{r.get('training_token_count', 0):,.0f}" if not pd.isna(r.get("training_token_count", 0)) else "Bilinmiyor",
                "FLOPs": f"{r.get('training_flops', 0):.2e}" if not pd.isna(r.get("training_flops", 0)) else "Bilinmiyor",
                "Emisyon Yoğunluğu": f"{r.get('intensity_tCO2e_per_FLOP', 0):.2e}" if not pd.isna(r.get("intensity_tCO2e_per_FLOP", 0)) else "Bilinmiyor",
            }
            for k, v in detaylar.items():
                st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e4a6e;">
                <span style="color:#8bb8d4;">{k}</span>
                <span style="color:#e8f4f8;font-weight:bold;">{v}</span></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# MODEL KARŞILAŞTIRMA
# ═══════════════════════════════════════════
elif page == "Model Karşılaştırma":
    page_header("Model Karşılaştırma", "Aynı compute seviyesinde neden bazı modeller daha sürdürülebilir?")
    from utils.calculations import sustainability_score, score_color

    modeller = sorted(df["model_name"].unique().tolist())
    c1, c2, c3 = st.columns(3)
    with c1:
        m1 = st.selectbox("Model 1", modeller, index=0, key="karsilastirma_m1")
    with c2:
        m2 = st.selectbox("Model 2", modeller, index=min(5, len(modeller)-1), key="karsilastirma_m2")
    with c3:
        m3 = st.selectbox("Model 3", modeller, index=min(10, len(modeller)-1), key="karsilastirma_m3")

    secilenler = [m1, m2, m3]
    renkler = ["#2ecc71", "#3498db", "#f39c12"]

    kartlar = []
    for idx, model in enumerate(secilenler):
        satir = df[df["model_name"] == model]
        if len(satir) == 0:
            continue
        r = satir.iloc[0]
        emisyon = r["emissions_tCO2e"]
        flops = r.get("training_flops", 0)
        gpu = r.get("training_gpu_type", "Bilinmiyor")
        bolge = r.get("model_region", "Bilinmiyor")
        enerji = r.get("disclosed_electricity_used_mwh", 0)
        if pd.isna(enerji) or enerji == 0:
            enerji = emisyon * 100
        maliyet = enerji * 1000 * 0.12  # MWh -> kWh, sonra $/kWh ile çarp
        skor = sustainability_score(emisyon * 1000, enerji * 1000, maliyet)
        kartlar.append({
            "model": model, "emisyon": emisyon, "flops": flops,
            "gpu": gpu, "bolge": bolge, "skor": skor, "renk": renkler[idx]
        })

    if kartlar:
        st.divider()
        st.subheader("MODEL KARŞILAŞTIRMA")

        cols = st.columns(3)
        for i, kart in enumerate(kartlar):
            with cols[i]:
                st.markdown(f"""
                <div style="background:#132744;border:1px solid #1e4a6e;border-radius:12px;padding:20px;text-align:center;">
                    <p style="color:{kart['renk']};font-weight:bold;font-size:1.1em;margin:0;">{kart['model']}</p>
                    <div style="margin:15px 0;"><div style="width:50px;height:50px;margin:0 auto;background:#1e4a6e;border-radius:50%;display:flex;align-items:center;justify-content:center;">
                        <span style="font-size:1.5em;">🌱</span></div></div>
                    <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e4a6e;">
                        <span style="color:#8bb8d4;">CO₂</span>
                        <span style="color:#2ecc71;font-weight:bold;">{kart['emisyon']:.1f} t</span></div>
                    <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e4a6e;">
                        <span style="color:#8bb8d4;">FLOPs</span>
                        <span style="color:#e8f4f8;font-weight:bold;">{kart['flops']:.2e}</span></div>
                    <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e4a6e;">
                        <span style="color:#8bb8d4;">GPU</span>
                        <span style="color:#e8f4f8;font-weight:bold;">{kart['gpu']}</span></div>
                    <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e4a6e;">
                        <span style="color:#8bb8d4;">Bölge</span>
                        <span style="color:#e8f4f8;font-weight:bold;">{kart['bolge']}</span></div>
                    <div style="display:flex;justify-content:space-between;padding:8px 0;">
                        <span style="color:#8bb8d4;">Skor</span>
                        <span style="color:{kart['renk']};font-weight:bold;font-size:1.2em;">{kart['skor']}</span></div>
                </div>""", unsafe_allow_html=True)

        # Scatter plot
        st.divider()
        st.subheader("Karbon vs Compute")
        scatter_df = df[df["training_flops"] > 0].copy()
        scatter_df["Skor"] = scatter_df.apply(
            lambda r: sustainability_score(r["emissions_tCO2e"] * 1000, r.get("disclosed_electricity_used_mwh", r["emissions_tCO2e"] * 100) * 1000, r.get("disclosed_electricity_used_mwh", r["emissions_tCO2e"] * 100) * 1000 * 0.12), axis=1
        )
        fig_scatter = px.scatter(
            scatter_df, x="training_flops", y="emissions_tCO2e",
            hover_name="model_name", hover_data={"training_gpu_type": True, "model_region": True, "Skor": True, "training_flops": False, "emissions_tCO2e": False},
            color="Skor", color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
            labels={"training_flops": "Training FLOPs", "emissions_tCO2e": "CO₂ (tCO₂e)"}
        )
        max_y = scatter_df["emissions_tCO2e"].quantile(0.95) * 1.2
        fig_scatter.update_layout(
            height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c8dce8"), xaxis=dict(gridcolor="#1e4a6e", type="log"),
            yaxis=dict(gridcolor="#1e4a6e", range=[0, max_y]), coloraxis_colorbar=dict(title="Skor")
        )
        fig_scatter.update_traces(marker=dict(size=6, opacity=0.7, line=dict(width=1, color="#132744")))
        st.plotly_chart(fig_scatter, use_container_width=True)

# ═══════════════════════════════════════════
# AI KARBON ZAMAN ÇİZELGESİ
# ═══════════════════════════════════════════
elif page == "AI Karbon Evrimi":
    page_header("AI Karbon Evrimi", "Model türlerine göre karbon yoğunluğu karşılaştırması")

    # Model türlerine göre trend
    timeline_df = df[["type", "emissions_tCO2e", "training_flops", "training_gpu_type"]].dropna()
    timeline_df = timeline_df[timeline_df["emissions_tCO2e"] > 0]

    # Model türü grupları
    tur_grup = timeline_df.groupby("type").agg(
        ort_emisyon=("emissions_tCO2e", "mean"),
        ort_flops=("training_flops", "mean"),
        sayi=("emissions_tCO2e", "count")
    ).reset_index().sort_values("sayi", ascending=False).head(8)

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Model Türüne Göre Ortalama Emisyon")
        fig_bar = px.bar(tur_grup, x="type", y="ort_emisyon", color="ort_emisyon",
                         color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
                         labels={"type": "Tür", "ort_emisyon": "Ort. Emisyon (tCO₂e)"})
        fig_bar.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#c8dce8"), xaxis=dict(gridcolor="#1e4a6e"), yaxis=dict(gridcolor="#1e4a6e"),
                              showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("Model Sayısı ve Emisyon Dağılımı")
        fig_scatter2 = px.scatter(tur_grup, x="sayi", y="ort_emisyon", size="ort_flops",
                                  hover_name="type", color="ort_emisyon",
                                  color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
                                  labels={"sayi": "Model Sayısı", "ort_emisyon": "Ort. Emisyon (tCO₂e)"})
        fig_scatter2.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font=dict(color="#c8dce8"), xaxis=dict(gridcolor="#1e4a6e"), yaxis=dict(gridcolor="#1e4a6e"))
        st.plotly_chart(fig_scatter2, use_container_width=True)

    st.divider()

    # GPU nesillerine göre trend
    st.subheader("GPU Nesillerine Göre Emisyon Trendi")
    gpu_zaman = timeline_df.copy()
    gpu_map = {
        "NVIDIA V100": 1, "NVIDIA T4": 1,
        "NVIDIA A100 80GB": 2, "NVIDIA A100 40GB": 2, "NVIDIA A100": 2,
        "NVIDIA H100 80GB": 3, "NVIDIA H100": 3,
        "NVIDIA L40S": 3, "NVIDIA RTX 4090": 3
    }
    gpu_zaman["nesil"] = gpu_zaman["training_gpu_type"].map(gpu_map)
    gpu_zaman = gpu_zaman.dropna(subset=["nesil"])

    nesil_emisyon = gpu_zaman.groupby("nesil").agg(
        ort_emisyon=("emissions_tCO2e", "mean"),
        ort_flops=("training_flops", "mean"),
        sayi=("emissions_tCO2e", "count")
    ).reset_index()
    nesil_emisyon["nesil_adi"] = nesil_emisyon["nesil"].map({1: "V100/T4 (1. Nesil)", 2: "A100 (2. Nesil)", 3: "H100/L40S (3. Nesil)"})

    fig_line = px.line(nesil_emisyon, x="nesil_adi", y="ort_emisyon", markers=True,
                       labels={"nesil_adi": "GPU Nesli", "ort_emisyon": "Ort. Emisyon (tCO₂e)"},
                       color_discrete_sequence=["#2ecc71"])
    fig_line.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#c8dce8"), xaxis=dict(gridcolor="#1e4a6e"), yaxis=dict(gridcolor="#1e4a6e"))
    st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    # Emisyon yoğunluğu trendi
    st.subheader("Emisyon Yoğunluğu (tCO₂e / FLOP)")
    yogunluk_df = timeline_df[timeline_df["training_flops"] > 0].copy()
    yogunluk_df["yogunluk"] = yogunluk_df["emissions_tCO2e"] / yogunluk_df["training_flops"]
    yogunluk_tur = yogunluk_df.groupby("type")["yogunluk"].mean().reset_index().sort_values("yogunluk")

    fig_yogun = px.bar(yogunluk_tur, x="type", y="yogunluk", color="yogunluk",
                       color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
                       labels={"type": "Tür", "yogunluk": "tCO₂e / FLOP"})
    fig_yogun.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#c8dce8"), xaxis=dict(gridcolor="#1e4a6e"), yaxis=dict(gridcolor="#1e4a6e"),
                            showlegend=False)
    st.plotly_chart(fig_yogun, use_container_width=True)

# ═══════════════════════════════════════════
# GÖRSELLEŞTİRMELER
# ═══════════════════════════════════════════
elif page == "Görselleştirmeler":
    page_header("Görselleştirmeler", "Proje analizlerinden elde edilen grafikler")

    import os
    img_dir = os.path.join(os.path.dirname(__file__), "img")

    görseller = [
        ("dünya_haritasi.png", "Dünya Haritası", "Model eğitim bölgelerinin coğrafi dağılımı"),
        ("emisyon_bar.png", "Emisyon Bar Grafiği", "Modellere göre toplam karbon emisyonu"),
        ("gpu_barplot.png", "GPU Kullanım Bar Grafiği", "Eğitimde en çok kullanılan GPU modelleri"),
        ("korelasyon.png", "Korelasyon Matrisi", "Sayısal değişkenler arası ilişkiler"),
        ("sayisal_degiskenlerin_dagilimi.png", "Sayısal Değişkenlerin Dağılımı", "Eğitim FLOPs, emisyon ve yoğunluk dağılımları"),
        ("boxplot.png", "Boxplot", "Emisyon değerlerinin istatistiksel dağılımı"),
        ("kategorilere_göre_boxplot.png", "Kategorilere Göre Boxplot", "Model türlerine göre emisyon karşılaştırması"),
        ("scatter.png", "Scatter Plot", "Eğitim FLOPs ile emisyon ilişkisi"),
        ("bildirilen_ve_ana_emisyon_scatter.png", "Bildirilen vs Ana Emisyon", "Açıklanan ve tahmini emisyon karşılaştırması"),
        ("residual_error_analysis.png", "Hata Analizi", "Regresyon modeli artıklarının analizi"),
        ("builtin_permutation.png", "Permutasyon Önem Sıralaması", "Özelliklerin model için önem sırası"),
    ]

    for dosya, baslik, aciklama in görseller:
        yol = os.path.join(img_dir, dosya)
        st.markdown(f"**{baslik}**")
        st.caption(aciklama)
        if os.path.exists(yol):
            st.image(yol, use_column_width=True)
        else:
            st.warning(f"Görsel bulunamadı: {dosya}")
        st.divider()

# ═══════════════════════════════════════════
# XAI ŞELALE SİMÜLATÖRÜ
# ═══════════════════════════════════════════
elif page == "XAI Şelale Simülatörü (Tahmini)":
    page_header("Karbon Simülatörü (Tahmini)", "Model parametrelerinin karbon emisyonuna tahmini etkisini simüle edin")

    from utils.calculations import sustainability_score, score_color

    modeller = sorted(df["model_name"].unique().tolist())
    secilen_model = st.selectbox("Model seçin", modeller, key="xai_model")

    model_satir = df[df["model_name"] == secilen_model]
    if len(model_satir) == 0:
        st.warning("Model bulunamadı.")
    else:
        r = model_satir.iloc[0]

        medyan_emisyon = df["emissions_tCO2e"].median()
        medyan_flops = df["training_flops"].median()

        emisyon = r["emissions_tCO2e"]
        flops = r.get("training_flops", medyan_flops)
        bolge = r.get("model_region", "Unknown")
        gpu = r.get("training_gpu_type", "Unknown")

        bolge_ef_map = {"United States": 1.2, "USA": 1.2, "China": 1.5, "Germany": 0.8, "France": 0.3,
                        "Japan": 1.1, "India": 1.8, "Finland": 0.2, "Canada": 0.4, "South Korea": 0.9}
        bolge_etkisi = bolge_ef_map.get(bolge, 0.5)

        gpu_etki_map = {"NVIDIA V100": 2.5, "NVIDIA T4": 1.8, "NVIDIA A100 80GB": -0.5,
                        "NVIDIA A100": -0.5, "NVIDIA H100 80GB": -2.0, "NVIDIA H100": -2.0}
        gpu_etkisi = gpu_etki_map.get(gpu, 0)

        flops_etkisi = (flops / medyan_flops) * 15 if medyan_flops > 0 else 0

        baslangic = medyan_emisyon
        nihai = baslangic + flops_etkisi + bolge_etkisi + gpu_etkisi

        st.divider()
        st.subheader(f"{secilen_model} - Tahmin Açıklaması")

        categories = ["Başlangıç (Medyan)", "FLOPs Etkisi", f"Bölge Etkisi ({bolge})", f"GPU Etkisi ({gpu})", "Nihai Tahmin"]
        measures = ["absolute", "relative", "relative", "relative", "total"]
        values = [baslangic, flops_etkisi, bolge_etkisi, gpu_etkisi, nihai]
        text_val = [f"{baslangic:.1f} tCO₂e", f"{flops_etkisi:+.1f} tCO₂e", f"{bolge_etkisi:+.1f} tCO₂e",
                    f"{gpu_etkisi:+.1f} tCO₂e", f"{nihai:.1f} tCO₂e"]

        fig_wf = go.Figure(go.Waterfall(
            name="Karbon Tahmini", orientation="v", measure=measures,
            x=categories, y=values, textposition="outside", text=text_val,
            connector={"line": {"color": "#1e4a6e"}},
            increasing={"marker": {"color": "#e74c3c"}},
            decreasing={"marker": {"color": "#2ecc71"}},
            totals={"marker": {"color": "#f39c12"}}
        ))
        fig_wf.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             font=dict(color="#c8dce8"), xaxis=dict(gridcolor="#1e4a6e"), yaxis=dict(gridcolor="#1e4a6e", title="tCO₂e"))
        st.plotly_chart(fig_wf, use_container_width=True)

        st.divider()
        st.subheader("Özellik Etki Sıralaması")
        onemli = [
            ("FLOPs (Hesaplama)", flops_etkisi),
            ("Bölge (Enerji Yoğunluğu)", bolge_etkisi),
            ("GPU (Donanım Verimliliği)", gpu_etkisi),
        ]
        onemli.sort(key=lambda x: abs(x[1]), reverse=True)

        for ozellik, etki in onemli:
            renk = "#e74c3c" if etki > 0 else "#2ecc71"
            yuzde = abs(etki) / (baslangic if baslangic > 0 else 1) * 100
            st.markdown(f"""<div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #1e4a6e;">
            <span style="color:#e8f4f8;font-weight:bold;width:250px;">{ozellik}</span>
            <div style="flex:1;background:#132744;border-radius:4px;height:20px;overflow:hidden;">
            <div style="width:{min(yuzde, 100)}%;height:100%;background:{renk};border-radius:4px;"></div></div>
            <span style="color:{renk};font-weight:bold;width:80px;text-align:right;">{etki:+.1f} tCO₂e</span></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# DENETİM RAPORU
# ═══════════════════════════════════════════
elif page == "Denetim Raporu":
    page_header("Kurumsal Yeşil AI Denetim Raporu", "Seçilen model için resmi ESG/Sürdürülebilirlik raporu oluşturun")
    from utils.calculations import sustainability_score, score_color, score_label, carbon_equivalents

    modeller = sorted(df["model_name"].unique().tolist())
    secilen = st.selectbox("Model seçin", modeller, key="rapor_model")

    model_satir = df[df["model_name"] == secilen]
    if len(model_satir) > 0:
        r = model_satir.iloc[0]
        emisyon = r["emissions_tCO2e"]
        en = r.get("disclosed_electricity_used_mwh", 0)
        if pd.isna(en) or en == 0:
            en = emisyon * 100
        maliyet = en * 1000 * 0.12  # MWh -> kWh, sonra $/kWh ile çarp
        skor = sustainability_score(emisyon * 1000, en * 1000, maliyet)
        skor_renk = score_color(skor)
        skor_ad = score_label(skor)
        flights, car_km, trees, *_ = carbon_equivalents(emisyon * 1000)

        st.divider()
        st.subheader(f"📋 {secilen} - Denetim Raporu Özeti")

        rapor_html = f"""
        <div style="background:#132744;border:2px solid {skor_renk};border-radius:16px;padding:25px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div>
                    <h2 style="color:#e8f4f8;margin:0;">{secilen}</h2>
                    <p style="color:#8bb8d4;margin:5px 0 0 0;">AI Carbon Analyzer Denetim Raporu</p>
                </div>
                <div style="text-align:center;background:{skor_renk};color:#0a1628;padding:10px 20px;border-radius:10px;">
                    <h3 style="margin:0;">{skor}/100</h3>
                    <p style="margin:0;font-size:0.85em;">{skor_ad}</p>
                </div>
            </div>
            <table style="width:100%;color:#c8dce8;font-size:0.9em;border-collapse:collapse;">
                <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:10px;color:#8bb8d4;">Model Adı</td><td style="text-align:right;font-weight:bold;">{secilen}</td></tr>
                <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:10px;color:#8bb8d4;">Karbon Emisyonu</td><td style="text-align:right;font-weight:bold;color:#2ecc71;">{emisyon:.4f} tCO₂e</td></tr>
                <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:10px;color:#8bb8d4;">Enerji Tüketimi</td><td style="text-align:right;font-weight:bold;">{en:.1f} MWh</td></tr>
                <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:10px;color:#8bb8d4;">Donanım</td><td style="text-align:right;font-weight:bold;">{r.get('training_gpu_type', 'Bilinmiyor')}</td></tr>
                <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:10px;color:#8bb8d4;">Bölge</td><td style="text-align:right;font-weight:bold;">{r.get('model_region', 'Bilinmiyor')}</td></tr>
                <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:10px;color:#8bb8d4;">Uçuş Karşılığı</td><td style="text-align:right;font-weight:bold;">{flights:.1f} uçuş</td></tr>
                <tr style="border-bottom:1px solid #1e4a6e;"><td style="padding:10px;color:#8bb8d4;">Araba Km Karşılığı</td><td style="text-align:right;font-weight:bold;">{car_km:,.0f} km</td></tr>
                <tr><td style="padding:10px;color:#8bb8d4;">Ağaç Karşılığı</td><td style="text-align:right;font-weight:bold;">{trees:.0f} ağaç</td></tr>
            </table>
        </div>"""
        st.markdown(rapor_html, unsafe_allow_html=True)

        st.divider()
        st.subheader("İyileştirme Tavsiyeleri")
        tavsiyeler = []
        if emisyon > 100:
            tavsiyeler.append(("Kırmızı", "Yüksek emisyon", "Yenilenebilir enerji kullanılan veri merkezlerine geçiş yapılması önerilir."))
        if emisyon > 10:
            tavsiyeler.append(("Turuncu", "Orta seviye emisyon", "Eğitim süresinin optimize edilmesi veya daha verimli donanım seçilmesi önerilir."))
        if skor < 60:
            tavsiyeler.append(("Turuncu", "Düşük sürdürülebilirlik skoru", "MoE mimarisi veya daha küçük model alternatifleri değerlendirilmelidir."))
        if not tavsiyeler:
            tavsiyeler.append(("Yeşil", "İyi durum", "Model sürdürülebilirlik kriterlerini karşılıyor."))

        for renk_ad, baslik, aciklama in tavsiyeler:
            renk_map = {"Kırmızı": "#e74c3c", "Turuncu": "#f39c12", "Yeşil": "#2ecc71"}
            rnk = renk_map[renk_ad]
            st.markdown(f"""<div style="background:{rnk}11;border:1px solid {rnk};border-radius:10px;padding:12px;margin:8px 0;">
            <span style="color:{rnk};font-weight:bold;">⚠ {baslik}</span>
            <p style="color:#c8dce8;margin:5px 0 0 0;">{aciklama}</p></div>""", unsafe_allow_html=True)

        st.divider()
        st.subheader("📥 Rapor İndirme")
        ind1, ind2 = st.columns(2)

        with ind1:
            csv_rapor = f"Model,Emisyon(tCO2e),Enerji(MWh),Donanim,Bolge,Skor\n{secilen},{emisyon:.4f},{en:.1f},{r.get('training_gpu_type','')},{r.get('model_region','')},{skor}"
            st.download_button("📄 CSV Rapor İndir", csv_rapor.encode("utf-8"), f"{secilen}_denetim_raporu.csv", "text/csv", use_container_width=True)

        with ind2:
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                rapor_df = pd.DataFrame([{
                    "Model": secilen, "Emisyon (tCO₂e)": emisyon, "Enerji (MWh)": en,
                    "Donanım": r.get("training_gpu_type", ""), "Bölge": r.get("model_region", ""),
                    "Skor": skor, "Skor Seviyesi": skor_ad,
                    "Uçuş Karşılığı": f"{flights:.1f}", "Ağaç Karşılığı": f"{trees:.0f}"
                }])
                rapor_df.to_excel(writer, index=False, sheet_name="Denetim Raporu")
            st.download_button("📊 Excel Rapor İndir", buffer.getvalue(), f"{secilen}_denetim_raporu.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

