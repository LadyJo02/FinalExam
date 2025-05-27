import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection strings
crm_url = os.getenv("STAGING_CRM_URL")
erp_url = os.getenv("STAGING_ERP_URL")
warehouse_url = os.getenv("DATA_WAREHOUSE_URL")

# Create DB engines
crm_engine = create_engine(crm_url)
erp_engine = create_engine(erp_url)
warehouse_engine = create_engine(warehouse_url)

# App title
st.set_page_config(page_title="Cloud Data Dashboard", layout="wide")
st.title("📊 Cloud Computing Data Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")
date_filter = st.sidebar.date_input("Select Start Date")

# Load data
@st.cache_data
def load_data():
    crm_df = pd.read_sql("SELECT * FROM customers", crm_engine)
    erp_df = pd.read_sql("SELECT * FROM orders", erp_engine)
    wh_df = pd.read_sql("SELECT * FROM data_summary", warehouse_engine)
    return crm_df, erp_df, wh_df

crm_df, erp_df, wh_df = load_data()

# CRM Section
st.subheader("🧑‍💼 CRM Overview")
st.dataframe(crm_df)
fig1 = px.bar(crm_df, x="customer_name", y="total_purchases", title="Total Purchases per Customer")
st.plotly_chart(fig1, use_container_width=True)

# ERP Section
st.subheader("🏭 ERP Overview")
st.dataframe(erp_df)
fig2 = px.pie(erp_df, values='total_amount', names='product_name', title='Sales Distribution by Product')
st.plotly_chart(fig2, use_container_width=True)

# Data Warehouse Section
st.subheader("🏢 Data Warehouse Summary")
st.dataframe(wh_df)
fig3 = px.bar(wh_df, x="source", y="records_processed", color="source", title="Records Processed by Source")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.caption("Final Exam Dashboard | Cloud Computing | Group 4")
