# DS105A Project
## Team Members
* Alex Faith (alexgabriellafaith) | BSc in Politics and Data Science
* Ayşe Yalçın (ayseyalcin1) | BSc in Politics and Data Science
* Maddox Leigh (maddoxleigh) | BSc in Politics and Data Science


**DATA VISUALISATIONS ARE ON OTHER WEBSITE**

## Why we chose our project topic 👀:
As Politics and Data Science students at LSE, we struggle the politics related data being stored in ways which are hard to interpret such as regression tables or excel files, which makes finding data for essays a very tedious process. Therefore, we sought out a website that is a source of easy to interpret data, that can also be customised to create interactive correlation graphs with simple descriptions underneath the graphs themselves in the USA/UK/Global data portion of the website. 

The descriptions help politics students, with no formal quatative skills, to make better anaylses for data summarisation. The data collected is political data focused on the USA, the UK, and global data to find more in depth sources to make graphs with interchangable variables. 

## How we gathered our data and challenges we faced:
We utilised the following methods to gather data throughout the project:

### Method 1: Web Scraping 💻
We gathered the majority of our data from different sources through web scraping credible websites such as census.gov and offical government pages such as ASPE. One problem we faced was, WIKI LINK PROBLEM.



### Method 2: APIs 💡
We also utilised APIs to find data, such as crime rates in the UK. Postman was particularly useful to explore the APIs and figure out the required parameters for the data we wanted. The crime rates API was extremely useful- as it allowed you to change the paramters of date and longnitude/latitude, which was useful for comparing cities. The issue with APIs was that many relevent ones we found were very expensive, thus websraping was very useful. Another issue was that the APIs usually directed us to Excel files or PDFs which contained qualitatative data and were were unable to turn this into usable quatative data.

### Method 3: Hidden APIs 📁
The website we used for hidden API collection was Fivethirtyeight and we were able to get the links of the json files through inspecting the page and going to the network tab, and then exploring the cURL using Postman. Though the process was challenging, we were able to gather the data in this manner. 

## What is the data and how does it look like in general 🔗:
The data was generally, as stated before, in the form of tables or graphs in which we scraped and collected with the aforementioned 3 methods. After scraping the data, we figured out what was useful and then cleaned it and saved relevent data to a csv. Lots of data sources had N/A columns or returned irrelevent data, such as crime ID. For example, the crime API returned 26,000 rows of data, which we cleaned and use value counts to reduce down, before saving it to a CSV.

We then used vega-altaire to create interactive data visualisations, using the appropriate graph type for the data. The graphs on the website are accomapained with a short explanation of what the graph suggests and the findings. 

## What we found out about the data 🔍:
Note: The following findings are also visible on the website under each graph. 

### UK crime rates data:
Explanation = This line graph compares the crime rates across 4 UK cities, using the surrounding area of their largest train stations, aiming to investigate the effect of covid lockdowns on crime rates. 

Findings = There is a clear increase of crime as covid restrictions gradually began to lift at the beginning of the year, and a peak around June, when Boris Johnson announced the easing of restrictions. This supports the hypothesis that crime rates are correlated to intensity of restrictions.

Consider = London train station is much more expensive than the other cities and the surrounding area is naturally much busier due to its high population, thus it is logical that London would have the highest crime rates, as supported by this data. However, it is important for one to note the anomaly of Manchester - this raises important questions about the variation of data collection accuracy in cities, and the problems this causes in conducting cross city comparisons. One must be weary of this when drawing conclusions from the above findings.

Source =  https://data.police.uk/docs/method/crime-street/  

### Crime category data:
Explanation = This bar chart shows the number of types of crime around kings cross, London, in 2021.

Findings = There is a clear range of counts in these findings with antisocial having around 7,000 vs. possession of weapon with XXX. 

Consider = Why is there such a stark difference? Consider that the area of kings cross is surrounded by various drinking locations, which may explain the high proportion of antisocial behaviours.

Source =  https://data.police.uk/docs/method/crime-street/ 

### Biden approval rates data:
Explanation = This graph compares bidens approval ratings throughout his presidency with key events in american politics 

Findings = Biden's approval peaked when he first took office on January 20th 2021, and have slowly decreased since then.The failure to adequately respond to HurricaneIda and Biden's meeting with Putin at the Geneva summit, seem to coincide with a clear increase of disapproval rates. 

Consider = It is important to assert caution here and not blindly reduce the change of approval ratings to these events, there are other variables that may also contribute to a change in approval ratings: increasing polarisation, protests, media coverage and scandals. 

Source =  https://projects.fivethirtyeight.com/biden-approval-rating/ 

### Population distribution over time data:
Explanation = These graphs show the distribution of the global population, depicted in the areas that are colour coded accordingly, and the expected increase of the population from years 2050 to 2100.

Findings = The high population in Central and Southern Asia is understandable with the Chinese population density and South Asian population, as it remains the highest populated region throughout years. One of the least populated, being Western Europe, can be correlated to the low death rates and low birth rates, compared to the high birth rates in the African region, where it can be seen that the population increases over time.

Consider = It is also important to consider the measures taken by countries to lower population increase, like the one-child policy in China, therefore affecting the increase of the region’s population over time. Also, better healthcare conditions must also be considered alongside other confounding variables, as better healthcare and welfare implies a longer lifetime and in turn a probability of a larger population in some regions, including Africa. 

Source = https://www.ined.fr/en/everything_about_population/data/world-projections/projections-by-countries/

### USA density data
Explanation = This graph summarises the population density for each state in the USA, and the population distribution between each state in the USA, to compare how each changes. The data is shown in the map which, as you hover over the state, the population and population density can be seen.

Findings = It can be seen that the highest population is in California, yet the highest population density is in New Jersey, and therefore the change can be seen that the land area affects how population density differs.

Consider = It is important to also consider that when viewing population density, that land area was only used, therefore inhabitable regions, if there is a lake or body of water in a state, affects the population density if one considers total area/population. The findings may also be affected by the state being a coastal, and therefore more desired region to live in, or a landlocked state. Reasons to move to the state, such as urbanisation, safety, healthcare conditions, and employment opportunities must also be considered when analysing reasons why that region has a higher population.

Sources = https://api.census.gov ,https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_area 

### Average global gini over the years graph:

Explanation = This graph depicts the average global gini index rate over the years, where the gini index shows economic inequality, the higher the gini, the higher the economic inequality.

Findings = There is a general increase in the trend of the global gini index, which can be constituted to the wages and jobs of lower-skilled workers in tradable sectors, especially in developed economies.

Consider = It is important to consider that as the average global gini is seen to be fluctuating, it can be seen that though some countries are moving towards an equal industrialised economic system, some countries still remain economically less developed, with more inequality, not allowing for a steady increase or decrease in the average global index.

Source = http://data.un.org/Data.aspx?q=gini&d=WDI&f=Indicator_Code%3aSI.POV.GINI 

### UK GDP per capita over the years graph:

Explanation = This graph depicts the average GDP per capita, meaning average GDP per person, in the United Kingdom for each year.

Findings = The graph shows a general increase in the GDP per capita in the UK, which can be constituted to the technological and industrial advancements, creating both more job opportunities, and generating a higher level of income.

Consider = The graph shows a severe decrease in the year 2008, which can show the effects of the 2008 stock market crash, and the effects of it on the UK. Though, a general increase can show that there are also different confounding variables, which should be considered. 

Source = https://www.macrotrends.net/countries/GBR/united-kingdom/gdp-per-capita 

### UK GDP growth rate over years data:

Explanation = This graph shows the GDP rate over the years in the United Kingdom, where GDP accounts for the monetary value of all finished goods in the country.

Findings = There is a visible amount of fluctuations in the graph, which neither shows a general increase or decrease. The largest contributor to GDP in the UK, which is manufacturing, is generally a large output generator, yet the fluctuations show that there are other variables affecting country GDP.

Consider = When analysing the graph, the 2008 stock market crash and COVID must be considered alongside other variables in order to see the effects of global issues on UK GDP.

Source = https://www.macrotrends.net/countries/GBR/united-kingdom/gdp-gross-domestic-product 

### US GDP per capita rate over years data:

Explanation = This graph shows the GDP per capita value over the years in the United States, meaning average GDP per person, in the United States for each year.

Findings = There are no visible major fluctuations, but a general increase in the GDP per capita. This shows that an increasing investment in technology and employment opportunities paved way to the better wellbeing of US citizens over the years.

Consider = The graph shows a  decrease in the year 2008, which can show the effects of the 2008 stock market crash, and the effects of it on the USA. Though, a general increase can show that there are also different confounding variables, which should be considered. 

Source = https://www.macrotrends.net/countries/USA/united-states/gdp-per-capita

### US GDP growth rate over years data:

Explanation = This graph shows the GDP rate over the years in the United States, where GDP accounts for the monetary value of all finished goods in the country.

Findings = The fluctuations in the graph show that though there are changes in overall GDP, they are not usually consistent over the years. The largest contributor to GDP in the USA, which is service-based industries, is generally a large output generator, in comparison to the manufacturing or agricultural industry, it can be seen that the professional and business sector is fluctuating, and there is a small general decrease in value. 

Consider = When analysing the graph, the 2008 stock market crash and COVID must be considered alongside other variables in order to see the effects of global issues on US GDP. 

Source = https://www.macrotrends.net/countries/USA/united-states/gdp-gross-domestic-product 

### The interactive graph
Explanation = This graph acts as a tool and compares different X and Y variables that are interchangeable according to the desired comparison that needs to be made. Every single point in the graph represents a year, and therefore all variables that are compared are compared by yearly data.

Consider = The data in the X and Y variables may not be correlational data, and can be adhered to what the user would like to find and compare, yet, finding a correlation is possible with the data given, as they provide sufficient comparable aspects. There are confounding variables in each correlation, and therefore they must be considered if they are being said to have a correlation. The line of best fit is present when X and/or Y variables are changed, so a positive or negative relationship can be analysed.

## Why we used Altair instead of plotnine and issues with Altair:
Altair produced graphs that were more interactive and visibly more pleasing to the eye instead of plotnine, so we decided to use Altair. The Altair package chaning during our project created some issues as we had running graphs, but they stopped running. We therefore had to update Altair and re-run the code to view the graphs, but in the end, the website and the graphs looked cohesive and more professional.

## What we used to merge the data:
To merge the data, we followed a method where we collected notebooks in a single folder, CSV files in a single folder, and data we didn't want outside the folders to be deleted from the main branch later on. The CSV files were added under the folder titled 'Data'. All folders and notebooks were under the folder 'docs' and therefore notebooks followed the path 'projectname / docs / Notebooks / notebookname' and CSV files followed the path 'projectname / docs / Data / csvfile' which were all renamed according to what data they contained in them. This system helped us group all our work in the main branch as we had multiple commits which created complexity.

## Organising Github: 
These are the steps/process we followed as we organised our GitHub.

### Step 1: The creation of notebooks 📌
The first step was a research step, and we scraped as much data as possible, also using all sorts of APIs. This was a trial and error step, where we decided which graphs worked best for us and what type of APIs we could use for the process. We also experimented with hidden APIs, giving us a broader range of resources and data. 

### Step 2: Organizing data 📌
The next step we created a data folder where we added all CSV files to it, so they could be uploaded to the website to create the interactive graphs. 

### Step 3: Markdowns and renaming 📌
We found that titling the notebooks the way we did in step 1 made it difficult to understand which notebook had which data, so we added markdown titles at the top of each notebook, so it is understandable when clicked on it. We also added short descriptions of the data summarized and hypotheses to some, so that we had a description that is easily understandable. Later on, we renamed our CSV files to represent what data they actually had. We also renamed out Notebooks where we added the name of the data utilising underscores between words. Example: UK_voter_turnout

### Step 4: Cleaning up notebooks 📌
In this step we added comments to all notebooks where needed, to further elaborate on where AI was used and what we did in each step. This helped us follow each other’s steps and work collabratively.

## Explanation of the process for each notebook:
Each notebook creates a csv folder on a different variable, which is stored in the data folder. 

At the start of each notebook there is a brief description of the purpose of the notebook.
