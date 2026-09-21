# 🌱 AI Carbon Intelligence Platform

> **Measure • Compare • Optimize**

AI modellerinin çevresel etkisini analiz etmek ve yapay zekâ sistemlerinin karbon ayak izini daha anlaşılır hale getirmek için geliştirilmiş **Streamlit tabanlı AI Sustainability Platform**.

Platform; AI modellerinin eğitim ve hesaplama süreçlerinden kaynaklanan karbon emisyonlarını inceleyerek **karbon hesaplama, model karşılaştırma, ülke bazlı analiz, senaryo simülasyonu ve sürdürülebilirlik değerlendirmesi** sunar.

---

## 🎯 Projenin Amacı

Yapay zekâ modellerinin büyümesiyle birlikte hesaplama gücü, enerji tüketimi ve karbon emisyonları da önemli bir sürdürülebilirlik konusu haline gelmiştir.

Bu projenin amacı:

* 🤖 AI modellerinin karbon ayak izini analiz etmek
* ⚡ Enerji tüketimi ve emisyon ilişkisini incelemek
* 🌍 Farklı ülkelerin karbon yoğunluklarını karşılaştırmak
* 🖥️ GPU türlerinin enerji ve karbon etkisini değerlendirmek
* 🔄 Farklı senaryoları karşılaştırmak
* 📊 Veri analizi ve görselleştirme ile sonuçları anlaşılır hale getirmek
* 🌱 Daha sürdürülebilir AI geliştirme kararlarını desteklemek

---

## 🚀 Platform Özellikleri

### 📊 Ana Dashboard

Genel proje metriklerinin tek bir ekranda görüntülenmesini sağlar.

* Toplam CO₂ emisyonu
* Tahmini enerji tüketimi
* Yenilenebilir enerji senaryosu
* PUE göstergesi
* Model sayısı
* Genel sürdürülebilirlik göstergeleri

---

### 🧮 Karbon Hesaplayıcı

GPU, çalışma süresi ve ülkenin emisyon faktörünü kullanarak tahmini karbon emisyonunu hesaplar.

Temel hesaplama:

```text
Enerji (kWh)
= GPU Sayısı × GPU Gücü × Çalışma Süresi

CO₂
= Enerji Tüketimi × Emisyon Faktörü
```

Sonuçlar enerji tüketimi, karbon emisyonu ve maliyet açısından değerlendirilebilir.

---

### 🌍 Global Carbon Map

Ülkelerin elektrik üretimindeki karbon yoğunluklarını karşılaştırmaya yönelik küresel analiz sunar.

Platform içerisinde farklı ülkeler için emisyon faktörleri kullanılarak:

* Ülke karşılaştırmaları
* Karbon yoğunluğu
* Bölgesel farklılıklar
* Harita tabanlı görselleştirmeler

incelenebilir.

---

### 🔄 What-If Simülasyonu

Kullanıcının farklı koşulları deneyerek sonuçların nasıl değiştiğini incelemesini sağlar.

Örneğin:

* Farklı GPU kullanımı
* Farklı çalışma süreleri
* Farklı ülkelerde çalıştırma
* Farklı enerji/emisyon faktörleri

üzerinden senaryolar oluşturulabilir.

---

### 🌱 Sustainability Score

Modelin karbon emisyonu, enerji tüketimi ve maliyet bilgilerini kullanarak bir sürdürülebilirlik skoru hesaplanır.

Skor:

```text
0 ─────────────── 100
Düşük             Yüksek
```

Bu skor, farklı modeller veya senaryolar arasında çevresel metrikleri daha kolay karşılaştırmak için kullanılır.

---

### 🤖 Model Explorer

Veri setindeki AI modellerinin özelliklerini incelemek için kullanılır.

Model bazında:

* Model adı
* Parametre bilgileri
* Eğitim verileri
* Eğitim hesaplama maliyeti
* GPU bilgileri
* Emisyon değerleri
* Model türü
* Modality
* MoE / Dense yapısı

gibi bilgiler analiz edilebilir.

---

### 📊 Model Karşılaştırma

Farklı AI modellerinin karbon emisyonlarını ve teknik özelliklerini karşılaştırmaya yönelik görselleştirmeler içerir.

Örneğin:

* Emisyon karşılaştırması
* GPU karşılaştırması
* Model kategorileri
* Sayısal değişken dağılımları
* Korelasyon analizleri

---

### 🧬 Model Soy Ağacı

AI modellerinin gelişimini ve model aileleri arasındaki ilişkileri görsel olarak incelemeye yönelik bir bölüm içerir.

---

### 🏆 Green Ranking

Modellerin çevresel metriklerini karşılaştırmaya yönelik sıralama görünümü sunar.

Değerlendirilen temel değişkenler arasında:

* CO₂ emisyonu
* Enerji tüketimi
* GPU kullanımı
* Model özellikleri

yer alır.

---

### 🧠 ML & Explainability

Proje kapsamında makine öğrenmesi ve açıklanabilirlik yaklaşımı da kullanılmaktadır.

Veri analizi ve modelleme sürecinde değişkenlerin emisyon tahminleri üzerindeki etkisinin incelenmesi amaçlanmıştır.

Projede ayrıca permutation importance ve hata analizi gibi görselleştirmeler bulunmaktadır.

---

### 🌎 Gerçek Dünya Eşdeğerleri

CO₂ emisyonlarını günlük hayattan örneklerle daha anlaşılır hale getirir.

Örneğin:

* ✈️ Uçuş
* 🚗 Araç kullanımı
* 🌳 Ağaçların yıllık CO₂ absorpsiyonu
* 📱 Telefon şarjı
* 🥩 Gıda tüketimi
* 🚿 Duş

gibi eşdeğerler üzerinden karbon etkisi gösterilir.

---

### 📄 Denetim Raporu

Proje içerisinde analiz sonuçlarının raporlanmasına yönelik bir bölüm bulunmaktadır.

Amaç; hesaplama sonuçlarını, veri kalitesini ve kullanılan analizleri daha düzenli şekilde sunmaktır.

---

# 🗂️ Proje Yapısı

```text
AI-Carbon-Intelligence/
│
├── app.py
├── requirements.txt
├── start.bat
│
├── HF_models_imputed_realistic_v2.csv
│
├── carbon_emissions_FINAL (1).ipynb
│
├── Karbon_Emisyon_Model_Kurma_Proje_Raporu.docx
│
├── assets/
│
├── img/
│   ├── bildirilen_ve_ana_emisyon_scatter.png
│   ├── boxplot.png
│   ├── builtin_permutation.png
│   ├── dünya_haritasi.png
│   ├── emisyon_bar.png
│   ├── gpu_barplot.png
│   ├── kategorilere_göre_boxplot.png
│   ├── korelasyon.png
│   ├── residual_error_analysis.png
│   ├── sayisal_degiskenlerin_dagilimi.png
│   └── scatter.png
│
├── pages/
│   ├── 01_📊_Veri_Analizi.py
│   ├── 01_🧮_Carbon_Calculator.py
│   ├── 02_🌍_Global_Carbon_Map.py
│   ├── 03_🤖_Model_Explorer.py
│   ├── 03_🧮_Green_AI_Planner.py
│   ├── 04_📊_Compare_and_Visualize.py
│   ├── 04_🔄_Senaryo_Simulatoru.py
│   ├── 05_🎯_Green_AI_Optimizer.py
│   ├── 05_🏆_Green_Ranking.py
│   ├── 06_🤖_Model_Explorer.py
│   ├── 06_🧠_ML_and_Explainability.py
│   ├── 07_📄_Report.py
│   └── 07_📄_Rapor.py
│
└── utils/
    ├── calculations.py
    ├── data_loader.py
    └── theme.py
```

---

# 🛠️ Kullanılan Teknolojiler

| Teknoloji            | Kullanım                     |
| -------------------- | ---------------------------- |
| **Python**           | Ana programlama dili         |
| **Streamlit**        | İnteraktif web platformu     |
| **Pandas**           | Veri işleme ve analiz        |
| **NumPy**            | Sayısal hesaplamalar         |
| **Plotly**           | İnteraktif görselleştirmeler |
| **Matplotlib**       | Veri görselleştirme          |
| **OpenPyXL**         | Excel veri işlemleri         |
| **Jupyter Notebook** | Veri analizi ve modelleme    |

---

# 📊 Veri Analizi

Projede AI modellerine ait çeşitli teknik ve çevresel değişkenler kullanılmaktadır.

Örnek değişkenler:

* `training_flops`
* `parameter_values`
* `training_token_count`
* `tier`
* `method`
* `inference_gpu_type`
* `inference_gpu_count`
* `type`
* `modality`
* `is_moe`
* `model_region`
* `emission_factor_tco2e_per_mwh`
* `training_gpu_type`
* `disclosed_electricity_used_mwh`

Bu değişkenler üzerinden model özellikleri ile enerji tüketimi ve karbon emisyonları arasındaki ilişkiler incelenmektedir.

---

# ⚙️ Kurulum

Projeyi klonlayın:

```bash
git clone https://github.com/USERNAME/AI-Carbon-Intelligence.git
```

Proje klasörüne girin:

```bash
cd AI-Carbon-Intelligence
```

Sanal ortam oluşturmanız önerilir:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

Uygulamayı başlatın:

```bash
streamlit run app.py
```

Alternatif olarak Windows'ta:

```bash
start.bat
```

---

# 📈 Proje Akışı

```text
AI Model Verileri
       ↓
Veri Ön İşleme
       ↓
Karbon Emisyon Hesaplama
       ↓
Enerji & GPU Analizi
       ↓
Ülke / Bölge Karşılaştırması
       ↓
What-If Senaryoları
       ↓
Model Karşılaştırma
       ↓
Sürdürülebilirlik Analizi
       ↓
Streamlit Dashboard
```

---

# 🔬 Analiz Yaklaşımı

Proje yalnızca tek bir karbon değeri göstermek yerine AI modellerinin çevresel etkisini farklı boyutlardan incelemeyi amaçlamaktadır.

Analiz kapsamında:

**Model → GPU → Enerji → Ülke → Emisyon → Maliyet → Sürdürülebilirlik**

ilişkisi ele alınmaktadır.

---

# 🌱 Projenin Odak Noktası

Bu platformun temel yaklaşımı:

> **AI sistemlerinin yalnızca performansını değil, çevresel maliyetini de görünür hale getirmek.**

Bu nedenle proje bir karbon hesaplayıcının ötesinde; veri analizi, görselleştirme, model karşılaştırma ve senaryo analizlerini bir araya getiren bir **AI Sustainability Platform** olarak tasarlanmıştır.

---

# 👩‍💻 Proje Türü

**AI Sustainability / Data Analytics / Machine Learning / Streamlit**

Bu proje akademik/grup proje çalışması kapsamında geliştirilmiştir. Streamlit kısmı bana aittir.
