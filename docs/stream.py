import requests
import pandas as pd
import streamlit as st
import altair as alt

def createpopulationbar():
    jsonlist = requests.get("https://api.census.gov/data/2019/pep/charagegroups?get=NAME,POP&HISP=2&for=state:*").json()
    states =[]
    print(jsonlist[3])
    populations =[]
    for list in jsonlist:
        states.append(list[0])
        populations.append(list[1])
    data = {"State":states,"Population":populations
    }
    us_population_df=pd.DataFrame(data)
    us_population_df = us_population_df.iloc[1:]
    us_population_df["Population"]=pd.to_numeric(us_population_df["Population"])
    chart = alt.Chart(us_population_df).mark_bar().encode(
        x="State",
        y="Population"
    ).interactive()
    return chart
def createpopulationgeo():
    from vega_datasets import data
    us_population_df = pd.read_csv("./Population_And_Median_Income")
    states_geo = alt.topo_feature(data.us_10m.url, 'states')
    chart = alt.Chart(states_geo).mark_geoshape().encode(
        color='Population:Q',
        tooltip=['State:N', 'Population:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(us_population_df, 'id', ['Population','State'])
    ).project(
        type='albersUsa'
    ).properties(
        width=500,
        height=300
    )
    return chart
st.title('Population by State')
st.altair_chart(createpopulationbar())
st.altair_chart(createpopulationgeo())

