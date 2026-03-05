import streamlit as st
import pandas as pd
import plotly.express as px


# App config (page title, layout)

st.set_page_config(
    page_title="ADHD Referral Demand & Service Strain Dashboard",
    layout="wide"
)


# Data loading (cached for performance)

@st.cache_data
def load_data():
    """
    Load processed datasets exported from the analysis notebook.
    Using st.cache_data prevents re-loading on every interaction.
    """
    ref_ts = pd.read_csv("data/processed/referrals_timeseries.csv")
    age_ts = pd.read_csv("data/processed/age_group_referrals.csv")
    strain_ts = pd.read_csv("data/processed/service_strain.csv")
    forecast_results = pd.read_csv("data/processed/forecast_results.csv")

    # Ensure date columns parse correctly (UK format DD/MM/YYYY)
    if "period_end" in ref_ts.columns:
        ref_ts["period_end"] = pd.to_datetime(ref_ts["period_end"], dayfirst=True)

    if "period_end" in age_ts.columns:
        age_ts["period_end"] = pd.to_datetime(age_ts["period_end"], dayfirst=True)

    if "period_end" in strain_ts.columns:
        strain_ts["period_end"] = pd.to_datetime(strain_ts["period_end"], dayfirst=True)

    if "period_end" in forecast_results.columns:
        forecast_results["period_end"] = pd.to_datetime(forecast_results["period_end"], dayfirst=True)

        return ref_ts, age_ts, strain_ts, forecast_results 

ref_ts, age_ts, strain_ts, forecast_results = load_data()


# Sidebar navigation (matches the 4 dashboard pages in plan)

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Overview", "Age Analysis", "Service Strain", "Forecast"]
)

st.title("ADHD Referral Demand & Service Strain (England, 2019–2024)")


# Helper: KPI card row

def show_kpis(ref_df):
    """
    Display headline metrics for the Overview page.
    """
    latest = ref_df.sort_values("period_end").iloc[-1]
    first = ref_df.sort_values("period_end").iloc[0]

    latest_referrals = latest["total_referrals"]
    start_referrals = first["total_referrals"]
    abs_change = latest_referrals - start_referrals
    pct_change = (abs_change / start_referrals) * 100 if start_referrals != 0 else None

    c1, c2, c3 = st.columns(3)
    c1.metric("Latest Monthly Referrals", f"{latest_referrals:,.0f}")
    c2.metric("Change Since Start", f"{abs_change:,.0f}")
    c3.metric("Percentage Change", f"{pct_change:,.1f}%" if pct_change is not None else "N/A")



# PAGE 1 — OVERVIEW

if page == "Overview":
    st.subheader("Overview")
    st.write(
        "This page summarises national ADHD referral demand over time and highlights key headline metrics."
    )

    show_kpis(ref_ts)

    st.markdown("---")

    st.subheader("Total Referrals Over Time")
    fig = px.line(
        ref_ts.sort_values("period_end"),
        x="period_end",
        y="total_referrals",
        labels={"period_end": "Month", "total_referrals": "Total Referrals"},
    )
    st.plotly_chart(fig, use_container_width=True)

    # Optional: show raw data
    with st.expander("Show data table"):
        st.dataframe(ref_ts.sort_values("period_end"))



# PAGE 2 — AGE ANALYSIS

elif page == "Age Analysis":
    st.subheader("Age Analysis")
    st.write(
        "This page compares referral counts across age groups to explore differences in demand profiles."
    )

    # age_ts has columns like: period_end, age_group, value/referrals
    # Adjust the y-column name below if needed.
    possible_y_cols = [c for c in age_ts.columns if c.lower() in ["value", "referrals", "total_referrals"]]
    y_col = possible_y_cols[0] if possible_y_cols else age_ts.columns[-1]

    age_groups = sorted(age_ts["age_group"].dropna().unique().tolist())
    selected_groups = st.multiselect(
        "Select age groups to display:",
        options=age_groups,
        default=age_groups
    )

    filtered = age_ts[age_ts["age_group"].isin(selected_groups)].sort_values("period_end")

    fig = px.line(
        filtered,
        x="period_end",
        y=y_col,
        color="age_group",
        labels={"period_end": "Month", y_col: "Referrals", "age_group": "Age Group"},
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show data table"):
        st.dataframe(filtered)



# PAGE 3 — SERVICE STRAIN

elif page == "Service Strain":
    st.subheader("Service Strain")
    st.write(
        "This page visualises the proportion of referrals waiting more than 52 weeks as an indicator of system strain."
    )

    # Expecting strain_ts to include: period_end, prop_52plus (and maybe totals)
    if "prop_52plus" not in strain_ts.columns:
        st.error("Expected column 'prop_52plus' not found in service_strain.csv.")
    else:
        fig = px.line(
            strain_ts.sort_values("period_end"),
            x="period_end",
            y="prop_52plus",
            labels={"period_end": "Month", "prop_52plus": "Proportion Waiting >52 Weeks"},
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Show data table"):
            st.dataframe(strain_ts.sort_values("period_end"))



# PAGE 4 — FORECAST

elif page == "Forecast":
    st.subheader("Forecast")
    st.write(
        "This page displays model outputs and compares actual vs predicted referrals for the test period."
    )

    # Expecting forecast_results to include actual and predicted columns
    
    expected_cols = {"total_referrals", "predicted_referrals"}
    if not expected_cols.issubset(set(forecast_results.columns)):
        st.warning(
            "Could not find expected columns for forecast plot. "
            "Expected: 'total_referrals' and 'predicted_referrals'. "
            f"Found: {list(forecast_results.columns)}"
        )
    else:
        plot_df = forecast_results.sort_values("period_end")

        fig = px.line(
            plot_df,
            x="period_end",
            y=["total_referrals", "predicted_referrals"],
            labels={"period_end": "Month", "value": "Referrals"},
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Show data table"):
            st.dataframe(plot_df)



# Footer

st.markdown("---")
st.caption("Data source: NHS England MHSDS ADHD statistics (processed in analysis notebook).")