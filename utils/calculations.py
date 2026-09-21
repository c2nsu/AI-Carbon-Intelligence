from utils.data_loader import get_gpu_power, get_country_factor

def calc_co2(gpu_count, gpu_power_w, hours, emission_factor):
    energy_kwh = (gpu_count * gpu_power_w / 1000) * hours
    co2_kg = energy_kwh * emission_factor
    co2_ton = co2_kg / 1000
    return energy_kwh, co2_kg, co2_ton

def calc_energy_cost(energy_kwh, country="USA"):
    cost_per_kwh = {
        "Germany": 0.35, "UK": 0.34, "France": 0.21, "USA": 0.12,
        "Norway": 0.08, "Turkey": 0.10, "China": 0.08, "India": 0.07,
        "Japan": 0.22, "South Korea": 0.11, "Canada": 0.10, "Brazil": 0.12,
    }
    rate = 0.15
    for key, val in cost_per_kwh.items():
        if key.lower() in str(country).lower():
            rate = val
            break
    return energy_kwh * rate

def sustainability_score(co2_kg, energy_kwh, cost_usd):
    score = 100
    if co2_kg > 1000000: score -= 40
    elif co2_kg > 100000: score -= 30
    elif co2_kg > 10000: score -= 20
    elif co2_kg > 1000: score -= 15
    elif co2_kg > 100: score -= 10
    elif co2_kg > 10: score -= 5
    if energy_kwh > 500000: score -= 30
    elif energy_kwh > 50000: score -= 20
    elif energy_kwh > 5000: score -= 10
    elif energy_kwh > 500: score -= 5
    if cost_usd > 50000: score -= 15
    elif cost_usd > 10000: score -= 10
    elif cost_usd > 1000: score -= 5
    return max(0, min(100, score))

def score_color(score):
    if score >= 80: return "#2ecc71"
    elif score >= 60: return "#27ae60"
    elif score >= 40: return "#f39c12"
    elif score >= 20: return "#e67e22"
    else: return "#e74c3c"

def score_label(score):
    if score >= 80: return "Mükemmel"
    elif score >= 60: return "İyi"
    elif score >= 40: return "Orta"
    elif score >= 20: return "Zayıf"
    else: return "Kötü"

def carbon_equivalents(co2_ton):
    FLIGHT_TON = 1.0
    CAR_TON_PER_KM = 0.000121
    TREE_TON_PER_YEAR = 0.022
    PHONE_CHARGE_TON = 0.000008
    STEAK_TON_PER_KG = 0.027
    SHOWER_TON_PER_MIN = 0.000056

    flights = co2_ton / FLIGHT_TON
    car_km = co2_ton / CAR_TON_PER_KM
    trees = co2_ton / TREE_TON_PER_YEAR
    phone = co2_ton / PHONE_CHARGE_TON
    steak = co2_ton / STEAK_TON_PER_KG
    shower = co2_ton / SHOWER_TON_PER_MIN
    return flights, car_km, trees, phone, steak, shower

def best_alternative(gpu_name, hours, country):
    from utils.data_loader import COUNTRY_EMISSIONS
    current_gw = get_gpu_power(gpu_name)
    current_ef = get_country_factor(country)
    _, _, current_co2 = calc_co2(1, current_gw, hours, current_ef)
    best_co2 = current_co2
    best_country = country
    for c, ef in COUNTRY_EMISSIONS.items():
        _, _, co2 = calc_co2(1, current_gw, hours, ef)
        if co2 < best_co2:
            best_co2 = co2
            best_country = c
    return best_country, best_co2, current_co2
