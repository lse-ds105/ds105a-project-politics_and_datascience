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
st.title('Political Data Science project')
st.markdown("* Alex Faith (alexgabriellafaith) | BSc in Politics and Data Science")
st.markdown("* Ayşe Yalçın (ayseyalcin1) | BSc in Politics and Data Science")
st.markdown("* Maddox Leigh (maddoxleigh) | BSc in Politics and Data Science")
st.write("This project aims to create easy to interpret, interactive graphs showing interesting correlations we found from various government census data and APIs")
st.write("It is important to note that any correlations shown do not implicitly imply that a causation exists between the two variables!")
st.markdown("# US data")
st.markdown("## Population vs Population Density by State")
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(createpopulationgeo())

with col2:
    st.altair_chart(createpopulationdensitygeo())

#st.markdown("## Median Household income (2019-2021) against population density")
#st.altair_chart(createpopagainstincome())
#st.markdown("# UK data")
#st.markdown("## Crime rates over 2021 between UK cities")
#st.altair_chart(createcrimeratesbetweenUKcities())
#st.markdown("## Crime by category, London 2022")
#st.altair_chart(createlondoncrimebycategory())




#st.altair_chart(createpopulationgeo())
#st.altair_chart(createpopulationdensitygeo())
