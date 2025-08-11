import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# 임시 데이터 생성
df_rank = pd.DataFrame({
    'Year': [2023, 2024, 2025],
    'QA': [15, 12, 10],
    'THE': [25, 23, 20],
    '중앙일보': [8, 7, 5]
})

df_research = pd.DataFrame({
    'Year': [2023, 2024, 2025],
    'Funding': [100, 120, 150],
    'Citation': [1500, 1650, 1800]
})

df_cooperation = pd.DataFrame({
    'Year': [2023, 2024, 2025],
    'Tech_transfer': [5, 8, 12],
    'Patent_application': [50, 60, 70],
    'Patent_registration': [30, 40, 50],
    'Internship_rate': [0.15, 0.18, 0.22]
})

df_global = pd.DataFrame({
    'Year': [2023, 2024, 2025],
    'Total_students': [500, 600, 750],
    '중국': [200, 250, 300],
    '베트남': [150, 180, 200],
    '말레이시아': [100, 120, 150],
    '기타': [50, 50, 100]
})

# 지표별/항목별 색상 팔레트 정의
item_colors = {
    'QA': '#1f77b4', 
    'THE': '#ff7f0e',
    '중앙일보': '#2ca02c',
    'Funding': '#1f77b4',
    'Citation': '#ff7f0e',
    'Tech_transfer': '#1f77b4',
    'Patent_application': '#ff7f0e',
    'Patent_registration': '#2ca02c',
    'Internship_rate': '#9467bd',
    '중국': '#1f77b4',
    '베트남': '#ff7f0e',
    '말레이시아': '#2ca02c',
    '기타': '#7f7f7f'
}

# KPI 카드를 생성하는 헬퍼 함수
def create_kpi_card(title, value, prev_value, suffix='', color='gray'):
    try:
        current_val = float(value)
        prev_val = float(prev_value)
    except (ValueError, TypeError):
        current_val = 0
        prev_val = 0

    change = current_val - prev_val
    
    if suffix == '%':
        display_value = f"{current_val:.0%}"
        change_text = f"{change * 100:.0f}"
    else:
        display_value = f"{current_val:.0f}"
        change_text = f"{change:.0f}"

    arrow = ''
    arrow_color = 'gray'
    change_text = ""
    
    if "순위" in title:
        if change < 0:
            arrow = '▲'
            arrow_color = '#dc3545'  # Red for rank improvement
        elif change > 0:
            arrow = '▼'
            arrow_color = '#007bff'  # Blue for rank decline
        change_text = f"{abs(change):.0f}"
    else:
        if change > 0:
            arrow = '▲'
            arrow_color = '#dc3545'
        elif change < 0:
            arrow = '▼'
            arrow_color = '#007bff'
        
        if suffix == '%':
            change_text = f"{change * 100:.0f}"
        else:
            change_text = f"{change:.0f}"

    if suffix == '%':
        display_value = f"{current_val:.0%}"
    else:
        display_value = f"{current_val:.0f}"

    # KPI 카드 내용
    return html.Div([
        html.H4(title, className='kpi-title'),
        html.Div(className='kpi-value-container', children=[
            html.P(f"{display_value}", className='kpi-value', style={'color': color}),
            html.Div(className='kpi-change', children=[
                html.Span(arrow, style={'color': arrow_color}),
                html.Span(f" {change_text}{'%' if suffix == '%' else ''}", style={'color': arrow_color})
            ])
        ])
    ], className='kpi-card')

# Dash 앱 초기화
app = dash.Dash(__name__)

# 대시보드 레이아웃
app.layout = html.Div(
    style={'font-family': 'Arial'},
    children=[
        # 타이틀에 로고와 텍스트 추가
        html.Div(
            className='dashboard-header',
            children=[
                html.Img(src='https://www.catholic.ac.kr/_res/cuk/ko/img/common/menu01/simbol_img01.jpg', style={'height': '46px', 'margin-right': '15px'}),
                html.H1("CUK 대학발전 대시보드", style={'margin': '0', 'font-size': '32px', 'font-weight': 'bold'})
            ]
        ),

        html.Div(
            className='menu-container',
            children=[
                html.Button("평판도", id="menu-reputation", n_clicks=0, className='menu-button'),
                html.Button("연구실적", id="menu-research", n_clicks=0, className='menu-button'),
                html.Button("산학협력", id="menu-cooperation", n_clicks=0, className='menu-button'),
                html.Button("글로벌", id="menu-global", n_clicks=0, className='menu-button'),
            ]
        ),
        html.Br(),

        # 토글 버튼 컨테이너
        html.Div(
            className="toggle-container",
            children=[
                html.Div("3개년 추이보기", style={'font-weight': 'bold', 'margin-right': '10px'}),
                html.Button("3개년 추이 켜기", id="trend-button", n_clicks=0, className='toggle-button')
            ]
        ),

        html.Div(
            id="main-content",
            className='main-container'
        )
    ]
)

# 콜백 함수: '3개년 추이' 버튼 클릭 시 전체 레이아웃 변경
@app.callback(
    Output("main-content", "children"),
    Output("trend-button", "className"),
    Output("trend-button", "children"),
    Input("trend-button", "n_clicks")
)
def update_layout(n_clicks):
    is_trend_view = n_clicks is not None and n_clicks % 2 != 0
    current_year = 2025
    prev_year = 2024
    
    rank_current = df_rank[df_rank['Year'] == current_year].iloc[0]
    rank_prev = df_rank[df_rank['Year'] == prev_year].iloc[0]
    research_current = df_research[df_research['Year'] == current_year].iloc[0]
    research_prev = df_research[df_research['Year'] == prev_year].iloc[0]
    cooperation_current = df_cooperation[df_cooperation['Year'] == current_year].iloc[0]
    cooperation_prev = df_cooperation[df_cooperation['Year'] == prev_year].iloc[0]
    global_current = df_global[df_global['Year'] == current_year].iloc[0]
    global_prev = df_global[df_global['Year'] == prev_year].iloc[0]

    if is_trend_view:
        button_class = 'toggle-button on'
        button_text = ' '
        content = [
            html.Div(className='content-section',
                     children=[html.H3("평판도 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="reputation-trend-graph", figure=get_reputation_trend_figure(), style={'height': '400px'})]),
            html.Div(className='content-section',
                     children=[html.H3("연구실적 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="research-trend-graph", figure=get_research_trend_figure(), style={'height': '400px'})]),
            html.Div(className='content-section',
                     children=[html.H3("산학협력 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="cooperation-trend-graph", figure=get_cooperation_trend_figure(), style={'height': '400px'})]),
            html.Div(className='content-section',
                     children=[html.H3("글로벌 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="global-trend-graph", figure=get_global_trend_figure(), style={'height': '400px'})])
        ]
    else:
        button_class = 'toggle-button'
        button_text = ' '
        content = [
            html.Div(className='content-section',
                     children=[html.H3("평판도", style={'text-align': 'center'}),
                               html.Div(className='kpi-card-container',
                                        children=[create_kpi_card("QA 순위", rank_current['QA'], rank_prev['QA'], color=item_colors['QA']),
                                                  create_kpi_card("THE 순위", rank_current['THE'], rank_prev['THE'], color=item_colors['THE']),
                                                  create_kpi_card("중앙일보 순위", rank_current['중앙일보'], rank_prev['중앙일보'], color=item_colors['중앙일보'])])]),
            html.Div(className='content-section',
                     children=[html.H3("연구실적", style={'text-align': 'center'}),
                               html.Div(className='kpi-card-container',
                                        children=[create_kpi_card("연구비 수혜실적", research_current['Funding'], research_prev['Funding'], suffix='억원', color=item_colors['Funding']),
                                                  create_kpi_card("피인용지수", research_current['Citation'], research_prev['Citation'], color=item_colors['Citation'])])]),
            html.Div(className='content-section',
                     children=[html.H3("산학협력", style={'text-align': 'center'}),
                               html.Div(className='kpi-card-container',
                                        children=[create_kpi_card("기술이전 수입료", cooperation_current['Tech_transfer'], cooperation_prev['Tech_transfer'], suffix='억원', color=item_colors['Tech_transfer']),
                                                  create_kpi_card("특허 출원 및 등록", cooperation_current['Patent_registration'], cooperation_prev['Patent_registration'], color=item_colors['Patent_registration']),
                                                  create_kpi_card("현장실습 이수율", cooperation_current['Internship_rate'], cooperation_prev['Internship_rate'], suffix='%', color=item_colors['Internship_rate'])])]),
            html.Div(className='content-section',
                     children=[
                         html.H3("글로벌", style={'text-align': 'center'}),
                         html.Div(
                             style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'margin-top': '20px'},
                             children=[
                                 html.Div(
                                     style={'width': '40%', 'display': 'flex', 'justify-content': 'center'},
                                     children=[create_kpi_card("총 유학생 수", global_current['Total_students'], global_prev['Total_students'], color=item_colors['중국'])]
                                 ),
                                 html.Div(
                                     style={'width': '55%'},
                                     children=[
                                         dcc.Graph(
                                             figure=go.Figure(
                                                 data=[go.Bar(
                                                     x=global_current[['중국', '베트남', '말레이시아', '기타']].index,
                                                     y=global_current[['중국', '베트남', '말레이시아', '기타']].values,
                                                     marker_color=[item_colors['중국'], item_colors['베트남'], item_colors['말레이시아'], item_colors['기타']]
                                                 )],
                                                 layout=go.Layout(
                                                     title='국가별 유학생 수 (2025)',
                                                     margin={'t': 40, 'b': 40, 'l': 40, 'r': 40}
                                                 )
                                             ),
                                             style={'height': '300px'}
                                         )
                                     ]
                                 )
                             ]
                         )
                     ])
        ]
    return content, button_class, button_text

# 3개년 추이 그래프 함수
def get_reputation_trend_figure():
    fig = go.Figure()
    for institution in df_rank.columns[1:]:
        fig.add_trace(go.Scatter(x=df_rank['Year'], y=df_rank[institution], mode='lines+markers', name=institution, line=dict(color=item_colors[institution]), marker=dict(color=item_colors[institution])))
    fig.update_layout(
        title='평가기관별 순위 (3개년 추이)',
        yaxis=dict(autorange="reversed"),
        xaxis=dict(dtick=1),
        legend_title="평가기관",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

def get_research_trend_figure():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_research['Year'], y=df_research['Funding'], mode='lines+markers', name='연구비 수혜실적 (억원)', yaxis='y1', line=dict(color=item_colors['Funding']), marker=dict(color=item_colors['Funding'])))
    fig.add_trace(go.Scatter(x=df_research['Year'], y=df_research['Citation'], mode='lines+markers', name='피인용지수', yaxis='y2', line=dict(color=item_colors['Citation']), marker=dict(color=item_colors['Citation'])))
    fig.update_layout(
        title='연구비 및 피인용지수 (3개년 추이)',
        yaxis=dict(title='연구비 (억원)'),
        xaxis=dict(dtick=1),
        yaxis2=dict(title='피인용지수', overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

def get_cooperation_trend_figure():
    fig = go.Figure()
    fig.add_trace(go.Bar(name='특허 출원', x=df_cooperation['Year'], y=df_cooperation['Patent_application'], marker_color=item_colors['Patent_application']))
    fig.add_trace(go.Bar(name='특허 등록', x=df_cooperation['Year'], y=df_cooperation['Patent_registration'], marker_color=item_colors['Patent_registration']))
    fig.add_trace(go.Scatter(x=df_cooperation['Year'], y=df_cooperation['Internship_rate'] * 100, mode='lines+markers', name='현장실습 이수율 (%)', yaxis='y2', line=dict(color=item_colors['Internship_rate']), marker=dict(color=item_colors['Internship_rate'])))
    fig.update_layout(
        title='산학협력 (3개년 추이)',
        barmode='group',
        xaxis=dict(dtick=1),
        yaxis2=dict(title='이수율 (%)', overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

def get_global_trend_figure():
    fig = go.Figure()
    for country in ['중국', '베트남', '말레이시아', '기타']:
        fig.add_trace(go.Scatter(x=df_global['Year'], y=df_global[country], mode='lines+markers', name=country, line=dict(color=item_colors[country]), marker=dict(color=item_colors[country])))
    fig.update_layout(
        title='외국인 유학생 수 (3개년 추이)',
        xaxis=dict(dtick=1),
        legend_title="국가",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

# 앱 실행
if __name__ == '__main__':
    app.run(debug=True)

# App Engine을 위한 서버 변수 정의
server = app.server

# Waitress를 사용한 로컬 테스트용 코드 (선택 사항)
# 아래 코드는 로컬에서 waitress로 실행할 때만 사용합니다.
#from waitress import serve
#serve(app.server, host='0.0.0.0', port=8080)