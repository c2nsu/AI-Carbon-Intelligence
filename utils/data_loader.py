import streamlit as st
import pandas as pd

@st.cache_data
def load_data(path="HF_models_imputed_realistic_v2.csv"):
    df = pd.read_csv(path)
    df.columns = df.columns.str.replace(".", "_", regex=False)
    def extract_model_name(mid):
        if pd.isna(mid): return str(mid)
        parts = str(mid).split("/")
        return parts[-1] if len(parts) > 1 else parts[0]
    df["model_name"] = df["model_id"].apply(extract_model_name)
    return df

GPU_POWER = {
    "NVIDIA H100 80GB": 350, "NVIDIA H100": 350,
    "NVIDIA A100 80GB": 300, "NVIDIA A100": 300, "NVIDIA A100-SXM4-80GB": 300,
    "NVIDIA V100": 300, "NVIDIA V100-SXM2-32GB": 300,
    "NVIDIA T4": 70, "NVIDIA T4-16GB": 70,
    "NVIDIA L40S": 300, "NVIDIA L40": 300,
    "NVIDIA RTX 4090": 450, "NVIDIA RTX 3090": 350,
    "NVIDIA A800": 300, "NVIDIA A10 40GB": 150,
    "TPU v4": 170, "TPU v5e": 162, "TPU v5p": 450,
}
DEFAULT_GPU_POWER = 250

GPU_FLOPS = {
    "NVIDIA H100 80GB": 990, "NVIDIA H100": 990,
    "NVIDIA A100 80GB": 312, "NVIDIA A100": 312, "NVIDIA A100-SXM4-80GB": 312,
    "NVIDIA V100": 15.7, "NVIDIA V100-SXM2-32GB": 15.7,
    "NVIDIA T4": 8.1, "NVIDIA T4-16GB": 8.1,
    "NVIDIA L40S": 362, "NVIDIA L40": 362,
    "NVIDIA RTX 4090": 165, "NVIDIA RTX 3090": 142,
    "NVIDIA A800": 312, "NVIDIA A10 40GB": 31.2,
    "TPU v4": 275, "TPU v5e": 197, "TPU v5p": 459,
}

COUNTRY_EMISSIONS = {
    "Norway": 0.023, "Sweden": 0.013, "Finland": 0.083, "France": 0.056,
    "Canada": 0.120, "USA": 0.386, "Germany": 0.350, "UK": 0.233,
    "Japan": 0.457, "China": 0.555, "India": 0.708, "Turkey": 0.444,
    "Australia": 0.530, "Italy": 0.300, "Spain": 0.230, "South Korea": 0.415,
    "Ireland": 0.350, "Denmark": 0.130, "Switzerland": 0.012, "Brazil": 0.075,
    "Netherlands": 0.380, "Belgium": 0.155, "Poland": 0.750, "Austria": 0.195,
    "Iceland": 0.003, "Russia": 0.450, "Ukraine": 0.400, "Israel": 0.600,
    "Singapore": 0.400, "Mexico": 0.450, "Thailand": 0.500,
    "Vietnam": 0.550, "Indonesia": 0.600, "Malaysia": 0.550,
    "Taiwan": 0.500, "Hong Kong": 0.550, "Pakistan": 0.550,
    "Saudi Arabia": 0.700, "Qatar": 0.600, "UAE": 0.600,
    "Egypt": 0.500, "Tunisia": 0.500, "Portugal": 0.300,
    "Romania": 0.400, "Croatia": 0.300, "Czech Republic": 0.500,
    "Hungary": 0.350, "Albania": 0.350, "Bangladesh": 0.600,
    "Argentina": 0.400, "Chile": 0.400, "Kazakhstan": 0.600,
    "Nepal": 0.500, "Iran": 0.600,
}
DEFAULT_EMISSION_FACTOR = 0.450

COUNTRY_ALIASES = {
    "United States": "USA", "US": "USA",
    "United Kingdom": "UK",
    "Türkiye": "Turkey",
    "South Korea": "South Korea", "Korea": "South Korea",
    "United Arab Emirates": "UAE",
    "Viet Nam": "Vietnam",
    "Czech Republic": "Czech Republic", "Czechia": "Czech Republic",
}

def get_emission_factor(country):
    if pd.isna(country): return DEFAULT_EMISSION_FACTOR
    c = str(country).strip()
    c = COUNTRY_ALIASES.get(c, c)
    return COUNTRY_EMISSIONS.get(c, DEFAULT_EMISSION_FACTOR)

ISO_MAP = {
    "USA": "USA", "United States": "USA", "US": "USA",
    "China": "CHN", "UK": "GBR", "United Kingdom": "GBR",
    "Germany": "DEU", "France": "FRA", "Japan": "JPN",
    "Canada": "CAN", "India": "IND", "South Korea": "KOR",
    "Norway": "NOR", "Sweden": "SWE", "Finland": "FIN", "Italy": "ITA",
    "Spain": "ESP", "Brazil": "BRA", "Australia": "AUS",
    "Turkey": "TUR", "Türkiye": "TUR",
    "Israel": "ISR", "Netherlands": "NLD", "Switzerland": "CHE", "Ireland": "IRL",
    "Denmark": "DNK", "Belgium": "BEL", "Poland": "POL", "Austria": "AUT",
    "Iceland": "ISL", "Russia": "RUS", "Ukraine": "UKR",
    "United Arab Emirates": "ARE", "UAE": "ARE", "Qatar": "QAT",
    "Singapore": "SGP", "Mexico": "MEX", "Thailand": "THA",
    "Vietnam": "VNM", "Viet Nam": "VNM", "Indonesia": "IDN", "Malaysia": "MYS",
    "Taiwan": "TWN", "Hong Kong": "HKG", "Pakistan": "PAK",
    "Argentina": "ARG", "Chile": "CHL", "Croatia": "HRV",
    "Czech Republic": "CZE", "Egypt": "EGY", "Hungary": "HUN",
    "Iran": "IRN", "Kazakhstan": "KAZ", "Nepal": "NPL",
    "Portugal": "PRT", "Romania": "ROU", "Saudi Arabia": "SAU",
    "Tunisia": "TUN", "Albania": "ALB", "Bangladesh": "BGD",
}

COUNTRY_NAMES_TR = {
    "Norway": "Norveç", "Sweden": "İsveç", "Finland": "Finlandiya",
    "France": "Fransa", "Canada": "Kanada", "USA": "ABD", "Germany": "Almanya",
    "UK": "İngiltere", "Japan": "Japonya", "China": "Çin", "India": "Hindistan",
    "Turkey": "Türkiye", "Australia": "Avustralya", "Italy": "İtalya",
    "Spain": "İspanya", "South Korea": "Güney Kore", "Ireland": "İrlanda",
    "Denmark": "Danimarka", "Switzerland": "İsviçre", "Brazil": "Brezilya",
    "Netherlands": "Hollanda", "Belgium": "Belçika", "Poland": "Polonya",
    "Austria": "Avusturya", "Iceland": "İzlanda",
}

def get_gpu_power(gpu_name):
    if pd.isna(gpu_name): return DEFAULT_GPU_POWER
    for key, val in GPU_POWER.items():
        if key.lower() in str(gpu_name).lower(): return val
    return DEFAULT_GPU_POWER

def get_country_factor(country):
    if pd.isna(country): return DEFAULT_EMISSION_FACTOR
    for key, val in COUNTRY_EMISSIONS.items():
        if key.lower() in str(country).lower(): return val
    return DEFAULT_EMISSION_FACTOR
