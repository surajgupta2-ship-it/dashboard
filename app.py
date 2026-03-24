import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Breach Monitoring Dashboard")

CSV_URL = "https://docs.google.com/spreadsheets/d/1lIycbeKh1G6fqAbQvTUkV_PkgU6Lj3L9wQv5aovLxKg/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=300)
def load_data():
    return pd.read_csv(CSV_URL)

df = load_data()
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# Filters
st.sidebar.header("Filters")
site = st.sidebar.multiselect("Site", df['Site Name'].dropna().unique())
bucket = st.sidebar.multiselect("Bucket", df['Breach Bucket'].dropna().unique())

if site:
    df = df[df['Site Name'].isin(site)]
if bucket:
    df = df[df['Breach Bucket'].isin(bucket)]

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Total", int(df['Total'].sum()))
df['LH lane new'] = pd.to_numeric(df['LH lane new'], errors='coerce')
c2.metric("LH Lane", int(df['LH lane new'].fillna(0).sum()))
c3.metric("RCAs", df['RCAs'].count())

# Charts
st.subheader("Daily Trend")
st.plotly_chart(px.line(df.groupby('Date')['Total'].sum().reset_index(), x='Date', y='Total'), use_container_width=True)

df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
st.subheader("Weekly")
st.plotly_chart(px.bar(df.groupby('Week')['Total'].sum().reset_index(), x='Week', y='Total'), use_container_width=True)

st.subheader("Site-wise")
st.plotly_chart(px.bar(df.groupby('Site Name')['Total'].sum().reset_index(), x='Site Name', y='Total'), use_container_width=True)

st.subheader("Bucket")
st.plotly_chart(px.pie(df.groupby('Breach Bucket')['Total'].sum().reset_index(), names='Breach Bucket', values='Total'))

st.subheader("Data")
st.dataframe(df)
