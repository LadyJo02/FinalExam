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
    try:
        crm_df = pd.read_sql('SELECT * FROM "CRM_cust_info"', crm_engine)
        erp_df = pd.read_sql('SELECT * FROM "ERP_order_info"', erp_engine)
        wh_df = pd.read_sql('SELECT * FROM dw_summary', warehouse_engine)
        return crm_df, erp_df, wh_df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

crm_df, erp_df, wh_df = load_data()

# CRM Section
st.subheader("🧑‍💼 CRM Overview")
if not crm_df.empty:
    st.dataframe(crm_df)
    if 'cust_name' in crm_df.columns and 'total_purchases' in crm_df.columns:
        fig1 = px.bar(
            crm_df,
            x="cust_name",
            y="total_purchases",
            title="Total Purchases per Customer",
            labels={"cust_name": "Customer Name", "total_purchases": "Total Purchases"}
        )
        st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("CRM data not available.")

# ERP Section
st.subheader("🏭 ERP Overview")
if not erp_df.empty:
    st.dataframe(erp_df)
    if 'total_amount' in erp_df.columns and 'product_name' in erp_df.columns:
        fig2 = px.pie(
            erp_df,
            values='total_amount',
            names='product_name',
            title='Sales Distribution by Product'
        )
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("ERP data not available.")

# Data Warehouse Section
st.subheader("🏢 Data Warehouse Summary")
if not wh_df.empty:
    st.dataframe(wh_df)
    if 'records_processed' in wh_df.columns and 'source' in wh_df.columns:
        fig3 = px.bar(
            wh_df,
            x="source",
            y="records_processed",
            color="source",
            title="Records Processed by Source"
        )
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Data Warehouse summary not available.")

st.markdown("---")
st.caption("Final Exam Dashboard | Cloud Computing | Canaman, Macalisang, Pabololot, Santos")
