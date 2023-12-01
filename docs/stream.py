import requests
import pandas as pd
import streamlit as st
import altair as alt

jsonlist = requests.get("https://api.census.gov/data/2019/pep/charagegroups?get=NAME,POP&HISP=2&for=state:*").json()
states =[]
print(jsonlist[3])
populations =[]
for list in jsonlist:
    states.append(list[0])
    populations.append(list[1])
data = {"State":states,"Population":populations
}
df=pd.DataFrame(data)
df = df.iloc[1:]
df["Population"]=pd.to_numeric(df["Population"])
chart = alt.Chart(df).mark_area().encode(
    x="State",
    y="Population"
)
st.title('Population Chart')
st.altair_chart(
    chart, use_container_width=True)

