import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Weather & Air Quality Analytics",
    page_icon="🌤️",
    layout="wide"
)

DATA_PATH = "data/processed/weather_aqi_analytics.csv"


@st.cache_data
def load_data():
    """Load cleaned analytics dataset with caching for fast UI re-renders."""
    if not os.path.exists(DATA_PATH):
        return None
    df = pd.read_csv(DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def main():
    st.title("🌤️ Real-Time Weather & Air Quality Analytics Dashboard")
    st.markdown("Interactive analytics pipeline powered by Open-Meteo API, Pandas, and Plotly.")

    df = load_data()

    if df is None:
        st.error("⚠️ Processed dataset not found! Please run `src/analyze_data.py` first.")
        return

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Options")
    cities = df["city"].unique().tolist()
    selected_city = st.sidebar.selectbox("Select City", cities, index=0)

    # Filter dataset by selected city
    city_df = df[df["city"] == selected_city].sort_values("timestamp")

    # Top KPI Metrics Cards
    st.subheader(f"📊 Live Overview for {selected_city}")
    col1, col2, col3, col4 = st.columns(4)

    latest_row = city_df.iloc[-1] if not city_df.empty else None

    if latest_row is not None:
        col1.metric(
            label="Temperature",
            value=f"{latest_row['temperature_celsius']:.1f} °C",
            delta=f"{latest_row['temp_anomaly']:.1f} °C vs Avg"
        )
        col2.metric(
            label="Humidity",
            value=f"{latest_row['humidity_percent']:.0f} %"
        )
        col3.metric(
            label="PM2.5 Level",
            value=f"{latest_row['pm2_5_ug_m3']:.1f} µg/m³"
        )
        col4.metric(
            label="AQI Status",
            value=latest_row['aqi_category']
        )

    st.markdown("---")

    # Visualizations Layout
    row1_col1, row1_col2 = st.columns(2)

    # 1. Temperature Trend & 24h Rolling Average
    with row1_col1:
        st.subheader("🌡️ Temperature vs 24h Moving Average")
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=city_df["timestamp"], y=city_df["temperature_celsius"],
            mode="lines", name="Hourly Temp (°C)", line=dict(color="#FFA500", width=1.5)
        ))
        fig_temp.add_trace(go.Scatter(
            x=city_df["timestamp"], y=city_df["temp_24h_avg"],
            mode="lines", name="24h Rolling Avg (°C)", line=dict(color="#FF4500", width=3)
        ))
        fig_temp.update_layout(template="plotly_white", xaxis_title="Timestamp", yaxis_title="°C")
        st.plotly_chart(fig_temp, use_container_width=True)

    # 2. Air Quality Particulate Matter (PM2.5 vs PM10)
    with row1_col2:
        st.subheader("🌫️ Air Quality Trends (PM2.5 & PM10)")
        fig_aqi = go.Figure()
        fig_aqi.add_trace(go.Scatter(
            x=city_df["timestamp"], y=city_df["pm2_5_ug_m3"],
            mode="lines", name="PM2.5", line=dict(color="#1F77B4")
        ))
        fig_aqi.add_trace(go.Scatter(
            x=city_df["timestamp"], y=city_df["pm10_ug_m3"],
            mode="lines", name="PM10", line=dict(color="#2CA02C")
        ))
        fig_aqi.update_layout(template="plotly_white", xaxis_title="Timestamp", yaxis_title="µg/m³")
        st.plotly_chart(fig_aqi, use_container_width=True)

    # Row 2: AQI Distribution Comparison
    st.subheader("🏙️ City-Wide Air Quality Distribution")
    fig_pie = px.pie(
        df,
        names="aqi_category",
        title="Overall AQI Status Distribution Across All Cities",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Raw Analytics Data Preview
    with st.expander("📄 View Processed Analytics Dataset"):
        st.dataframe(city_df)


if __name__ == "__main__":
    main()