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
    us_population_df = pd.read_csv("docs/Population_And_Median_Income")
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
    us_population_df = pd.read_csv("docs/Population_And_Median_Income")
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
def createpopagainstincome():
    merged_population_income = pd.read_csv("docs/Population_And_Median_Income")
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
    crimeratesdf = pd.read_csv("crimerates2021.csv")
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
    crimecategorylondon2022 = pd.read_csv("crimecategorylondon2022.csv")
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
st.markdown("## Median Household income (2019-2021) against population density")
st.altair_chart(createpopagainstincome())
st.markdown("# UK data")
st.markdown("## Crime rates over 2021 between UK cities")
st.altair_chart(createcrimeratesbetweenUKcities())
st.markdown("## Crime by category, London 2022")
st.altair_chart(createlondoncrimebycategory())

    

