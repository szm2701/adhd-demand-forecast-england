# =========================================================
# ADHD Assessment Demand & Service Strain Dashboard (Streamlit)
# England, 2019–2024
#
# Purpose:
# - Communicate key findings from the capstone analysis notebook
# - Provide stakeholder-friendly visuals and interpretations
# - Support healthcare planning by summarising demand + service strain
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# STREAMLIT APP CONFIGURATION
# ---------------------------------------------------------

# Configure the Streamlit page (title shown in browser tab + wide layout)
st.set_page_config(
    page_title="ADHD Assessment Demand & Service Strain (England, 2019–2024)",
    layout="wide"
)


# SMALL VISUAL TWEAKS (professional polish)


# Tweak 1: Reduce top whitespace + soften KPI styling.
# Note: This is purely presentation. It does not affect analysis results.
st.markdown(
    """
    <style>
      .block-container { padding-top: 1.2rem; padding-bottom: 1.5rem; }
      h1 { margin-bottom: 0.2rem; }
      .stMetric { padding: 0.45rem 0.65rem; border-radius: 14px; }
      /* Make expander labels stand out slightly */
      div[data-testid="stExpander"] > details > summary { font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True
)

# Tweak 2: Use a clean Plotly template for consistent chart styling
# (No hard-coded colours; it just improves grid/axes readability)
PLOTLY_TEMPLATE = "plotly_white"

# Tweak 3: Make charts easier to read by default (hover aligned by x)
def apply_chart_layout(fig, title: str = None):
    """Standard chart layout settings for consistent visuals across pages."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        hovermode="x unified",
        margin=dict(l=10, r=10, t=50, b=10),
        title=title
    )
    return fig



# HEADER + SUBTITLE BANNER (stakeholder-friendly)


st.title("ADHD Assessment Demand & Service Strain (England, 2019–2024)")

# Subtitle banner (requested): helps assessors and stakeholders immediately understand purpose
st.info(
    "This dashboard summarises ADHD referral demand trends and service strain indicators in England (2019–2024), "
    "and presents an interpretable forecasting model to support service planning and capacity management."
)

st.caption("Data source: NHS England MHSDS ADHD statistics (processed in analysis notebook).")



# DATA LOADING (CACHED FOR PERFORMANCE)


@st.cache_data
def load_data():
    """
    Load processed datasets exported from the analysis notebook.

    Using st.cache_data prevents re-reading CSV files on each interaction,
    improving performance and keeping the app responsive.
    """
    ref_ts = pd.read_csv("data/processed/referrals_timeseries.csv")
    age_ts = pd.read_csv("data/processed/age_group_referrals.csv")
    strain_ts = pd.read_csv("data/processed/service_strain.csv")
    forecast_results = pd.read_csv("data/processed/forecast_results.csv")

    # Parse dates (UK day-first). NHS extracts often use DD/MM/YYYY.
    for df in (ref_ts, age_ts, strain_ts, forecast_results):
        if "period_end" in df.columns:
            df["period_end"] = pd.to_datetime(df["period_end"], dayfirst=True, errors="coerce")

    # Rename columns to be stakeholder-friendly (presentation only).
    # This keeps the underlying analysis pipeline intact while improving readability in the dashboard.
    ref_ts = ref_ts.rename(columns={
        "period_end": "Month",
        "total_referrals": "Total referrals"
    })

    age_ts = age_ts.rename(columns={
        "period_end": "Month",
        "age_group": "Age group",
        "value": "Referrals"
    })

    strain_ts = strain_ts.rename(columns={
        "period_end": "Month",
        "value_total": "Total referrals",
        "value_52plus": "Referrals waiting >52 weeks",
        "prop_52plus": "Proportion waiting >52 weeks"
    })

    forecast_results = forecast_results.rename(columns={
        "period_end": "Month",
        "total_referrals": "Actual referrals",
        "predicted_referrals": "Predicted referrals"
    })

    return ref_ts, age_ts, strain_ts, forecast_results


# Load datasets once (from cached function)
ref_ts, age_ts, strain_ts, forecast_results = load_data()



# HELPER FUNCTIONS


def safe_min_max_date(*dfs, date_col="Month"):
    """
    Find a global min/max date across multiple datasets.
    Used to power a single date filter that applies to all pages.
    """
    dates = []
    for df in dfs:
        if df is not None and not df.empty and date_col in df.columns:
            s = df[date_col].dropna()
            if not s.empty:
                dates.append(s.min())
                dates.append(s.max())
    if not dates:
        return None, None
    return min(dates), max(dates)


def apply_date_filter(df: pd.DataFrame, start, end, date_col="Month") -> pd.DataFrame:
    """
    Apply an inclusive date range filter to a dataframe.
    This supports stakeholder exploration without altering raw data.
    """
    if df is None or df.empty or date_col not in df.columns or start is None or end is None:
        return df
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    return df[(df[date_col] >= start) & (df[date_col] <= end)].copy()


def show_kpis(ref_df: pd.DataFrame, strain_df: pd.DataFrame) -> None:
    """
    Display headline KPIs aligned with the project plan:
    - Latest monthly referrals
    - Average monthly referrals (selected period)
    - Latest % waiting >52 weeks (service strain indicator, if available)
    """
    c1, c2, c3 = st.columns(3)

    # KPI 1: latest monthly referrals
    if ref_df is None or ref_df.empty or "Total referrals" not in ref_df.columns:
        c1.metric("Latest monthly referrals", "N/A")
    else:
        latest_referrals = float(ref_df.sort_values("Month").iloc[-1]["Total referrals"])
        c1.metric("Latest monthly referrals", f"{latest_referrals:,.0f}")

    # KPI 2: average monthly referrals across selected period
    if ref_df is None or ref_df.empty or "Total referrals" not in ref_df.columns:
        c2.metric("Average monthly referrals", "N/A")
    else:
        avg_referrals = float(ref_df["Total referrals"].mean())
        c2.metric("Average monthly referrals", f"{avg_referrals:,.0f}")

    # KPI 3: latest long-wait percentage (>52 weeks)
    if (
        strain_df is None
        or strain_df.empty
        or "Proportion waiting >52 weeks" not in strain_df.columns
    ):
        c3.metric("Waiting >52 weeks (latest)", "N/A")
    else:
        latest_prop = float(strain_df.sort_values("Month").iloc[-1]["Proportion waiting >52 weeks"])
        c3.metric("Waiting >52 weeks (latest)", f"{latest_prop * 100:.1f}%")



# SIDEBAR (NAVIGATION + FILTERS)


st.sidebar.title("Navigation")

# Sidebar page selection (matches your project dashboard structure)
page = st.sidebar.radio(
    "Go to:",
    ["Overview", "Age Analysis", "Service Strain", "Forecast"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

# Global date filter applied across all pages
min_date, max_date = safe_min_max_date(ref_ts, age_ts, strain_ts, forecast_results, date_col="Month")
if min_date is None or max_date is None:
    st.sidebar.warning("Date filter unavailable (Month column missing or empty).")
    start_date, end_date = None, None
else:
    # "Reset" requires a changing key to force Streamlit to refresh widget state
    if "filters_reset" not in st.session_state:
        st.session_state.filters_reset = 0

    start_date, end_date = st.sidebar.date_input(
        "Date range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date(),
        key=f"date_range_{st.session_state.filters_reset}",
        help="Applies to all pages."
    )

# Reset filters button (stakeholder-friendly)
if st.sidebar.button("Reset filters"):
    st.session_state.filters_reset += 1
    st.rerun()

# Apply date filter to each dataset (keeps logic consistent across pages)
ref_f = apply_date_filter(ref_ts, start_date, end_date)
age_f = apply_date_filter(age_ts, start_date, end_date)
strain_f = apply_date_filter(strain_ts, start_date, end_date)
forecast_f = apply_date_filter(forecast_results, start_date, end_date)



# PAGE 1 — OVERVIEW

if page == "Overview":

    st.subheader("Overview")

    # Subtitle banner (page-level): clarifies what the page does
    st.success(
        "Summary view: referral demand trend + headline KPIs for service planning."
    )

    st.write(
        "This page summarises ADHD referral demand over time and highlights headline indicators "
        "relevant to capacity planning and service monitoring."
    )

    # KPI row aligned with dashboard plan
    show_kpis(ref_f, strain_f)

    st.markdown("---")

    st.subheader("Total referrals over time")

    if ref_f is None or ref_f.empty or "Total referrals" not in ref_f.columns:
        st.warning("No referral time-series data available for the selected date range.")
    else:
        # Line chart: total referrals over time
        fig = px.line(
            ref_f.sort_values("Month"),
            x="Month",
            y="Total referrals",
            markers=True,
            labels={"Month": "Month", "Total referrals": "Monthly referrals"},
        )
        fig = apply_chart_layout(fig, title="Monthly ADHD referrals (open pathways)")

        st.plotly_chart(fig, use_container_width=True)

        # Stakeholder-friendly interpretation (non-technical)
        first_val = float(ref_f.sort_values("Month").iloc[0]["Total referrals"])
        last_val = float(ref_f.sort_values("Month").iloc[-1]["Total referrals"])
        abs_change = last_val - first_val
        pct_change = (abs_change / first_val * 100) if first_val else None

        st.markdown("### Interpretation")
        st.markdown(
            f"- Referrals reflect **monthly demand** entering ADHD assessment pathways.\n"
            f"- Over the selected period, demand changed by **{abs_change:,.0f} referrals**"
            + (f" (**{pct_change:.1f}%**)." if pct_change is not None else ".")
            + "\n- This provides a **top-level signal** to support capacity planning and backlog risk monitoring."
        )

    # Optional technical table (useful for assessors)
    with st.expander("Show data table (technical)"):
        st.dataframe(ref_f.sort_values("Month"), use_container_width=True)



# PAGE 2 — AGE ANALYSIS

elif page == "Age Analysis":

    st.subheader("Age Analysis")

    # Subtitle banner (page-level)
    st.info(
        "Age breakdown: compares referral demand across age groups and summarises ANOVA findings."
    )

    st.write(
        "This page compares referral demand across age groups and highlights which groups contribute most to overall demand."
    )

    if age_f is None or age_f.empty or "Age group" not in age_f.columns:
        st.warning("No age-group dataset available for the selected date range.")
    else:
        # Stakeholder control: select which age groups to display
        age_groups = sorted(age_f["Age group"].dropna().unique().tolist())
        selected_groups = st.multiselect(
            "Select age groups to display:",
            options=age_groups,
            default=age_groups
        )

        age_plot = age_f.copy()
        if selected_groups:
            age_plot = age_plot[age_plot["Age group"].isin(selected_groups)].copy()

        # Bar chart: average monthly referrals by age group (summary comparison)
        st.subheader("Average monthly referrals by age group")

        age_bar = (
            age_plot.groupby("Age group")["Referrals"]
            .mean()
            .reset_index()
            .sort_values("Referrals", ascending=False)
        )

        fig_bar = px.bar(
            age_bar,
            x="Age group",
            y="Referrals",
            labels={"Age group": "Age group", "Referrals": "Average monthly referrals"},
        )
        fig_bar = apply_chart_layout(fig_bar, title="Average monthly referrals by age group")
        st.plotly_chart(fig_bar, use_container_width=True)

        # Line chart: monthly trends by age group (pattern over time)
        st.subheader("Referral trends by age group over time")

        fig_line = px.line(
            age_plot.sort_values("Month"),
            x="Month",
            y="Referrals",
            color="Age group",
            markers=True,
            labels={"Month": "Month", "Referrals": "Monthly referrals", "Age group": "Age group"},
        )
        fig_line = apply_chart_layout(fig_line, title="Monthly referrals by age group")
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("### Interpretation")
        st.markdown(
            "- Referral demand is **not evenly distributed** across age groups.\n"
            "- The ANOVA test in the analysis notebook indicated **statistically significant differences** in mean referrals across age groups (p < 0.05).\n"
            "- This helps stakeholders identify which demographic groups may drive demand and require targeted capacity planning."
        )

        with st.expander("Show data table (technical)"):
            st.dataframe(age_plot.sort_values(["Age group", "Month"]), use_container_width=True)



# PAGE 3 — SERVICE STRAIN

elif page == "Service Strain":

    st.subheader("Service Strain")

    # Subtitle banner (page-level)
    st.warning(
        "Service pressure view: tracks long waits (>52 weeks) as an indicator of strain."
    )

    st.write(
        "This page monitors long-wait pressure using the share of referrals waiting longer than 52 weeks."
    )

    if strain_f is None or strain_f.empty:
        st.warning("No service strain dataset available for the selected date range.")
    elif "Proportion waiting >52 weeks" not in strain_f.columns:
        st.error("Expected column 'Proportion waiting >52 weeks' not found in service_strain.csv.")
    else:
        # Convert proportion into a percentage for stakeholder readability
        strain_plot = strain_f.sort_values("Month").copy()
        strain_plot["% waiting >52 weeks"] = strain_plot["Proportion waiting >52 weeks"] * 100

        st.subheader("Percent of referrals waiting >52 weeks over time")

        fig = px.line(
            strain_plot,
            x="Month",
            y="% waiting >52 weeks",
            markers=True,
            labels={"Month": "Month", "% waiting >52 weeks": "% waiting >52 weeks"},
        )
        fig = apply_chart_layout(fig, title="Long-wait share over time (>52 weeks)")
        st.plotly_chart(fig, use_container_width=True)

        # Plain English interpretation tied to your hypothesis result (H3)
        st.markdown("### Interpretation")
        st.markdown(
            "- This metric indicates **long-wait pressure** (waiting over one year).\n"
            "- Theregression test for trend was **not statistically significant** (p = 0.561), suggesting no clear linear increase in the long-wait share across the period.\n"
            "- Even without a significant trend, **high absolute levels** can still indicate operational risk and patient impact."
        )

        with st.expander("Show data table (technical)"):
            st.dataframe(strain_plot, use_container_width=True)



# PAGE 4 — FORECAST

elif page == "Forecast":

    st.subheader("Forecast")

    # Subtitle banner (page-level)
    st.success(
        "Forecast view: compares actual vs predicted referrals and shows model accuracy (test set)."
    )

    st.write(
        "This page compares observed referrals to model predictions in the test period."
    )

    # Forecast evaluation metrics from your analysis notebook (user-provided)
    # MAE = Mean Absolute Error
    # RMSE = Root Mean Squared Error
    # MAPE = Mean Absolute Percentage Error
    MAE_VALUE = 65648.78
    RMSE_VALUE = 67461.28
    MAPE_VALUE = 25.16

    # KPI-like metric cards for model performance (stakeholder-friendly)
    st.subheader("Model accuracy (test set)")
    c1, c2, c3 = st.columns(3)
    c1.metric("MAE", f"{MAE_VALUE:,.0f}")
    c2.metric("RMSE", f"{RMSE_VALUE:,.0f}")
    c3.metric("MAPE", f"{MAPE_VALUE:.1f}%")

    # Validate expected columns before plotting
    expected_cols = {"Actual referrals", "Predicted referrals"}
    if forecast_f is None or forecast_f.empty:
        st.warning("No forecast dataset available for the selected date range.")
    elif not expected_cols.issubset(set(forecast_f.columns)):
        st.warning(
            "Could not find expected columns for forecast plot. "
            "Expected: 'Actual referrals' and 'Predicted referrals'. "
            f"Found: {list(forecast_f.columns)}"
        )
    else:
        plot_df = forecast_f.sort_values("Month")

        st.subheader("Actual vs predicted referrals (test period)")
        fig = px.line(
            plot_df,
            x="Month",
            y=["Actual referrals", "Predicted referrals"],
            markers=True,
            labels={"Month": "Month", "value": "Referrals"},
        )
        fig = apply_chart_layout(fig, title="Actual vs predicted monthly referrals")
        st.plotly_chart(fig, use_container_width=True)

        # Interpretation uses your exact MAPE value (rounded for readability)
        st.markdown("### Interpretation")
        st.markdown(
            "- The model captures the **overall direction of change**, but may **underestimate** demand in later months.\n"
            f"- Average prediction error is **{MAPE_VALUE:.1f}% (MAPE)**, which supports **trend planning** rather than precise month-by-month targets.\n"
            "- A simple linear model was selected to maintain **transparency and interpretability** for stakeholders."
        )

        with st.expander("Show data table (technical)"):
            st.dataframe(plot_df, use_container_width=True)



# FOOTER


st.markdown("---")
st.caption("Dashboard built for capstone assessment: Analysis + Hypothesis Testing + Forecasting + Visual Communication.")