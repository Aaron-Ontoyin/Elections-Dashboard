import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout="wide")

if "pres_data" not in ss:
    ss.pres_data = pd.read_excel("data/combined_pres.xlsx")
if "parl_data" not in ss:
    ss.parl_data = pd.read_excel("data/combined_parl.xlsx")


def plot_pie_chart(year):
    year_data = data[data["YEAR"] == year]
    year_data = year_data.drop(
        columns=["YEAR", "TOTAL VOTES", "REG VOTERS", "PS NAME", "PS CODE"]
    )
    year_data = year_data.apply(pd.to_numeric, errors="coerce")
    year_data_sum = year_data.sum()
    fig = px.pie(
        values=year_data_sum.values,
        names=year_data_sum.index,
        title=f"Party Distribution for Year {year}",
        hole=0.3,
        labels={"names": "party", "values": "votes"},
    )
    st.plotly_chart(fig)


def plot_bar_chart(years):
    years_data = data[data["YEAR"].isin(years)]
    years_data = years_data.apply(pd.to_numeric, errors="coerce")
    years_data = years_data.drop(
        columns=["TOTAL VOTES", "REG VOTERS", "PS NAME", "PS CODE"]
    )
    years_data_grp = years_data.groupby("YEAR").sum().reset_index()
    fig = go.Figure()
    for party in years_data.columns:
        if party in ["YEAR"]:
            continue
        fig.add_trace(
            go.Bar(
                x=years_data_grp["YEAR"],
                y=years_data_grp[party],
                name=party,
            )
        )
    fig.update_layout(
        barmode="group",
        title=f"Party Distribution for Years {', '.join(map(str, years))}",
        xaxis_title="Year",
        yaxis_title="Votes",
    )
    st.plotly_chart(fig)


def plot_top_n_stations_by_party(party, years, top_n, method):
    pdata = data.copy(True)
    pdata = pdata[pdata["YEAR"].isin(years)]
    pdata = pdata[["PS CODE", "PS NAME", "TOTAL VOTES", party]]
    pdata = pdata.groupby("PS CODE").sum().reset_index()
    y_col = party
    if method == "Local Fraction":
        pdata["local_fraction"] = pdata[party] / pdata["TOTAL VOTES"]
        pdata = pdata.sort_values("local_fraction", ascending=False).head(top_n)
        y_col = "local_fraction"
    elif method == "Global Fraction":
        pdata["global_fraction"] = pdata[party] / pdata["TOTAL VOTES"].sum()
        pdata = pdata.sort_values("global_fraction", ascending=False).head(top_n)
        y_col = "global_fraction"
    elif method == "Number":
        pdata = pdata.sort_values(party, ascending=False).head(top_n)

    if pdata.empty:
        st.info(f"No data available for selected {party} and {years}")
        st.stop()

    fig = px.bar(
        pdata,
        x="PS NAME",
        y=y_col,
        title=f"Top {top_n} Stations for {party} in {str(years)[1:-1]} ({method})",
    )
    st.plotly_chart(fig)


def plot_top_n_stations_by_voter_change(top_n, from_year, to_year, change_by):
    st.warning("Not Implemented due to changes in pooling stations names over years!")


st.title("Election Data Analysis")

data = st.radio(
    "Choose Data", ["Presidential", "Parliamentary"], horizontal=True, label_visibility="hidden"
)
data = ss.pres_data if data == "Presidential" else ss.parl_data


VDAL, VDPYPP, TNSPP, TNSVC = st.tabs(
    [
        "Vote Dist. (All Parties)",
        "Vote Dist. Per Yr (Per Party)",
        "Top N Stations (Per Party)",
        "Top N Stations by Voter Change",
    ]
)

with VDAL:
    with st.columns(5)[-1]:
        year = st.selectbox("Select Year", data["YEAR"].unique())
    plot_pie_chart(year)

with VDPYPP:
    with st.columns(2)[-1]:
        st.write("Select Years")
        available_years = data["YEAR"].unique()
        year_cols = st.columns(len(available_years))
        for col_idx, year in enumerate(available_years):
            year_cols[col_idx].checkbox(str(year), value=True, key=str(year))

    years = [int(year) for year in available_years if st.session_state[year]]
    if not years:
        st.info("Please select at least one year")
        st.stop()

    plot_bar_chart(years)


with TNSPP:
    party_col, years_col, n_col, method_col = st.columns(4)
    party = party_col.selectbox(
        "Select Party",
        set(data.columns).difference(
            set(["YEAR", "TOTAL VOTES", "REG VOTERS", "PS NAME", "PS CODE", "REJECTED"])
        ),
    )
    years = years_col.multiselect("Select Years", data["YEAR"].unique())
    n = n_col.number_input(
        "Select N", min_value=1, max_value=data["PS CODE"].nunique(), value=5
    )
    method = method_col.selectbox(
        "Select Method",
        ["Local Fraction", "Global Fraction", "Number"],
        help="""
        Local Fraction: Top N stations with highest fraction of votes for the party in those respective stations;
        Global Fraction: Top N stations with highest fraction of votes for the party across all stations;
        Number: Top N stations with highest number of votes for the party
        """,
    )

    if not years:
        st.info("Please select at least one year")
    else:
        plot_top_n_stations_by_party(party, years, n, method)


with TNSVC:
    n = st.slider("Select N", min_value=1, max_value=data["PS CODE"].nunique(), value=5)
    from_year_col, to_year_col, change_by_col = st.columns(3)
    from_year = from_year_col.selectbox("From Year", data["YEAR"].unique())
    to_year = to_year_col.selectbox("To Year", data["YEAR"].unique())
    change_by = change_by_col.selectbox(
        "Change in",
        ["REG VOTERS"]
        + list(
            set(data.columns).difference(
                set(
                    [
                        "YEAR",
                        "TOTAL VOTES",
                        "REG VOTERS",
                        "PS NAME",
                        "PS CODE",
                        "REJECTED",
                    ]
                )
            )
        ),
    )
    if from_year == to_year:
        st.info("Please select different years")
        st.stop()
    plot_top_n_stations_by_voter_change(n, from_year, to_year, change_by)
