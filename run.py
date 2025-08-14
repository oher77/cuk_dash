import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import re
import plotly.graph_objs as go

# 데이터 로딩 (기존 로직 그대로 유지)
try:
    df_reputation = pd.read_excel('data/reputation.xlsx')
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure reputation.xlsx is in the 'data' directory. Using temporary data.")
    df_reputation = pd.DataFrame({
        'Year': [2024, 2025, 2026],
        'QS_Rank': [850, 800, 750],
        'QS_Rank_Domestic': [15, 12, 10],
        'THE_Rank': [900, 850, 800],
        'THE_Rank_Domestic': [20, 18, 16],
        'ARWU_Rank': [700, 650, 600],
        'ARWU_Rank_Domestic': [10, 9, 8],
        'QS_Overall': [16.53, 20.0, 30.8],
        'QS_Academic_Reputation': [4.5, 5.0, 7.9],
        'QS_Citations_Per_Faculty': [18.1, 25.0, 31.0],
        'QS_Faculty_Student_Ratio': [85.0, 90.0, 97.4],
        'QS_Employer_Reputation': [3.2, 4.0, 6.0]
    })

try:
    df_research = pd.read_excel('data/research.xlsx')
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure research.xlsx is in the 'data' directory. Using temporary data.")
    df_research = pd.DataFrame({
        'Year': [2023, 2024, 2025],
        'Funding': [100, 120, 150],
        'Citation': [1500, 1650, 1800]
    })

try:
    df_cooperation = pd.read_excel('data/cooperation.xlsx')
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure cooperation.xlsx is in the 'data' directory. Using temporary data.")
    df_cooperation = pd.DataFrame({
        'Year': [2023, 2024, 2025],
        'Tech_transfer': [5, 8, 12],
        'Patent_application': [50, 60, 70],
        'Patent_registration': [30, 40, 50],
        'Internship_rate': [0.15, 0.18, 0.22]
    })

try:
    df_global = pd.read_excel('data/global.xlsx')
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure global.xlsx is in the 'data' directory. Using temporary data.")
    df_global = pd.DataFrame({
        'Year': [2023, 2024, 2025],
        'Total_students': [500, 600, 750],
        '중국': [200, 250, 300],
        '베트남': [150, 180, 200],
        '말레이시아': [100, 120, 150],
        '기타': [50, 50, 100]
    })

# Dash 앱 초기화
app = dash.Dash(__name__, external_stylesheets=['/assets/style.css'])

# 다른 파일에서 정의된 레이아웃 및 콜백 함수를 가져옵니다.
from src.main_layouts import main_layout
from src.main_callbacks import register_callbacks as register_main_callbacks
from src.pages.summary.summary_callbacks import register_callbacks as register_summary_callbacks
# from src.pages.reputation.reputation_layouts import reputation_layout 
# from src.pages.reputation.reputation_callbacks import register_callbacks as register_reputation_callbacks 

# 전역 데이터프레임과 색상 팔레트를 다른 파일에서 사용하기 위해 전역 변수로 설정
global_data = {
    'df_reputation': df_reputation,
    'df_research': df_research,
    'df_cooperation': df_cooperation,
    'df_global': df_global,
    'item_colors': {
        'QS': '#1f77b4', 'THE': '#ff7f0e', 'ARWU': '#2ca02c', 'Funding': '#1f77b4', 'Citation': '#ff7f0e',
        'Tech_transfer': '#1f77b4', 'Patent_application': '#ff7f0e', 'Patent_registration': '#2ca02c',
        'Internship_rate': '#9467bd', '중국': '#1f77b4', '베트남': '#ff7f0e', '말레이시아': '#2ca02c', '기타': '#7f7f7f'
    }
}

# 앱 레이아웃 설정
app.layout = main_layout

# 콜백 등록
register_main_callbacks(app)
register_summary_callbacks(app, global_data)
# 평판도 페이지 콜백 등록 (임시)
# register_reputation_callbacks(app, global_data)

# App Engine을 위한 서버 변수 정의
server = app.server

if __name__ == '__main__':
    app.run(debug=True)
