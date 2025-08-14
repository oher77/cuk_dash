from dash import dcc, html
import dash_bootstrap_components as dbc

# 메뉴 버튼에 '요약' 메뉴 추가
menu_container = html.Div(
    className='menu-container',
    children=[
        html.Button("요약", id="menu-summary", n_clicks=0, className='menu-button active'),
        html.Button("평판도", id="menu-reputation", n_clicks=0, className='menu-button'),
        html.Button("연구실적", id="menu-research", n_clicks=0, className='menu-button'),
        html.Button("산학협력", id="menu-cooperation", n_clicks=0, className='menu-button'),
        html.Button("글로벌", id="menu-global", n_clicks=0, className='menu-button'),
    ]
)

# 전체 앱의 뼈대 레이아웃
main_layout = html.Div(
    style={'font-family': 'Arial'},
    children=[
        # 대시보드 헤더
        html.Div(
            className='dashboard-header',
            children=[
                html.Img(src='https://www.catholic.ac.kr/_res/cuk/ko/img/common/menu01/simbol_img01.jpg', style={'height': '46px', 'margin-right': '15px'}),
                html.H1("CUK 대학발전 대시보드", style={'margin': '0', 'font-size': '32px', 'font-weight': 'bold'})
            ]
        ),
        
        # 메뉴 컨테이너
        menu_container,
        
        html.Br(),

        # 페이지 콘텐츠가 로드될 영역
        # 초기에는 summary 페이지가 로드되도록 설정
        html.Div(
            id="page-content",
            className='main-container',
            children=[]
        ),

        # 현재 활성화된 메뉴를 저장하기 위한 dcc.Store
        dcc.Store(id='current-menu-state', data='menu-summary')
    ]
)

