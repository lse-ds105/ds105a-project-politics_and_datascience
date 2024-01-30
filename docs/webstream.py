import requests
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

def createpopulationgeo():
    from vega_datasets import data
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///Data/PoliticsandDataSci.db', echo=False, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        pass
    us_population_df = pd.read_sql_table("State Data",con=engine)
    states_geo = alt.topo_feature(data.us_10m.url, 'states')
    chart = alt.Chart(states_geo).mark_geoshape().encode(
        color= alt.Color('Population:Q',scale=alt.Scale(scheme='greens'), title='Population'),
        tooltip=['State:N', 'Population:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(us_population_df, 'id', ['Population','State'])
    ).project(
        type='albersUsa'
    ).properties(
        width=500,
        height=300,
        title='Population by State'
    )
    return chart

def createpopulationdensitygeo():
    from vega_datasets import data
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///Data/PoliticsandDataSci.db', echo=False, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        pass
    us_population_df = pd.read_sql_table("State Data",con=engine)
    states_geo = alt.topo_feature(data.us_10m.url, 'states')
    chart = alt.Chart(states_geo).mark_geoshape().encode(
        color=alt.Color('Population/SqMi:Q',scale=alt.Scale(scheme='blues'), title='Population/Sq/Mi'),
        tooltip=['State:N', 'Population/SqMi:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(us_population_df, 'id', ['Population/SqMi','State'])
    ).project(
        type='albersUsa'
    ).properties(
        width=500,
        height=300,
        title='Population Density by State'
    )
    return chart


st.altair_chart(createpopulationgeo())
st.altair_chart(createpopulationdensitygeo())
