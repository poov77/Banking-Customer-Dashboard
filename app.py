from pathlib import Path

import pandas as pd
import streamlit as st


DATA_FILE = Path(__file__).with_name("American Banking Data - Fully_Cleaned_Data.csv")


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_FILE, index_col=0)
    data["Date Joined"] = pd.to_datetime(data["Date Joined"], errors="coerce")
    data["Age"] = pd.to_numeric(data["Age"], errors="coerce")
    data["Balance"] = pd.to_numeric(data["Balance"], errors="coerce")
    return data


def money(value: float) -> str:
    return f"${value:,.0f}"


st.set_page_config(
    page_title="Banking Customer Dashboard",
    page_icon=":bank:",
    layout="wide",
)

st.title("Banking Customer Dashboard")
st.caption("Customer balances, loan status, and segmentation from the cleaned banking dataset.")

df = load_data()

with st.sidebar:
    st.header("Filters")

    states = st.multiselect(
        "State",
        options=sorted(df["State"].dropna().unique()),
        default=sorted(df["State"].dropna().unique()),
    )
    jobs = st.multiselect(
        "Job classification",
        options=sorted(df["Job Classification"].dropna().unique()),
        default=sorted(df["Job Classification"].dropna().unique()),
    )
    genders = st.multiselect(
        "Gender",
        options=sorted(df["Gender"].dropna().unique()),
        default=sorted(df["Gender"].dropna().unique()),
    )
    age_min = int(df["Age"].min())
    age_max = int(df["Age"].max())
    age_range = st.slider("Age range", age_min, age_max, (age_min, age_max))

filtered = df[
    df["State"].isin(states)
    & df["Job Classification"].isin(jobs)
    & df["Gender"].isin(genders)
    & df["Age"].between(age_range[0], age_range[1])
].copy()

customers = len(filtered)
avg_balance = filtered["Balance"].mean() if customers else 0
total_balance = filtered["Balance"].sum() if customers else 0
default_rate = (
    (filtered["Loan Default"].str.lower() == "yes").mean() * 100 if customers else 0
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", f"{customers:,}")
col2.metric("Average balance", money(avg_balance))
col3.metric("Total balance", money(total_balance))
col4.metric("Loan default rate", f"{default_rate:.1f}%")

tab_overview, tab_segments, tab_data = st.tabs(["Overview", "Segments", "Data"])

with tab_overview:
    left, right = st.columns(2)

    with left:
        st.subheader("Customers by state")
        state_counts = filtered["State"].value_counts().sort_values(ascending=False)
        st.bar_chart(state_counts)

    with right:
        st.subheader("Average balance by job")
        balance_by_job = (
            filtered.groupby("Job Classification")["Balance"].mean().sort_values()
        )
        st.bar_chart(balance_by_job)

    st.subheader("Monthly customers joined")
    joined = (
        filtered.dropna(subset=["Date Joined"])
        .set_index("Date Joined")
        .resample("ME")["Customer Code"]
        .count()
    )
    st.line_chart(joined)

with tab_segments:
    left, right = st.columns(2)

    with left:
        st.subheader("Loan default by education")
        default_by_education = pd.crosstab(
            filtered["education"], filtered["Loan Default"], normalize="index"
        )
        st.dataframe(default_by_education.style.format("{:.1%}"), use_container_width=True)

    with right:
        st.subheader("House loan and other loan")
        loan_mix = pd.crosstab(filtered["House Loan"], filtered["Other Loan"])
        st.dataframe(loan_mix, use_container_width=True)

    st.subheader("Top balances")
    top_balances = filtered.sort_values("Balance", ascending=False).head(20)
    st.dataframe(
        top_balances[
            [
                "Customer Code",
                "Full Name",
                "State",
                "Job Classification",
                "Age",
                "Balance",
                "Loan Default",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with tab_data:
    st.subheader("Filtered records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered CSV",
        data=csv,
        file_name="filtered_banking_customers.csv",
        mime="text/csv",
    )
