from dash import dcc, html
import pandas as pd

# 임시 데이터프레임과 년도 목록
try:
    df_reputation = pd.read_excel('data/reputation.xlsx')
except FileNotFoundError:
    df_reputation = pd.DataFrame({'Year': [2024, 2025, 2026]})
years = df_reputation['Year'].unique()

summary_layout = html.Div(
    children=[
        # 하위 메뉴: 토글 버튼 및 년도 선택 드롭다운
        html.Div(
            className="toggle-container",
            children=[
                dcc.Dropdown(
                    id='year-selector',
                    options=[{'label': str(year), 'value': year} for year in years],
                    value=years.max(),  # 최신 년도를 초기값으로 설정
                    clearable=False,
                    style={'width': '120px', 'margin-right': '20px'}
                ),
                html.Div("3개년 추이보기", style={'font-weight': 'bold', 'margin-right': '10px'}),
                html.Button(id="trend-button", n_clicks=0, className='toggle-button')
            ]
        ),
        
        # 실제 요약 페이지 콘텐츠가 로드될 영역
        html.Div(
            id="summary-content",
            className='main-container',
            children=[] # 콜백에 의해 채워질 예정
        )
    ]
)
