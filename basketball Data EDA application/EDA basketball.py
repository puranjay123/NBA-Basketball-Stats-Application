import streamlit as st
import pandas as pd 
import base64
import matplotlib.pyplot as pyplot
import seaborn as sns
import numpy as np

st.title("NBA Player Stats Explorer")

st.markdown("""Application To sort NBA players Data for Past years""")

st.sidebar.header('User Input features')

selected_year = st.sidebar.selectbox('year',list(reversed(range(1950,2020))))

#wEB SCRAPING
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" +str(year)+"_per_game.html"
    html = pd.read_html(url,header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'],axis =1)
    return playerstats
playerstats = load_data(selected_year)

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team',sorted_unique_team,sorted_unique_team)

unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position',unique_pos,unique_pos)

#Filtering load_data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Seletced team')
st.write('Data Dimension:' + str(df_selected_team.shape[0])+ 'rows and' + str(df_selected_team.shape[1])+ ' columns.')
test = df_selected_team.astype(str)
st.dataframe(test)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'<a href="data:file/csv;base64,{b64}" download="playerDaTa.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)







