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

# App title with improved layout
st.set_page_config(page_title="Cloud Data Dashboard", layout="wide")
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>📊 Cloud Computing Data Dashboard</h1>
    <p style='text-align: center;'>Explore CRM and ERP insights in one unified view.</p>
""", unsafe_allow_html=True)

# Load cleaned data
@st.cache_data
def load_data():
    try:
        df = pd.read_sql('SELECT * FROM "crm_erp"', warehouse_engine)
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Sidebar filters with navigation
st.sidebar.header("🔍 Filter Options")
if not df.empty:
    available_dates = pd.to_datetime(df['OrderDate'].dt.date.unique())
    min_date, max_date = available_dates.min(), available_dates.max()
    selected_date = st.sidebar.date_input("Select Order Date", value=min_date, min_value=min_date, max_value=max_date)
    filtered_df = df[df['OrderDate'].dt.date == selected_date]

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📌 Sections")
    st.sidebar.markdown("- [📊 Key Business Insights](#key-business-insights)")
    st.sidebar.markdown("- [💰 Total Sales by Customer](#total-sales-by-customer)")
    st.sidebar.markdown("- [🏆 Top Selling Products](#top-selling-products)")
    st.sidebar.markdown("- [📈 Monthly Quantity Ordered (All Time)](#monthly-quantity-ordered-all-time)")
else:
    selected_date = None
    filtered_df = pd.DataFrame()

# CRM + ERP Section Combined
st.subheader("📄 CRM & ERP Combined Overview")
if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Key Business Insights", anchor="key-business-insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_sales = filtered_df['SalesAmount'].sum()
        st.metric(label="💵 Total Revenue", value=f"${total_sales:,.2f}")

    with col2:
        total_products = filtered_df['ProductName'].nunique() if 'ProductName' in filtered_df.columns else 0
        st.metric(label="📦 Total Products", value=total_products)

    with col3:
        total_customers = filtered_df['CustomerID'].nunique()
        st.metric(label="🧑 Total Customers", value=total_customers)

    st.markdown("---")

    # Total Sales by Customer
    if 'FirstName' in filtered_df.columns and 'SalesAmount' in filtered_df.columns:
        st.subheader("💰 Total Sales by Customer", anchor="total-sales-by-customer")
        sales_by_customer = filtered_df.groupby('FirstName')['SalesAmount'].sum().reset_index().sort_values(by='SalesAmount', ascending=False)
        fig1 = px.bar(sales_by_customer, x='FirstName', y='SalesAmount',
                      title="💰 Total Sales by Customer",
                      labels={'FirstName': 'Customer Name', 'SalesAmount': 'Total Sales'},
                      color='SalesAmount', color_continuous_scale='Viridis')
        st.plotly_chart(fig1, use_container_width=True)

    # Top Selling Products
    if 'ProductName' in filtered_df.columns and 'SalesAmount' in filtered_df.columns:
        st.subheader("🏆 Top Selling Products", anchor="top-selling-products")
        product_sales = filtered_df.groupby('ProductName')['SalesAmount'].sum().reset_index().sort_values(by='SalesAmount', ascending=False)
        fig2 = px.pie(product_sales, values='SalesAmount', names='ProductName',
                      title="🏆 Top Selling Products")
        st.plotly_chart(fig2, use_container_width=True)

# Always show full trend chart over time regardless of selected date
if not df.empty and 'OrderDate' in df.columns and 'Quantity' in df.columns:
    st.markdown("---")
    st.subheader("📈 Monthly Quantity Ordered (All Time)", anchor="monthly-quantity-ordered-all-time")
    monthly_quantity = df.groupby(df['OrderDate'].dt.to_period('M'))['Quantity'].sum().reset_index()
    monthly_quantity['OrderDate'] = monthly_quantity['OrderDate'].dt.to_timestamp()
    fig3 = px.line(monthly_quantity, x='OrderDate', y='Quantity', markers=True,
                   title="Monthly Quantity Ordered",
                   line_shape='spline', render_mode='svg')
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("No data available for the selected date.")

st.markdown("---")
st.caption("Final Exam Dashboard | Cloud Computing | Canaman, Macalisang, Pabololot, Santos")
