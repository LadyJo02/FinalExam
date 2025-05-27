import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection string for cleaned warehouse table
warehouse_url = os.getenv("DATA_WAREHOUSE_URL")
warehouse_engine = create_engine(warehouse_url)

# App title
st.set_page_config(page_title="Cloud Data Dashboard", layout="wide")
st.title("📊 Cloud Computing Data Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")
date_filter = st.sidebar.date_input("Select Start Date")

# Load cleaned data
@st.cache_data
def load_data():
    try:
        df = pd.read_sql('SELECT * FROM "crm_erp"', warehouse_engine)
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# CRM + ERP Section Combined
st.subheader("🧾 CRM & ERP Combined Overview")
if not df.empty:
    st.dataframe(df)

    # Total Purchases Visualization
    if 'cust_name' in df.columns and 'total_purchases' in df.columns:
        fig1 = px.bar(df, x="cust_name", y="total_purchases",
                      title="Total Purchases per Customer",
                      labels={"cust_name": "Customer Name"})
        st.plotly_chart(fig1, use_container_width=True)

    # Product Sales Visualization
    if 'product_name' in df.columns and 'total_amount' in df.columns:
        fig2 = px.pie(df, names='product_name', values='total_amount',
                      title="Sales Distribution by Product")
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Cleaned data from crm_erp not available.")

st.markdown("---")
st.caption("Final Exam Dashboard | Cloud Computing | Canaman, Macalisang, Pabololot, Santos")
