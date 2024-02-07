# Importing libraries
import statsmodels.api as sm
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
from sqlalchemy import create_engine

# Creating engine used to access our database
engine = create_engine('sqlite:///Docs/Data/PoliticsandDataSci.db', 
                       echo=False, 
                       isolation_level="AUTOCOMMIT")
# Opening connection to database
with engine.connect() as conn:
        pass


# Generic method for plotting line graph from data in interactive table
def plot_line_graph(y_column):
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
    # smoothing and aggregating data
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
    # reading sql table to dataframe
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

## Website creation

# This line of code allows user to navigate between different pages on the website
page = st.sidebar.radio("Go to", ['Home', 'Interactive Graph', 'US Data', 'UK Data', 'Global Data'])

# The following are functions for displaying each page
def show_home():
    st.title('Political Data Science project')
    st.markdown("* Alex Faith (alexgabriellafaith) | BSc in Politics and Data Science")
    st.markdown("* Ayşe Yalçın (ayseyalcin1) | BSc in Politics and Data Science")
    st.markdown("* Maddox Leigh (maddoxleigh) | BSc in Politics and Data Science")
    st.write("This project aims to create easy to interpret, interactive graphs showing interesting correlations we found from various government census data and APIs")
    st.write("It is important to note that any correlations shown do not implicitly imply that a causation exists between the two variables!")

def show_interactive():
    st.markdown("# Interactive Graph")
    # Taking user input via drop down box
    var_x = st.selectbox("Select an X variable:", ['Average Global Gini', 'UK GDP Per Capita (US $)', 'UK GDP Growth Rate',	'USA GDP Per Capita (US $)', 'US GDP Growth Rate','Persons Below Poverty (US)','Percent Below Poverty (US)', 'Voter Turnout in UK'])
    var_y = st.selectbox("Select a Y variable:", ['Average Global Gini', 'UK GDP Per Capita (US $)', 'UK GDP Growth Rate',	'USA GDP Per Capita (US $)', 'US GDP Growth Rate','Persons Below Poverty (US)','Percent Below Poverty (US)' ,'Voter Turnout in UK'])
    st.altair_chart(plot_interactive(var_x,var_y))
    st.markdown("This graph acts as a tool and compares different X and Y variables that are interchangeable according to the desired comparison that needs to be made. Every single point in the graph represents a year, and therefore all variables that are compared are compared by yearly data.")
    st.markdown("The data in the X and Y variables may not be correlational data, and can be adhered to what the user would like to find and compare, yet, finding a correlation is possible with the data given, as they provide sufficient comparable aspects. There are confounding variables in each correlation, and therefore they must be considered if they are being said to have a correlation. The line of best fit is present when X and/or Y variables are changed, so a positive or negative relationship can be analysed.")

def show_us():
    st.markdown("# US data")
    
    st.markdown("## Population vs Population Density by State")
    # Here two altair charts are organised to be side by side for easier comparison
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(createpopulationgeo())

    with col2:
        st.altair_chart(createpopulationdensitygeo())
    st.markdown("Sources = https://api.census.gov ,https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_area")
    st.markdown("This graph summarises the population density for each state in the USA, and the population distribution between each state in the USA, to compare how each changes. The data is shown in the map which, as you hover over the state, the population and population density can be seen.")
    st.markdown("It can be seen that the highest population is in California, yet the highest population density is in New Jersey, and therefore the change can be seen that the land area affects how population density differs.")
    st.markdown("It is important to also consider that when viewing population density, that land area was only used, therefore inhabitable regions, if there is a lake or body of water in a state, affects the population density if one considers total area/population. The findings may also be affected by the state being a coastal, and therefore more desired region to live in, or a landlocked state. Reasons to move to the state, such as urbanisation, safety, healthcare conditions, and employment opportunities must also be considered when analysing reasons why that region has a higher population.")
    
    st.markdown("## Biden Aproval over time")
    st.altair_chart(createbidenpollchart())
    st.markdown("Source = https://projects.fivethirtyeight.com/biden-approval-rating/")
    st.markdown("This graph compares bidens approval ratings throughout his presidency with key events in american politics")
    st.markdown("Biden's approval peaked when he first took office on January 20th 2021, and have slowly decreased since then.The failure to adequately respond to HurricaneIda and Biden's meeting with Putin at the Geneva summit, seem to coincide with a clear increase of disapproval rates.")
    st.markdown(" It is important to assert caution here and not blindly reduce the change of approval ratings to these events, there are other variables that may also contribute to a change in approval ratings: increasing polarisation, protests, media coverage and scandals.")
    st.markdown("## Median Household income (2019-2021) against population density")
    st.altair_chart(createpopagainstincome())
    st.markdown("Sources = https://www.census.gov/quickfacts/fact/table/US/PST045222, https://api.census.gov ,https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_area")
    st.markdown("This graph plots the average median household income between 2019 and 2021 against the population density of states")
    st.markdown("As can be seen there is a clear correlation between income and population denisty, this is likely due to densely populated areas being more urban with more jobs and oppurtunity")


    st.markdown("## GDP pre capita over time")
    st.altair_chart(plot_line_graph('USA GDP Per Capita (US $)'))
    st.markdown("Source = https://www.macrotrends.net/countries/USA/united-states/gdp-per-capita")
    st.markdown("This graph shows the GDP per capita value over the years in the United States, meaning average GDP per person, in the United States for each year.")
    st.markdown("There are no visible major fluctuations, but a general increase in the GDP per capita. This shows that an increasing investment in technology and employment opportunities paved way to the better wellbeing of US citizens over the years.")
    st.markdown("The graph shows a decrease in the year 2008, which can show the effects of the 2008 stock market crash, and the effects of it on the USA. Though, a general increase can show that there are also different confounding variables, which should be considered.")
    
    st.markdown("## Growth (GDP) over time")
    st.altair_chart(plot_line_graph('US GDP Growth Rate'))
    st.markdown("Source = https://www.macrotrends.net/countries/USA/united-states/gdp-per-capita")
    st.markdown("This graph shows the GDP rate over the years in the United States, where GDP accounts for the monetary value of all finished goods in the country.")
    st.markdown("The fluctuations in the graph show that though there are changes in overall GDP, they are not usually consistent over the years. The largest contributor to GDP in the USA, which is service-based industries, is generally a large output generator, in comparison to the manufacturing or agricultural industry, it can be seen that the professional and business sector is fluctuating, and there is a small general decrease in value.")
    st.markdown("When analysing the graph, the 2008 stock market crash and COVID must be considered alongside other variables in order to see the effects of global issues on US GDP.")

def show_uk():
    st.markdown("# UK data")
    
    st.markdown("## Crime rates over 2021 between UK cities")
    st.altair_chart(createcrimeratesbetweenUKcities())
    st.markdown("Source = https://data.police.uk/docs/method/crime-street/")
    st.markdown("This line graph compares the crime rates across 4 UK cities, using the surrounding area of their largest train stations, aiming to investigate the effect of covid lockdowns on crime rates.")
    st.markdown("There is a clear increase of crime as covid restrictions gradually began to lift at the beginning of the year, and a peak around June, when Boris Johnson announced the easing of restrictions. This supports the hypothesis that crime rates are correlated to intensity of restrictions.")
    st.markdown("London train station is much more expensive than the other cities and the surrounding area is naturally much busier due to its high population, thus it is logical that London would have the highest crime rates, as supported by this data. However, it is important for one to note the anomaly of Manchester - this raises important questions about the variation of data collection accuracy in cities, and the problems this causes in conducting cross city comparisons. One must be weary of this when drawing conclusions from the above findings.")
    
    st.markdown("## Crime by category, London 2022")
    st.altair_chart(createlondoncrimebycategory())
    st.markdown("Source = https://data.police.uk/docs/method/crime-street/")
    st.markdown("This bar chart shows the number of types of crime around kings cross, London, in 2021.")
    st.markdown("There is a clear range of counts in these findings with antisocial having around 7,000 vs. possession of weapon with 109.")
    st.markdown("Why is there such a stark difference? Consider that the area of kings cross is surrounded by various drinking locations, which may explain the high proportion of antisocial behaviours.")
    
    st.markdown("## Gdp pre capita ($) over time")
    st.altair_chart(plot_line_graph("UK GDP Per Capita (US $)"))
    st.markdown("Source = https://www.macrotrends.net/countries/GBR/united-kingdom/gdp-per-capita")
    st.markdown("This graph depicts the average GDP per capita, meaning average GDP per person, in the United Kingdom for each year.")
    st.markdown("The graph shows a general increase in the GDP per capita in the UK, which can be constituted to the technological and industrial advancements, creating both more job opportunities, and generating a higher level of income.")
    st.markdown("The graph shows a severe decrease in the year 2008, which can show the effects of the 2008 stock market crash, and the effects of it on the UK. Though, a general increase can show that there are also different confounding variables, which should be considered.")
    
    st.markdown("## UK growth (GDP $) over time")
    st.altair_chart(plot_line_graph('UK GDP Growth Rate'))
    st.markdown("Source = https://www.macrotrends.net/countries/GBR/united-kingdom/gdp-gross-domestic-product")
    st.markdown("This graph shows the GDP rate over the years in the United Kingdom, where GDP accounts for the monetary value of all finished goods in the country.")
    st.markdown("There is a visible amount of fluctuations in the graph, which neither shows a general increase or decrease. The largest contributor to GDP in the UK, which is manufacturing, is generally a large output generator, yet the fluctuations show that there are other variables affecting country GDP.")
    st.markdown("When analysing the graph, the 2008 stock market crash and COVID must be considered alongside other variables in order to see the effects of global issues on UK GDP.")

def show_global():     
    st.markdown("# Global data")
    
    st.markdown("## Future population distribution estimates")
    st.altair_chart(create_pop_charts())
    st.markdown("Source = https://www.ined.fr/en/everything_about_population/data/world-projections/projections-by-countries/")
    st.markdown("These graphs show the distribution of the global population, depicted in the areas that are colour coded accordingly, and the expected increase of the population from years 2050 to 2100.")
    st.markdown("The high population in Central and Southern Asia is understandable with the Chinese population density and South Asian population, as it remains the highest populated region throughout years. One of the least populated, being Western Europe, can be correlated to the low death rates and low birth rates, compared to the high birth rates in the African region, where it can be seen that the population increases over time.")
    st.markdown("It is also important to consider the measures taken by countries to lower population increase, like the one-child policy in China, therefore affecting the increase of the region’s population over time. Also, better healthcare conditions must also be considered alongside other confounding variables, as better healthcare and welfare implies a longer lifetime and in turn a probability of a larger population in some regions, including Africa.")
    
    st.markdown("## Average global Gini coefficient over time")
    st.altair_chart(create_gloabl_gini_average())
    st.markdown("Source = http://data.un.org/Data.aspx?q=gini&d=WDI&f=Indicator_Code%3ASI.POV.GINI")
    st.markdown("This graph depicts the average global gini index rate over the years. The gini coefficient is a measure of income distribution, the higher the gini coefficient, the higher the inequality.")
    st.markdown("There is a general increase in the trend of the global gini index, which can be constituted to the wages and jobs of lower-skilled workers in tradable sectors, especially in developed economies.")
    st.markdown("It is important to consider that as the average global gini is seen to be fluctuating, it can be seen that though some countries are moving towards an equal industrialised economic system, some countries still remain economically less developed, with more inequality, not allowing for a steady increase or decrease in the average global index.")


# These conditional statements call the corresponding functions whenever a new page is selected
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


