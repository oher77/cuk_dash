import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from components import create_kpi_card, create_ranking_card, item_colors, \
    get_reputation_trend_figure, get_research_trend_figure, \
    get_cooperation_trend_figure, get_global_trend_figure

def get_main_layout(df_reputation):
    """
    대시보드의 전체 초기 레이아웃을 생성합니다.
    """
    return html.Div(
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
            html.Div(id="main-content", className='main-container')
        ]
    )

def get_kpi_layout(current_year, prev_year, dataframes):
    """
    단일 년도 KPI 레이아웃을 생성합니다.
    """
    df_reputation, df_research, df_cooperation, df_global = dataframes

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

    return [
        html.Div(className='content-section',
                 children=[html.H3("평판도", style={'text-align': 'center'}),
                           html.Div(className='kpi-card-container',
                                    children=[
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

def get_trend_layout(dataframes):
    """
    3개년 추이 그래프 레이아웃을 생성합니다.
    """
    df_reputation, df_research, df_cooperation, df_global = dataframes
    return [
        html.Div(className='content-section',
                 children=[html.H3("평판도 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="reputation-trend-graph", figure=get_reputation_trend_figure(df_reputation), style={'height': '400px'})]),
        html.Div(className='content-section',
                 children=[html.H3("연구실적 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="research-trend-graph", figure=get_research_trend_figure(df_research), style={'height': '400px'})]),
        html.Div(className='content-section',
                 children=[html.H3("산학협력 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="cooperation-trend-figure", figure=get_cooperation_trend_figure(df_cooperation), style={'height': '400px'})]),
        html.Div(className='content-section',
                 children=[html.H3("글로벌 (3개년 추이)", style={'text-align': 'center'}), dcc.Graph(id="global-trend-graph", figure=get_global_trend_figure(df_global), style={'height': '400px'})])
    ]
