# Importing libraries

import statsmodels.api as sm
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
from sqlalchemy import create_engine

# Creating engine used to access our database
engine = create_engine('sqlite:///Docs/Data/PoliticsandDataSci.db', echo=False, isolation_level="AUTOCOMMIT")

# Generic method for plotting line graph from data in interactive table
def plot_line_graph(y_column):
    
    # Opening connection to database
    with engine.connect() as conn:
        pass
    # reading sql table to dataframe
    dataframe = pd.read_sql_table("Interactive Data",con=engine)
    custom_domain = [year for year in range(1960, 2025)]
    chart = alt.Chart(dataframe).mark_line(
        color='red'
    ).encode(
        x=alt.X('Year:O', title='Year',scale=alt.Scale(domain=custom_domain)),
        y=alt.Y(f'{y_column}:Q', title=f'{y_column}'),
        tooltip=['Year:O', f'{y_column}:Q']
    ).properties(
        title=f'{y_column} Over Years',
        width = 500
    ).interactive()
    return chart


def createpopulationgeo():
    # opening connection to database
    with engine.connect() as conn:
        pass
    # reading table to dataframe
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
        width=375,
        height=225,
        title='Population by State'
    )
    return chart

def createpopulationdensitygeo():
    # opening connection to database
    with engine.connect() as conn:
        pass
    # reading table to dataframe
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
        width=365,
        height=225,
        title='Population Density by State'
    )
    return chart

def createbidenpollchart():
    # opening connection to database
    with engine.connect() as conn:
        pass
    # reading biden polls table to dataframe
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
    # reading events table to dataframe
    events_data = pd.read_sql_table("Biden Events",con=engine)
    vertical_lines = alt.Chart(events_data).mark_rule(color='blue', strokeWidth=1.5,opacity=0.5).encode(
    x='Date:T',
    tooltip=['Event:N'],
    )
    # creating smooth lines for graph
    loess_smoothed = df_long.groupby(['Opinion', 'startDate']).mean().reset_index()
    loess_smoothed['smoothed'] = loess_smoothed.groupby('Opinion')['Percentage'].transform(lambda x: sm.nonparametric.lowess(x, range(len(x)), frac=0.3)[:, 1])

    # Altair Chart for smoothed lines
    chart_lines = alt.Chart(loess_smoothed).mark_line(color='black').encode(
        x=alt.X('startDate:T', axis=alt.Axis(tickCount='month', format='%b %Y', labelAngle=-90), title='Date'),
        y=alt.Y('smoothed:Q', axis=alt.Axis(title='Percentage')),
        detail='Opinion:N'
    )
    # combining event, point and line graphs together
    combined_chart = alt.layer(chart_points, chart_lines, vertical_lines).interactive()
    return combined_chart

# generic method to plot regression graph from user input
def plot_interactive(col_x,col_y):
    with engine.connect() as conn:
        pass
    df = pd.read_sql_table("Interactive Data",con=engine)
    chart = alt.Chart(df).mark_circle().encode(
        x=col_x,
        y=col_y,
        tooltip=['Year', col_x, col_y]
    )
    # combining scatter graph with regression line
    regressionline = chart.transform_regression(col_x, col_y).mark_line()
    return (chart+regressionline)

def createpopagainstincome():
    # reading table to dataframe
    merged_population_income = pd.read_sql("State Data",con=engine)
    merged_population_income['Income_Integer'] = merged_population_income['Median Household income'].replace('[\$,]', '', regex=True).astype(int)
    merged_population_income['Population/SqMi'] = pd.to_numeric(merged_population_income['Population/SqMi'], errors='coerce')
    scatter = alt.Chart(merged_population_income).mark_circle().encode(
    y= alt.Y('Income_Integer',title="Median Household Income"),
    x='Population/SqMi',
    tooltip=['State:N', 'Income_Integer:Q', 'Population/SqMi:Q']
    )
    regressionline = scatter.transform_regression('Income_Integer', 'Population/SqMi').mark_line()
    # combining scatter graph with regression line
    combined_chart = (scatter + regressionline)
    return combined_chart.interactive()

def createcrimeratesbetweenUKcities():
    # reading table to dataframe
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

def create_pie_chart(year,df):
    # creating data frame for single year
    
    data_year = df.reset_index()[['Region', year]].rename(columns={year: 'Population'})
    chart = alt.Chart(data_year).mark_arc().encode(
        theta=alt.Theta(field="Population", type="quantitative"),
        color=alt.Color(field="Region", type="nominal"),
        tooltip=['Region', 'Population']
    ).properties(
        title=f"Population Distribution in {year}",
        width=200,
        height=200
    )
    # returns only the chart for a single year
    return chart

# this method calls the create_pie_chart() method three times to return 3 pie charts for each year, showing the change over time
def create_pop_charts():
    region_pop_df = pd.read_sql("Global population",con=engine)
    chart_2050 = create_pie_chart('2050',region_pop_df)
    chart_2075 = create_pie_chart('2075',region_pop_df)
    chart_2100 = create_pie_chart('2100',region_pop_df)
    return chart_2050 | chart_2075 | chart_2100


def create_gloabl_gini_average():
    # reading sql table to dataframe
    gini_df = pd.read_sql("Global gini",con=engine)
    scatter = alt.Chart(gini_df).mark_circle().encode(
    y= alt.Y('GlobalGini',title = "Average Global Gini"),
    x='Year',
    )
    regression = scatter.transform_regression('Year', 'GlobalGini').mark_line()
    # combining scatter and regression graphs
    combined_chart =regression+scatter
    return combined_chart

#### comments up to here

def show_home():
    st.title('Political Data Science project')
    st.markdown("* Alex Faith (alexgabriellafaith) | BSc in Politics and Data Science")
    st.markdown("* Ayşe Yalçın (ayseyalcin1) | BSc in Politics and Data Science")
    st.markdown("* Maddox Leigh (maddoxleigh) | BSc in Politics and Data Science")
    st.write("This project aims to create easy to interpret, interactive graphs showing interesting correlations we found from various government census data and APIs")
    st.write("It is important to note that any correlations shown do not implicitly imply that a causation exists between the two variables!")
def show_interactive():
    st.markdown("# Interactive Graph")
    var_x = st.selectbox("Select an X variable:", ['Average Global Gini', 'UK GDP Per Capita (US $)', 'UK GDP Growth Rate',	'USA GDP Per Capita (US $)', 'US GDP Growth Rate','Persons Below Poverty (US)','Percent Below Poverty (US)', 'Voter Turnout in UK'])
    var_y = st.selectbox("Select a Y variable:", ['Average Global Gini', 'UK GDP Per Capita (US $)', 'UK GDP Growth Rate',	'USA GDP Per Capita (US $)', 'US GDP Growth Rate','Persons Below Poverty (US)','Percent Below Poverty (US)' ,'Voter Turnout in UK'])
    st.altair_chart(plot_interactive(var_x,var_y))
def show_us():
    st.markdown("# US data")
    st.markdown("## Population vs Population Density by State")
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(createpopulationgeo())

    with col2:
        st.altair_chart(createpopulationdensitygeo())

    st.altair_chart(createbidenpollchart())

    st.markdown("## Median Household income (2019-2021) against population density")
    st.altair_chart(createpopagainstincome())
    st.markdown("## GDP pre capita over time")
    st.altair_chart(plot_line_graph('USA GDP Per Capita (US $)'))
    st.markdown("## Growth (GDP) over time")
    st.altair_chart(plot_line_graph('US GDP Growth Rate'))

def show_uk():
    st.markdown("# UK data")
    st.markdown("## Crime rates over 2021 between UK cities")
    st.altair_chart(createcrimeratesbetweenUKcities())
    st.markdown("## Crime by category, London 2022")
    st.altair_chart(createlondoncrimebycategory())
    st.markdown("## Gdp pre capita ($) over time")
    st.altair_chart(plot_line_graph("UK GDP Per Capita (US $)"))
    st.markdown("## UK growth (GDP $) over time")
    st.altair_chart(plot_line_graph('UK GDP Growth Rate'))
def show_global():     
    st.markdown("# Global data")
    st.markdown("## Population distribution over time")
    st.altair_chart(create_pop_charts())
    st.markdown("## Average global Gini coefficient over time")
    st.altair_chart(create_gloabl_gini_average())

page = st.sidebar.radio("Go to", ['Home', 'Interactive Graph', 'US Data', 'UK Data', 'Global Data'])

if page == 'Home':
    show_home()
elif page == 'Interactive Graph':
    show_interactive()
elif page == 'US Data':
    show_us()
elif page == 'UK Data':
    show_uk()
elif page == 'Global Data':
    show_global()


