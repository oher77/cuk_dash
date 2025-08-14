import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import re

# 변경된 부분: 각 파일을 개별적으로 로드하여 오류를 처리합니다.
# Try to load each XLSX file, fall back to temporary data if not found.
try:
    df_reputation = pd.read_excel('data/reputation.xlsx')
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure reputation.xlsx is in the 'data' directory. Using temporary data.")
    # 업데이트된 임시 데이터 프레임, ARWU 추가
    df_reputation = pd.DataFrame({
        'Year': [2024, 2025, 2026],
        'QS_Rank': [850, 800, 750],
        'QS_Rank_Domestic': [15, 12, 10],
        'THE_Rank': [900, 850, 800],
        'THE_Rank_Domestic': [20, 18, 16],
        'ARWU_Rank': [700, 650, 600],
        'ARWU_Rank_Domestic': [10, 9, 8],
        # 임시 데이터에 다른 평판도 관련 컬럼 추가 (사용자의 요청에 따라)
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


# 지표별/항목별 색상 팔레트 정의
item_colors = {
    'QS': '#1f77b4',
    'THE': '#ff7f0e',
    'ARWU': '#2ca02c',
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

# 변경된 부분: 순위 지표를 표시하는 새로운 KPI 카드 함수
def create_ranking_card(title, current_data, prev_data, suffix='', color='gray'):
    try:
        current_rank = current_data[f'{title.split(" ")[0]}_Rank']
        prev_rank = prev_data[f'{title.split(" ")[0]}_Rank']
        current_domestic_rank = current_data[f'{title.split(" ")[0]}_Rank_Domestic']
        prev_domestic_rank = prev_data[f'{title.split(" ")[0]}_Rank_Domestic']
    except (KeyError, TypeError):
        current_rank = "N/A"
        prev_rank = "N/A"
        current_domestic_rank = "N/A"
        prev_domestic_rank = "N/A"

    # NaN 값에 대한 className 및 텍스트 처리
    rank_value = f"{current_rank}" if not pd.isna(current_rank) else "미공개"
    rank_class = 'kpi-value global' if not pd.isna(current_rank) else 'kpi-value kpi-na'
    domestic_rank_value = f"{current_domestic_rank}" if not pd.isna(current_domestic_rank) else "미공개"
    domestic_rank_class = 'kpi-value' if not pd.isna(current_domestic_rank) else 'kpi-value kpi-na'
    
    # 수정된 부분: 순위가 숫자 범위 문자열인지 확인
    def get_change_text(current, prev):
        if pd.isna(current) or pd.isna(prev) or isinstance(current, str) or isinstance(prev, str):
            return '', 'gray', 'N/A'
        
        try:
            change = float(current) - float(prev)
            if change < 0:
                arrow = '▲'
                arrow_color = '#dc3545'  # Red for rank improvement
                change_text = f"{abs(change):.0f}"
            elif change > 0:
                arrow = '▼'
                arrow_color = '#007bff'  # Blue for rank decline
                change_text = f"{abs(change):.0f}"
            else:
                arrow = ''
                arrow_color = 'gray'
                change_text = "0"
            return arrow, arrow_color, change_text
        except (ValueError, TypeError):
            return '', 'gray', 'N/A'

    arrow_int, arrow_color_int, change_text_int = get_change_text(current_rank, prev_rank)
    arrow_dom, arrow_color_dom, change_text_dom = get_change_text(current_domestic_rank, prev_domestic_rank)
    
    # NaN일 경우 변경 텍스트를 숨김
    if pd.isna(current_rank):
        arrow_int, change_text_int = '', ''
    if pd.isna(current_domestic_rank):
        arrow_dom, change_text_dom = '', ''

    # 변경된 부분: 기존 CSS 클래스를 활용하도록 수정
    return html.Div([
        html.H4(title, className='kpi-title'),
        html.Div(className='kpi-value-container', children=[
            html.Div(className='ranking-item', children=[
                html.P("국제", className='ranking-label'),
                html.P(rank_value, className=rank_class, style={'color': color, 'margin': '0'}),
                # 수정된 부분: style 속성에 올바른 색상 변수(arrow_color_int)를 사용
                html.Div(className='kpi-change', children=[
                    html.Span(arrow_int, style={'color': arrow_color_int}),
                    html.Span(f" {change_text_int}", style={'color': arrow_color_int})
                ])
            ]),
            html.Div(className='ranking-item', children=[
                html.P("국내", className='ranking-label'),
                html.P(domestic_rank_value, className=domestic_rank_class, style={'color': color, 'margin': '0'}),
                # 수정된 부분: style 속성에 올바른 색상 변수(arrow_color_dom)를 사용
                html.Div(className='kpi-change', children=[
                    html.Span(arrow_dom, style={'color': arrow_color_dom}),
                    html.Span(f" {change_text_dom}", style={'color': arrow_color_dom})
                ])
            ])
        ])
    ], className='kpi-card')

# 기존 KPI 카드를 생성하는 헬퍼 함수
def create_kpi_card(title, value, prev_value, suffix='', color='gray'):
    # 변경된 부분: value가 NaN인 경우를 먼저 처리
    if pd.isna(value):
        display_value = '미공개'
        value_class = 'kpi-value kpi-na'
        change_text = ''
        arrow = ''
        arrow_color = 'gray'
    else:
        try:
            current_val = float(value)
            prev_val = float(prev_value)
        except (ValueError, TypeError):
            current_val = 0
            prev_val = 0

        change = current_val - prev_val
        
        arrow = ''
        arrow_color = 'gray'
        change_text = ""
        
        if change > 0:
            arrow = '▲'
            arrow_color = '#dc3545'
        elif change < 0:
            arrow = '▼'
            arrow_color = '#007bff'
        
        if suffix == '%':
            change_text = f"{change * 100:.0f}"
            display_value = f"{current_val:.0%}"
        else:
            change_text = f"{change:.0f}"
            display_value = f"{current_val:.0f}"
        
        value_class = 'kpi-value'

    return html.Div([
        html.H4(title, className='kpi-title'),
        html.Div(className='kpi-value-container', children=[
            html.P(display_value, className=value_class, style={'color': color}),
            html.Div(className='kpi-change', children=[
                html.Span(arrow, style={'color': arrow_color}),
                html.Span(f" {change_text}{'%' if suffix == '%' and '순위' not in title else ''}", style={'color': arrow_color})
            ])
        ])
    ], className='kpi-card')

# 3개년 추이 그래프 함수
def get_reputation_trend_figure():
    fig = go.Figure()
    
    # 수정된 부분: 순위 데이터가 '숫자' 또는 '범위 문자열'일 경우를 모두 처리
    for institution in ['QS', 'THE', 'ARWU']:
        column = f'{institution}_Rank'
        if column in df_reputation.columns:
            # 순위 데이터 전처리: '801-850' -> 801
            processed_ranks = []
            for rank_str in df_reputation[column]:
                if isinstance(rank_str, str) and '-' in rank_str:
                    first_number = int(re.match(r'^\d+', rank_str).group(0))
                    processed_ranks.append(first_number)
                else:
                    processed_ranks.append(rank_str)

            fig.add_trace(go.Scatter(x=df_reputation['Year'], y=processed_ranks, mode='lines+markers', name=institution, line=dict(color=item_colors[institution]), marker=dict(color=item_colors[institution])))
    
    fig.update_layout(
        title='평가기관별 국제 순위 (3개년 추이)',
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

        # 토글 버튼 컨테이너에 드롭다운 추가
        html.Div(
            className="toggle-container",
            children=[
                # 변경된 부분: 년도 선택 드롭다운 추가
                dcc.Dropdown(
                    id='year-selector',
                    options=[{'label': str(year), 'value': year} for year in df_reputation['Year'].unique()],
                    value=2025,  # 초기값 설정
                    clearable=False,
                    style={'width': '120px', 'margin-right': '20px'}
                ),
                html.Div("3개년 추이보기", style={'font-weight': 'bold', 'margin-right': '10px'}),
                html.Button(id="trend-button", n_clicks=0, className='toggle-button')
            ]
        ),

        html.Div(
            id="main-content",
            className='main-container'
        )
    ]
)

# 콜백 함수: '3개년 추이' 버튼 클릭 시 전체 레이아웃 변경 및 년도 선택에 따른 데이터 업데이트
@app.callback(
    Output("main-content", "children"),
    Output("trend-button", "className"),
    Input("trend-button", "n_clicks"),
    Input("year-selector", "value")
)
def update_layout(n_clicks, selected_year):
    is_trend_view = n_clicks is not None and n_clicks % 2 != 0
    current_year = selected_year
    prev_year = current_year - 1

    # 변경된 부분: 데이터가 존재하는지 확인하는 로직 추가
    reputation_current_df = df_reputation[df_reputation['Year'] == current_year]
    reputation_prev_df = df_reputation[df_reputation['Year'] == prev_year]
    research_current_df = df_research[df_research['Year'] == current_year]
    research_prev_df = df_research[df_research['Year'] == prev_year]
    cooperation_current_df = df_cooperation[df_cooperation['Year'] == current_year]
    cooperation_prev_df = df_cooperation[df_cooperation['Year'] == prev_year]
    global_current_df = df_global[df_global['Year'] == current_year]
    global_prev_df = df_global[df_global['Year'] == prev_year]

    reputation_current = reputation_current_df.iloc[0] if not reputation_current_df.empty else pd.Series(dtype='object')
    reputation_prev = reputation_prev_df.iloc[0] if not reputation_prev_df.empty else pd.Series(dtype='object')
    research_current = research_current_df.iloc[0] if not research_current_df.empty else pd.Series(dtype='object')
    research_prev = research_prev_df.iloc[0] if not research_prev_df.empty else pd.Series(dtype='object')
    cooperation_current = cooperation_current_df.iloc[0] if not cooperation_current_df.empty else pd.Series(dtype='object')
    cooperation_prev = cooperation_prev_df.iloc[0] if not cooperation_prev_df.empty else pd.Series(dtype='object')
    global_current = global_current_df.iloc[0] if not global_current_df.empty else pd.Series(dtype='object')
    global_prev = global_prev_df.iloc[0] if not global_prev_df.empty else pd.Series(dtype='object')

    if is_trend_view:
        button_class = 'toggle-button on'
        content = [
            html.Div(className='content-section',
                     children=[html.H3("평판도 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="reputation-trend-graph", figure=get_reputation_trend_figure(), style={'height': '400px'})]),
            html.Div(className='content-section',
                     children=[html.H3("연구실적 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="research-trend-graph", figure=get_research_trend_figure(), style={'height': '400px'})]),
            html.Div(className='content-section',
                     children=[html.H3("산학협력 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="cooperation-trend-figure", figure=get_cooperation_trend_figure(), style={'height': '400px'})]),
            html.Div(className='content-section',
                     children=[html.H3("글로벌 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="global-trend-graph", figure=get_global_trend_figure(), style={'height': '400px'})])
        ]
    else:
        button_class = 'toggle-button'
        content = [
            html.Div(className='content-section',
                     children=[html.H3("평판도", style={'text-align': 'center'}),
                               html.Div(className='kpi-card-container',
                                        children=[
                                            # 변경된 부분: 새로운 함수 create_ranking_card를 사용하여 국내/국제 순위 모두 표시
                                            create_ranking_card("QS 순위", reputation_current, reputation_prev, color=item_colors['QS']),
                                            create_ranking_card("THE 순위", reputation_current, reputation_prev, color=item_colors['THE']),
                                            create_ranking_card("ARWU 순위", reputation_current, reputation_prev, color=item_colors['ARWU'])
                                        ])]),
            html.Div(className='content-section',
                     children=[html.H3("연구실적", style={'text-align': 'center'}),
                               html.Div(className='kpi-card-container',
                                        children=[create_kpi_card("연구비 수혜실적", research_current.get('Funding'), research_prev.get('Funding'), suffix='억원', color=item_colors['Funding']),
                                                  create_kpi_card("피인용지수", research_current.get('Citation'), research_prev.get('Citation'), color=item_colors['Citation'])])]),
            html.Div(className='content-section',
                     children=[html.H3("산학협력", style={'text-align': 'center'}),
                               html.Div(className='kpi-card-container',
                                        children=[create_kpi_card("기술이전 수입료", cooperation_current.get('Tech_transfer'), cooperation_prev.get('Tech_transfer'), suffix='억원', color=item_colors['Tech_transfer']),
                                                  create_kpi_card("특허 출원 및 등록", cooperation_current.get('Patent_registration'), cooperation_prev.get('Patent_registration'), color=item_colors['Patent_registration']),
                                                  create_kpi_card("현장실습 이수율", cooperation_current.get('Internship_rate'), cooperation_prev.get('Internship_rate'), suffix='%', color=item_colors['Internship_rate'])])]),
            html.Div(className='content-section',
                     children=[
                         html.H3("글로벌", style={'text-align': 'center'}),
                         html.Div(
                             style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'margin-top': '20px'},
                             children=[
                                 html.Div(
                                     style={'width': '40%', 'display': 'flex', 'justify-content': 'center'},
                                     children=[create_kpi_card("총 유학생 수", global_current.get('Total_students'), global_prev.get('Total_students'), color=item_colors['중국'])]
                                 ),
                                 html.Div(
                                     style={'width': '55%'},
                                     children=[
                                         dcc.Graph(
                                             figure=go.Figure(
                                                 data=[go.Bar(
                                                     x=['중국', '베트남', '말레이시아', '기타'],
                                                     y=[global_current.get('중국'), global_current.get('베트남'), global_current.get('말레이시아'), global_current.get('기타')],
                                                     marker_color=[item_colors['중국'], item_colors['베트남'], item_colors['말레이시아'], item_colors['기타']]
                                                 )],
                                                 layout=go.Layout(
                                                     # 변경된 부분: 그래프 제목에 선택된 년도 표시
                                                     title=f'국가별 유학생 수 ({current_year})',
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
    return content, button_class

# App Engine을 위한 서버 변수 정의
server = app.server

# Waitress를 사용한 로컬 테스트용 코드 (선택 사항)
if __name__ == '__main__':
    app.run(debug=True)
