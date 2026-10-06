import os
import json
import glob
import logging
import pandas as pd

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"


def load_json_file(filepath: str) -> dict:
    """Load and return raw JSON data from a given filepath."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def process_city_payload(raw_json: dict) -> pd.DataFrame:
    """Transform nested city weather and air quality JSON into a clean DataFrame."""
    city_name = raw_json.get("city")
    lat = raw_json.get("latitude")
    lon = raw_json.get("longitude")

    # Extract Weather Hourly Data
    weather_hourly = raw_json.get("weather", {}).get("hourly", {})
    df_weather = pd.DataFrame(weather_hourly)

    # Extract Air Quality Hourly Data
    air_hourly = raw_json.get("air_quality", {}).get("hourly", {})
    df_air = pd.DataFrame(air_hourly)

    # Merge Weather and Air Quality DataFrames on timestamp ('time')
    if not df_weather.empty and not df_air.empty:
        df_merged = pd.merge(df_weather, df_air, on="time", how="outer")
    elif not df_weather.empty:
        df_merged = df_weather
    else:
        df_merged = df_air

    # Metadata එක් කිරීම
    df_merged["city"] = city_name
    df_merged["latitude"] = lat
    df_merged["longitude"] = lon

    # Datetime column පරිවර්තනය
    df_merged["timestamp"] = pd.to_datetime(df_merged["time"])
    df_merged.drop(columns=["time"], inplace=True)

    return df_merged


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values, duplicate rows, and column renaming."""
    # Duplicates ඉවත් කිරීම
    df = df.drop_duplicates(subset=["city", "timestamp"]).copy()

    # Rename columns to standard readable format
    rename_map = {
        "temperature_2m": "temperature_celsius",
        "relative_humidity_2m": "humidity_percent",
        "pm2_5": "pm2_5_ug_m3",
        "pm10": "pm10_ug_m3",
        "carbon_monoxide": "co_ug_m3",
        "nitrogen_dioxide": "no2_ug_m3"
    }
    df.rename(columns=rename_map, inplace=True)

    # Missing values handling (Forward fill, then Backward fill)
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    df[numeric_cols] = df[numeric_cols].ffill().bfill()

    # Sort values chronologically by city and timestamp
    df = df.sort_values(by=["city", "timestamp"]).reset_index(drop=True)

    return df


def main():
    logging.info("Starting Data Processing Pipeline...")
    raw_files = glob.glob(os.path.join(RAW_DATA_DIR, "*_raw.json"))

    if not raw_files:
        logging.warning("No raw JSON files found in data/raw. Run fetch_data.py first.")
        return

    all_city_dfs = []
    for filepath in raw_files:
        logging.info(f"Processing {filepath}...")
        raw_payload = load_json_file(filepath)
        df_city = process_city_payload(raw_payload)
        all_city_dfs.append(df_city)

    # සියලුම නගරවල DataFrames එකතු කිරීම
    combined_df = pd.concat(all_city_dfs, ignore_index=True)
    cleaned_df = clean_data(combined_df)

    # Save cleaned dataset to processed directory
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    csv_path = os.path.join(PROCESSED_DATA_DIR, "weather_aqi_processed.csv")
    cleaned_df.to_csv(csv_path, index=False)

    logging.info(f"Successfully processed {len(cleaned_df)} rows.")
    logging.info(f"Saved processed dataset to {csv_path}")


if __name__ == "__main__":
    main()