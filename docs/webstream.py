import requests
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
from sqlalchemy import create_engine
engine = create_engine('sqlite:///Data/PoliticsandDataSci.db', echo=False, isolation_level="AUTOCOMMIT")

def createpopulationgeo():
    
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
def createbidenpollchart():
    with engine.connect() as conn:
        pass
    Biden_dataframe = pd.read_sql_table("Biden polls",con=engine)
    df_long= pd.melt(Biden_dataframe, id_vars=['startDate'], value_vars=['approve', 'disapprove'],
                  var_name='Opinion', value_name='Percentage')
    chart_points = alt.Chart(df_long).mark_point(size=50, opacity=0.25, filled=True).encode(
        x=alt.X('startDate:T', axis=alt.Axis(tickCount='month', format='%b %Y', labelAngle=-90)),
        y=alt.Y('Percentage:Q', axis=alt.Axis(title='Percentage')),
        color=alt.Color('Opinion:N', scale=alt.Scale(domain=['approve', 'disapprove'], range=['green', 'red']), legend=alt.Legend(title='Opinion')),
    ).properties(
        title='Biden Approval Rates Overtime',
        width=600,
        height=400
    )
    return chart_points

def plot_interactive(col_x,col_y):
    with engine.connect() as conn:
        pass
    df = pd.read_sql_table("Interactive Data",con=engine)
    chart = alt.Chart(df).mark_circle().encode(
        x=col_x,
        y=col_y,
        tooltip=['Year', col_x, col_y]
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

st.altair_chart(createbidenpollchart())

st.markdown("# Interactive Graph")
var_x = st.selectbox("Select an X variable:", ['Average Global Gini', 'UK GDP Per Capita (US $)', 'UK GDP Growth Rate',	'USA GDP Per Capita (US $)', 'US GDP Growth Rate'])
var_y = st.selectbox("Select a Y variable:", ['Average Global Gini', 'UK GDP Per Capita (US $)', 'UK GDP Growth Rate',	'USA GDP Per Capita (US $)', 'US GDP Growth Rate'])
st.altair_chart(plot_interactive(var_x,var_y))




#st.markdown("## Median Household income (2019-2021) against population density")
#st.altair_chart(createpopagainstincome())
#st.markdown("# UK data")
#st.markdown("## Crime rates over 2021 between UK cities")
#st.altair_chart(createcrimeratesbetweenUKcities())
#st.markdown("## Crime by category, London 2022")
#st.altair_chart(createlondoncrimebycategory())




#st.altair_chart(createpopulationgeo())
#st.altair_chart(createpopulationdensitygeo())
