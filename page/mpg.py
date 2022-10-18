import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import koreanize_matplotlib


st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
)

# 메인 화면 제목 마크다운
st.markdown("# 자동차 연비🚗")
# 왼쪽 사이드바 제목 마크다운
st.sidebar.markdown("# 자동차🚗")

# 데이터 URL 불러오기, 출력
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"

@st.cache
def load_data(url):
    data = pd.read_csv(url)
    return data

data_load_state = st.text('Loading data...')
data = load_data(url)
data_load_state.text("Done! (using st.cache)")

# 사이드바
st.sidebar.header('User Input Features')

# 연도 검색 기준
selected_year = st.sidebar.selectbox('Year',
        list(reversed(range(data.model_year.min(), data.model_year.max())))
        )
# 설정된 검색 기준으로 데이터 준비
if selected_year > 0:
    data = data[data.model_year == selected_year]
    
# 지역 검색 기준    
sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin)

# 설정된 검색 기준으로 데이터 준비
if len(selected_origin) > 0:
    data = data[data.origin.isin(selected_origin)]
    
st.dataframe(data)

st.line_chart(data["mpg"])
st.bar_chart(data["mpg"])

pxh = px.histogram(data, x='origin')
pxh

fig, ax = plt.subplots(figsize=(10,3))
sns.barplot(data=data, x="origin", y="mpg").set_title("지역 별 자동차 연비")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(15,4))
sns.barplot(data=data, x="weight", y="displacement").set_title("무게 별 배기량")
st.pyplot(fig)
