import requests
import statsmodels.api as sm
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
from sqlalchemy import create_engine
engine = create_engine('sqlite:///Docs/Data/PoliticsandDataSci.db', echo=False, isolation_level="AUTOCOMMIT")

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
    events_data = pd.read_sql_table("Biden Events",con=engine)
    vertical_lines = alt.Chart(events_data).mark_rule(color='blue', strokeWidth=1.5,opacity=0.5).encode(
    x='Date:T',
    tooltip=['Event:N'],
    )
    loess_smoothed = df_long.groupby(['Opinion', 'startDate']).mean().reset_index()
    loess_smoothed['smoothed'] = loess_smoothed.groupby('Opinion')['Percentage'].transform(lambda x: sm.nonparametric.lowess(x, range(len(x)), frac=0.3)[:, 1])

    # Altair Chart for smoothed lines
    chart_lines = alt.Chart(loess_smoothed).mark_line(color='black').encode(
        x=alt.X('startDate:T', axis=alt.Axis(tickCount='month', format='%b %Y', labelAngle=-90), title='Date'),
        y=alt.Y('smoothed:Q', axis=alt.Axis(title='Percentage')),
        detail='Opinion:N'
    )
    combined_chart = alt.layer(chart_points, chart_lines, vertical_lines).interactive()


    return combined_chart

def plot_interactive(col_x,col_y):
    with engine.connect() as conn:
        pass
    df = pd.read_sql_table("Interactive Data",con=engine)
    chart = alt.Chart(df).mark_circle().encode(
        x=col_x,
        y=col_y,
        tooltip=['Year', col_x, col_y]
    )
    regressionline = chart.transform_regression(col_x, col_y).mark_line()
    return (chart+regressionline)

def createpopagainstincome():
    merged_population_income = pd.read_sql("State Data",con=engine)
    merged_population_income['Income_Integer'] = merged_population_income['Median Household income'].replace('[\$,]', '', regex=True).astype(int)
    merged_population_income['Population/SqMi'] = pd.to_numeric(merged_population_income['Population/SqMi'], errors='coerce')
    scatter = alt.Chart(merged_population_income).mark_circle().encode(
    y= alt.Y('Income_Integer',title="Median Household Income"),
    x='Population/SqMi',
    tooltip=['State:N', 'Income_Integer:Q', 'Population/SqMi:Q']
    )
    regressionline = scatter.transform_regression('Income_Integer', 'Population/SqMi').mark_line()
    combined_chart = (scatter + regressionline)
    return combined_chart.interactive()
def createcrimeratesbetweenUKcities():
    crimeratesdf = pd.read_sql("UK crime rates",con=engine)
    Crimegraph = alt.Chart(crimeratesdf).mark_line().encode(
    x=alt.X('Month:O', title='Month'),  
    color=alt.Color('city:N', title='City'), 
    y=alt.Y('crime_rate:Q', title='Crime Rates'),
    tooltip=['Month:O', 'city:N', 'crime_rate:Q'] 
    ).properties(
        width=500, 
        height=300,
        title='Crime Rates in Cities (2021)'
    ).transform_fold(  
        fold=['London', 'Manchester', 'Newcastle', 'Portsmouth' ],
        as_=['city', 'crime_rate']
    )
    return Crimegraph

def createlondoncrimebycategory():
    crimecategorylondon2022 = pd.read_sql("London crime categories",con=engine)
    chart = alt.Chart(crimecategorylondon2022).mark_bar().encode(
    x='count:Q',
    y=alt.Y('category:N', sort='-x'),
    tooltip=['category:N', 'count:Q'] 
    ).properties(
    title='Crime by Category in London 2021'  # Add a title to the chart
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
var_x = st.selectbox("Select an X variable:", ['Average Global Gini', 'UK GDP Per Capita (US $)', 'UK GDP Growth Rate',	'USA GDP Per Capita (US $)', 'US GDP Growth Rate','Persons Below Poverty (US)','Percent Below Poverty (US)', 'Voter Turnout in UK'])
var_y = st.selectbox("Select a Y variable:", ['Average Global Gini', 'UK GDP Per Capita (US $)', 'UK GDP Growth Rate',	'USA GDP Per Capita (US $)', 'US GDP Growth Rate','Persons Below Poverty (US)','Percent Below Poverty (US)' ,'Voter Turnout in UK'])
st.altair_chart(plot_interactive(var_x,var_y))




st.markdown("## Median Household income (2019-2021) against population density")
st.altair_chart(createpopagainstincome())
st.markdown("# UK data")
st.markdown("## Crime rates over 2021 between UK cities")
st.altair_chart(createcrimeratesbetweenUKcities())
st.markdown("## Crime by category, London 2022")
st.altair_chart(createlondoncrimebycategory())




