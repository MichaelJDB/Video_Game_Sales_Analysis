import pandas as pd
import streamlit as st
import altair as alt

# Load dataset 
data = pd.read_csv("Data/vgsales_cleaned.csv")  
data = data.rename(columns=lambda x: x.strip())  

st.title('🎮 Video Game Sales Dashboard')

# Sidebar filters
genre = st.sidebar.selectbox('Select Genre', options=data['Genre'].unique())
platform = st.sidebar.selectbox('Select Platform', options=data['Platform'].unique())

year_range = st.slider(
    'Select Year Range',
    int(data['Year'].min()),
    int(data['Year'].max()),
    (1980, 2011)
)

selected_genres = st.sidebar.multiselect(
    'Select Genres (optional)',
    options=data['Genre'].unique(),
    default=[genre]
)

# Filtered data
filtered = data[
    (data['Genre'].isin(selected_genres)) &
    (data['Platform'] == platform) &
    (data['Year'] >= year_range[0]) &
    (data['Year'] <= year_range[1])
]

st.subheader('Filtered Data')
st.dataframe(filtered)

# Tabs
tab1, tab2, tab3 = st.tabs(["Platforms", "Yearly Trends", "Publishers"])

with tab1:
    st.subheader("Top Platforms")
    top_platforms = data.groupby('Platform')['Global'].sum().nlargest(10).reset_index()
    platform_chart = alt.Chart(top_platforms).mark_bar(color='cornflowerblue').encode(
        x=alt.X('Global:Q', title='Global Sales (millions)'),
        y=alt.Y('Platform:N', sort='-x'),
        tooltip=['Platform', 'Global']
    ).properties(title='Top 10 Platforms by Global Sales')
    st.altair_chart(platform_chart, use_container_width=True)

with tab2:
    st.subheader("Sales by Year")
    sales_by_year = filtered.groupby('Year')['Global'].sum().reset_index()
    year_chart = alt.Chart(sales_by_year).mark_line(point=True).encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Global:Q', title='Global Sales'),
        tooltip=['Year', 'Global']
    ).properties(title='Global Video Game Sales by Year')
    st.altair_chart(year_chart, use_container_width=True)

with tab3:
    st.subheader("Top Publishers")
    top_publishers = data[data['Platform'] == platform].groupby('Publisher')['Global'].sum().nlargest(10).reset_index()
    publisher_chart = alt.Chart(top_publishers).mark_bar(color='orange').encode(
        x=alt.X('Global:Q', title='Global Sales (millions)'),
        y=alt.Y('Publisher:N', sort='-x'),
        tooltip=['Publisher', 'Global']
    ).properties(title='Top 10 Publishers by Global Sales')
    st.altair_chart(publisher_chart, use_container_width=True)

    st.subheader("Best-Selling Title per Publisher")
    best_titles = data.loc[data.groupby('Publisher')['Global'].idxmax()][['Publisher','Game Title','Global']]
    top_best_titles = best_titles.sort_values(by='Global', ascending=False).head(10)

    best_title_chart = alt.Chart(top_best_titles).mark_bar(color='mediumseagreen').encode(
        x=alt.X('Global:Q', title='Global Sales (millions)'),
        y=alt.Y('Publisher:N', sort='-x'),
        tooltip=['Publisher', 'Game Title', 'Global']
    ).properties(title='Best-Selling Title per Publisher')
    st.altair_chart(best_title_chart, use_container_width=True)




