import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Spot Instance Analysis Dashboard", layout="wide")

st.title("Spot Instance Analysis Dashboard")
st.markdown("Upload your CSV files to start the analysis.")

# ---------------------------
# 1. Take Input at Run Time
# ---------------------------
st.sidebar.header("Upload CSV Files")
fulfillment_file = st.sidebar.file_uploader("Upload RequestFulfillment CSV", type=["csv"])
interruption_file = st.sidebar.file_uploader("Upload SpotInterruptionWarning CSV", type=["csv"])

if fulfillment_file is not None and interruption_file is not None:
    # Read CSV files from the uploaded files
    fulfillment_df = pd.read_csv(fulfillment_file)
    interruption_df = pd.read_csv(interruption_file)
    
    # Convert time columns to datetime
    fulfillment_df['time'] = pd.to_datetime(fulfillment_df['time'])
    interruption_df['time'] = pd.to_datetime(interruption_df['time'])
    
    # Merge the data on instance_id to get common instances
    merged_df = pd.merge(fulfillment_df, interruption_df, on='instance_id', suffixes=('_start', '_stop'))
    
    # Calculate uptime in hours
    merged_df['uptime_hours'] = (merged_df['time_stop'] - merged_df['time_start']).dt.total_seconds() / 3600.0
    
    # ---------------------------
    # 2. Compute Summary Statistics
    # ---------------------------
    summary_by_type = merged_df.groupby('instance_type_start')['uptime_hours'].agg(
        total_uptime_hours='sum',
        mean_uptime_hours='mean',
        median_uptime_hours='median',
        mode_uptime_hours=lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        std_dev_uptime_hours='std',
        instance_count='count'
    ).reset_index().sort_values(by='total_uptime_hours', ascending=False)
    
    availability_stats = merged_df.groupby(['availability_zone_start', 'instance_type_start']).size().reset_index(name='count')
    most_available_per_region = availability_stats.sort_values('count', ascending=False).groupby('availability_zone_start').first().reset_index()
    uptime_stats_by_type = merged_df.groupby('instance_type_start')['uptime_hours'].agg(['mean', 'std', 'count']).reset_index().sort_values('mean', ascending=False)
    interruption_freq = interruption_df['instance_id'].map(merged_df.set_index('instance_id')['instance_type_start']).value_counts().reset_index()
    interruption_freq.columns = ['instance_type', 'interruption_count']
    
    st.markdown("### Summary Statistics by Instance Type")
    st.dataframe(summary_by_type)
    
    st.markdown("### Interruption Frequency by Instance Type")
    st.dataframe(interruption_freq)
    
    # ---------------------------
    # 3. Sidebar Filters for Interactive Analysis
    # ---------------------------
    st.sidebar.header("Filter Options")
    instance_types = merged_df['instance_type_start'].unique().tolist()
    selected_instance_types = st.sidebar.multiselect("Select Instance Type(s)", instance_types, default=instance_types)
    
    regions = merged_df['availability_zone_start'].unique().tolist()
    selected_regions = st.sidebar.multiselect("Select Region(s)", regions, default=regions)
    
    filtered_df = merged_df[
        (merged_df['instance_type_start'].isin(selected_instance_types)) &
        (merged_df['availability_zone_start'].isin(selected_regions))
    ]
    
    st.markdown("### Overview of Filtered Data")
    st.write(f"Total instances analyzed: **{merged_df['instance_id'].nunique()}**")
    st.write(f"Filtered instances: **{filtered_df['instance_id'].nunique()}**")
    st.dataframe(filtered_df.head())
    
    # ---------------------------
    # 4. Interactive Charts
    # ---------------------------
    st.markdown("## Uptime Distribution by Instance Type")
    fig1 = px.histogram(
        filtered_df,
        x="uptime_hours",
        color="instance_type_start",
        nbins=30,
        title="Distribution of Instance Uptime by Instance Type",
        labels={"uptime_hours": "Uptime (hours)", "instance_type_start": "Instance Type"},
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("## Most Available Instance Type per Region")
    fig2 = px.bar(
        most_available_per_region,
        x="availability_zone_start",
        y="count",
        color="instance_type_start",
        title="Most Available Instance Type per Region",
        labels={"availability_zone_start": "Region", "count": "Count", "instance_type_start": "Instance Type"},
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("## Top 10 Instance Types by Total Uptime")
    fig3 = px.bar(
        summary_by_type.head(10),
        x="instance_type_start",
        y="total_uptime_hours",
        color="instance_type_start",
        title="Top 10 Instance Types by Total Uptime",
        labels={"instance_type_start": "Instance Type", "total_uptime_hours": "Total Uptime (hrs)"},
        template="plotly_white"
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # ---------------------------
    # 5. Download Options for Data Files
    # ---------------------------
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    
    csv_summary = convert_df(summary_by_type)
    st.download_button(
        label="Download Uptime Summary as CSV",
        data=csv_summary,
        file_name='uptime_summary.csv',
        mime='text/csv'
    )
    
    # You can add additional download buttons for Excel or other outputs if desired.
    
else:
    st.info("Please upload both the RequestFulfillment CSV and the SpotInterruptionWarning CSV to view the analysis.")
