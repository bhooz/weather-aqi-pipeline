import os
import logging
import pandas as pd
import numpy as np

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

INPUT_CSV = "data/processed/weather_aqi_processed.csv"
OUTPUT_CSV = "data/processed/weather_aqi_analytics.csv"


def calculate_aqi_category(pm25: float) -> str:
    """Classify Air Quality Index (AQI) based on US EPA PM2.5 thresholds."""
    if pd.isna(pm25):
        return "Unknown"
    elif pm25 <= 12.0:
        return "Good"
    elif pm25 <= 35.4:
        return "Moderate"
    elif pm25 <= 55.4:
        return "Unhealthy for Sensitive Groups"
    elif pm25 <= 150.4:
        return "Unhealthy"
    elif pm25 <= 250.4:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def compute_rolling_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute 24-hour rolling averages per city for temperature and particulate matter."""
    df = df.sort_values(by=["city", "timestamp"]).reset_index(drop=True)

    # Group by city to apply rolling window logic independently
    df["temp_24h_avg"] = df.groupby("city")["temperature_celsius"].transform(
        lambda x: x.rolling(window=24, min_periods=1).mean()
    )
    
    df["pm2_5_24h_avg"] = df.groupby("city")["pm2_5_ug_m3"].transform(
        lambda x: x.rolling(window=24, min_periods=1).mean()
    )

    df["humidity_24h_avg"] = df.groupby("city")["humidity_percent"].transform(
        lambda x: x.rolling(window=24, min_periods=1).mean()
    )

    return df


def add_analytical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add time-based features and AQI classification labels."""
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_name"] = df["timestamp"].dt.day_name()
    df["date"] = df["timestamp"].dt.date

    # Apply AQI Classification
    df["aqi_category"] = df["pm2_5_ug_m3"].apply(calculate_aqi_category)

    # Temperature Anomaly: deviation from city mean
    city_temp_mean = df.groupby("city")["temperature_celsius"].transform("mean")
    df["temp_anomaly"] = df["temperature_celsius"] - city_temp_mean

    return df


def main():
    logging.info("Starting Analytical Feature Engineering Pipeline...")

    if not os.path.exists(INPUT_CSV):
        logging.error(f"Input file {INPUT_CSV} not found. Please run process_data.py first.")
        return

    df = pd.read_csv(INPUT_CSV)
    logging.info(f"Loaded {len(df)} rows from {INPUT_CSV}")

    # Compute Rolling Metrics & Analytical Features
    df_analytics = compute_rolling_metrics(df)
    df_analytics = add_analytical_features(df_analytics)

    # Save Processed Analytics Data
    df_analytics.to_csv(OUTPUT_CSV, index=False)
    logging.info(f"Analytics pipeline complete. Saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()