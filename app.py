
import streamlit as st
from databricks import sql
import pandas as pd
import plotly.express as px


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="THAMES | Retail Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. CUSTOM STYLING
# ============================================================

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stMetric"] {
        background-color: rgba(128,128,128,0.08);
        padding: 18px;
        border-radius: 12px;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.2);
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. DATABASE CONNECTION
# ============================================================

def get_connection():
    return sql.connect(
        server_hostname=st.secrets["DATABRICKS_SERVER_HOSTNAME"],
        http_path=st.secrets["DATABRICKS_HTTP_PATH"],
        access_token=st.secrets["DATABRICKS_TOKEN"]
    )


@st.cache_data(ttl=60)
def load_table(table_name):

    with get_connection() as connection:

        query = f"SELECT * FROM default.{table_name}"

        return pd.read_sql(query, connection)


# ============================================================
# 4. LOAD DATA
# ============================================================
TABLES = {
    "products": "thames_products_large_raw",
    "customers": "thames_customer_features_large",
    "activity": "thames_events_large_raw",
    "segments": "thames_customer_segments_large",
    "recommendations": "thames_product_recommendations_large"
}

data = {}
errors = {}

for key, table_name in TABLES.items():

    try:
        data[key] = load_table(table_name)

    except Exception as e:
        data[key] = pd.DataFrame()
        errors[key] = str(e)


products = data["products"]
customers = data["customers"]
activity = data["activity"]
segments = data["segments"]
recommendations = data["recommendations"]


# ============================================================
# 5. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.title("🛍️ THAMES")

    st.caption("Retail Intelligence Platform")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Product Catalogue",
            "Customer Analytics",
            "Customer Segmentation",
            "Recommendations",
            "MLflow Tracking"
        ]
    )

    st.divider()

    st.caption("Powered by")

    st.markdown("""
    - PySpark
    - Delta Lake
    - Spark MLlib
    - MLflow
    - Streamlit
    """)

    st.divider()

    if st.button("Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ============================================================
# 6. APPLICATION HEADER
# ============================================================

st.title("THAMES")

st.caption(
    "An ML-powered retail customer analytics "
    "and product recommendation platform."
)

st.divider()


# ============================================================
# 7. OVERVIEW
# ============================================================

if page == "Overview":

    st.header("Platform Overview")

    if errors:
        st.warning(
            "Some datasets could not be loaded. "
            "Check the affected modules for details."
        )

    total_products = len(products)
    total_customers = len(customers)

    total_purchases = (
        int(customers["Total_Purchases"].sum())
        if not customers.empty else 0
    )

    total_spending = (
        customers["Total_Spending"].sum()
        if not customers.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("Total Products", total_products)
    col3.metric("Total Purchases", total_purchases)
    col4.metric("Total Spending", f"₹{total_spending:,.0f}")

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Product Categories")

        if not products.empty:

            category_counts = (
                products["Category"]
                .value_counts()
                .reset_index()
            )

            category_counts.columns = ["Category", "Products"]

            fig = px.pie(
                category_counts,
                names="Category",
                values="Products",
                hole=0.45
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Product data unavailable.")

    with right:

        st.subheader("Customer Cluster Distribution")

        if not segments.empty:

            cluster_counts = (
                segments["Cluster"]
                .value_counts()
                .sort_index()
                .reset_index()
            )

            cluster_counts.columns = ["Cluster", "Customers"]

            fig = px.bar(
                cluster_counts,
                x="Cluster",
                y="Customers",
                text="Customers",
                title="Customers by K-Means Cluster"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Segmentation data unavailable.")

    st.divider()

    st.subheader("Platform Capabilities")

    col1, col2, col3 = st.columns(3)

    col1.markdown("**Customer Intelligence**")
    col1.write("Understand customer behaviour and purchasing patterns.")

    col2.markdown("**Machine Learning**")
    col2.write("Segment customers using K-Means clustering.")

    col3.markdown("**Recommendations**")
    col3.write("Recommend relevant products using interaction scores.")


# ============================================================
# 8. PRODUCT CATALOGUE
# ============================================================

elif page == "Product Catalogue":

    st.header("Product Catalogue")

    if products.empty:

        st.error(errors.get("products", "Product data unavailable."))

    else:

        col1, col2 = st.columns(2)

        with col1:
            category_filter = st.selectbox(
                "Filter by Category",
                ["All"] + sorted(products["Category"].dropna().unique().tolist())
            )

        with col2:
            search = st.text_input("Search Products")

        filtered_products = products.copy()

        if category_filter != "All":

            filtered_products = filtered_products[
                filtered_products["Category"] == category_filter
                ]

        if search:

            filtered_products = filtered_products[
                filtered_products["Product_Name"]
                .astype(str)
                .str.contains(search, case=False, na=False)
            ]

        st.metric("Products Found", len(filtered_products))

        st.dataframe(
            filtered_products,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 9. CUSTOMER ANALYTICS
# ============================================================

elif page == "Customer Analytics":

    st.header("Customer Analytics")

    if customers.empty:

        st.error(errors.get("customers", "Customer data unavailable."))

    else:

        col1, col2, col3 = st.columns(3)

        col1.metric("Customers", len(customers))

        col2.metric(
            "Total Views",
            int(customers["Total_Views"].sum())
        )

        col3.metric(
            "Total Spending",
            f"₹{customers['Total_Spending'].sum():,.0f}"
        )

        st.divider()

        st.subheader("Customer Behaviour")

        metrics = [
            "Total_Views",
            "Total_Carts",
            "Total_Purchases"
        ]

        metric_choice = st.selectbox(
            "Select Behaviour Metric",
            metrics
        )

        fig = px.bar(
            customers,
            x="Customer_ID",
            y=metric_choice,
            text=metric_choice,
            title=f"Customer {metric_choice.replace('_', ' ')}"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Customer Spending Analysis")

        fig = px.bar(
            customers,
            x="Customer_ID",
            y="Total_Spending",
            text="Total_Spending",
            title="Spending by Customer"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Customer Feature Table")

        st.dataframe(
            customers,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 10. CUSTOMER SEGMENTATION
# ============================================================

elif page == "Customer Segmentation":

    st.header("Customer Segmentation")

    st.write(
        "Customer groups generated using K-Means clustering "
        "with Apache Spark MLlib."
    )

    if segments.empty:

        st.error(errors.get("segments", "Segment data unavailable."))

    else:

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Segments",
            segments["Cluster"].nunique()
        )

        col2.metric(
            "Customers Segmented",
            len(segments)
        )

        st.divider()

        st.subheader("Cluster Assignments")

        st.dataframe(
            segments,
            use_container_width=True,
            hide_index=True
        )

        cluster_counts = (
            segments["Cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        cluster_counts.columns = ["Cluster", "Customers"]

        st.subheader("Cluster Distribution")

        fig = px.bar(
            cluster_counts,
            x="Cluster",
            y="Customers",
            text="Customers",
            color="Cluster",
            title="Customer Distribution Across Clusters"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Combine customer features with cluster assignments
        if not customers.empty:

            segment_details = customers.merge(
                segments,
                on="Customer_ID",
                how="inner"
            )

            st.subheader("Customer Segment Profiles")

            st.dataframe(
                segment_details,
                use_container_width=True,
                hide_index=True
            )

        st.info(
            "Cluster IDs are algorithm-generated labels, "
            "not rankings of customer value. "
            "The current dataset is small and exploratory."
        )


# ============================================================
# 11. PRODUCT RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.header("Personalised Product Recommendations")

    st.write(
        "Product recommendations generated using customer "
        "interaction scores, category preferences and product ratings."
    )

    if recommendations.empty:

        st.error(
            errors.get(
                "recommendations",
                "Recommendation data unavailable."
            )
        )

    else:

        customer_ids = sorted(
            recommendations["Customer_ID"].dropna().unique().tolist()
        )

        if customer_ids:

            selected_customer = st.selectbox(
                "Select Customer",
                customer_ids
            )

            customer_recommendations = recommendations[
                recommendations["Customer_ID"] == selected_customer
                ].copy()

            if "Recommendation_Rank" in customer_recommendations.columns:

                customer_recommendations = (
                    customer_recommendations
                    .sort_values("Recommendation_Rank")
                )

            st.divider()

            st.subheader(
                f"Recommended Products for {selected_customer}"
            )

            st.metric(
                "Products Recommended",
                len(customer_recommendations)
            )

            display_columns = [
                "Product_ID",
                "Product_Name",
                "Category",
                "Price",
                "Rating",
                "Recommendation_Rank"
            ]

            available_columns = [
                column for column in display_columns
                if column in customer_recommendations.columns
            ]

            if not customer_recommendations.empty:

                st.dataframe(
                    customer_recommendations[available_columns],
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No recommendations available for this customer."
                )

            st.divider()

            st.subheader("All Recommendations")

            st.dataframe(
                recommendations,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No customers have recommendations available.")


# ============================================================
# 12. MLFLOW TRACKING
# ============================================================

elif page == "MLflow Tracking":

    st.header("MLflow Experiment Tracking")

    st.write(
        "Experiment tracking and model performance information "
        "from the THAMES K-Means training run."
    )

    st.divider()

    st.subheader("K-Means Model")

    col1, col2, col3 = st.columns(3)

    col1.metric("Algorithm", "K-Means")
    col2.metric("Clusters (K)", "3")
    col3.metric("Silhouette Score", "0.2217")

    st.divider()

    st.subheader("Experiment Details")

    mlflow_details = pd.DataFrame({
        "Parameter": [
            "Algorithm",
            "Number of Clusters",
            "Random Seed",
            "Evaluation Metric",
            "Silhouette Score",
            "Model Artifact"
        ],
        "Value": [
            "K-Means",
            "3",
            "42",
            "Silhouette Score",
            "0.2217",
            "kmeans_model"
        ]
    })

    st.dataframe(
        mlflow_details,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("MLflow Run Information")

    st.code(
        "3066ba3864084525b71e4bc07a3c0777",
        language="text"
    )

    st.caption(
        "Values shown are from the previously recorded MLflow run. "
        "This section displays saved experiment information; "
        "it does not query MLflow live."
    )

    st.info(
        "The silhouette score is relatively low. "
        "The current five-customer dataset is a demonstration dataset, "
        "so the clustering results should be treated as exploratory."
    )


# ============================================================
# 13. FOOTER
# ============================================================

st.divider()

st.caption(
    "THAMES | Retail Customer Analytics & Recommendation Platform | "
    "Built with PySpark, Delta Lake, MLlib, MLflow and Streamlit"
)
