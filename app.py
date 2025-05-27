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
st.markdown("Explore CRM and ERP insights in one unified view.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
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
st.subheader("📄 CRM & ERP Combined Overview")
if not df.empty:
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Data Visualizations")

    # Total Sales by Customer
    if 'FirstName' in df.columns and 'SalesAmount' in df.columns:
        sales_by_customer = df.groupby('FirstName')['SalesAmount'].sum().reset_index().sort_values(by='SalesAmount', ascending=False)
        fig1 = px.bar(sales_by_customer, x='FirstName', y='SalesAmount',
                      title="💰 Total Sales by Customer",
                      labels={'FirstName': 'Customer Name', 'SalesAmount': 'Total Sales'})
        st.plotly_chart(fig1, use_container_width=True)

    # Top Selling Products
    if 'ProductName' in df.columns and 'SalesAmount' in df.columns:
        product_sales = df.groupby('ProductName')['SalesAmount'].sum().reset_index().sort_values(by='SalesAmount', ascending=False)
        fig2 = px.pie(product_sales, values='SalesAmount', names='ProductName',
                      title="🏆 Top Selling Products")
        st.plotly_chart(fig2, use_container_width=True)

    # Quantity Trend Over Time
    if 'OrderDate' in df.columns and 'Quantity' in df.columns:
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        daily_quantity = df.groupby(df['OrderDate'].dt.to_period('M'))['Quantity'].sum().reset_index()
        daily_quantity['OrderDate'] = daily_quantity['OrderDate'].dt.to_timestamp()
        fig3 = px.line(daily_quantity, x='OrderDate', y='Quantity', markers=True,
                       title="📈 Monthly Quantity Ordered")
        st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Cleaned data from crm_erp not available.")

st.markdown("---")
st.caption("Final Exam Dashboard | Cloud Computing | Canaman, Macalisang, Pabololot, Santos")
