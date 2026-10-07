# 🌤️ Real-Time Weather & Air Quality Analytics Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An end-to-end data analytics pipeline that fetches multi-city meteorological and air quality data from the **Open-Meteo API**, performs automated ETL transformations and time-series computations with **Pandas**, and presents interactive insights through a **Streamlit & Plotly** web dashboard.

---

## 📌 Project Overview

Understanding atmospheric shifts and pollution patterns requires up-to-date data ingestion and transformation. This platform automates the full data lifecycle:

1. **Extraction:** Ingests hourly temperature, humidity, PM2.5, and PM10 metrics for multiple cities from the Open-Meteo REST APIs.
2. **Transformation:** Cleans the data, fills missing values (forward/backward fill), removes hourly duplicates, and computes time-series features (24-hour rolling averages, temperature anomalies, AQI categories).
3. **Visualization:** Provides an interactive dashboard with city-level filtering, dynamic charts, and KPI metrics.

---

## 🚀 Key Features

- **Automated Data Pipeline:** Modular Python scripts that fetch, parse, and normalize nested JSON responses.
- **Time-Series Analysis:**
  - **24-Hour Rolling Average:** Smooths short-term fluctuations to highlight broader weather trends.
  - **Temperature Anomaly Detection:** Calculates each reading's deviation from the baseline mean temperature.
- **Air Quality Categorization:** Rule-based AQI classification (Good, Moderate, Unhealthy for Sensitive Groups, Unhealthy) using standard PM2.5 thresholds.
- **Interactive Visual Analytics:**
  - Multi-city dropdown filters
  - Dual-axis time-series line charts (Plotly)
  - City-wide pollution level breakdown charts

---

## 🏗️ Project Structure

```text
weather-aqi-analytics/
│
├── data/
│   ├── raw/                 # Raw JSON responses from the Open-Meteo API
│   └── processed/           # Cleaned CSV with computed features (rolling avg, AQI category)
│
├── src/
│   ├── fetch_data.py        # Ingestion script that pulls live API data
│   ├── process_data.py      # Pandas ETL & data-cleaning pipeline
│   └── analyze_data.py      # Feature engineering & time-series aggregation
│
├── app.py                   # Streamlit & Plotly interactive dashboard
├── requirements.txt         # Project dependencies
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Data Manipulation:** Pandas, NumPy
- **Data Ingestion:** Requests (Open-Meteo REST APIs)
- **Visualization:** Streamlit, Plotly Express, Plotly Graph Objects

---

## ⚙️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/bhooz/weather-aqi-analytics.git
cd weather-aqi-analytics
```

### 2. Create a Virtual Environment & Install Dependencies

```bash
# Create the virtual environment (first time only)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Run the Data Pipeline

Run the scripts in order:

```bash
# Step 1: Ingest raw weather & air quality data
python src/fetch_data.py

# Step 2: Clean, merge, and normalize the data
python src/process_data.py

# Step 3: Compute rolling averages and AQI categories
python src/analyze_data.py
```

### 4. Launch the Dashboard

```bash
streamlit run app.py
```

Then open <http://localhost:8501> in your browser.

---

## 📊 Sample Insights

- **Trend Smoothing:** A 24-hour rolling average helps separate daily (diurnal) temperature cycles from broader multi-day weather shifts.
- **Air Quality Patterns:** PM2.5 spikes can coincide with particular low-humidity periods, pushing readings into the *Unhealthy for Sensitive Groups* category.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Kaveesha Gayanjana**

GitHub: [@bhooz](https://github.com/bhooz)