import dash
from dash.dependencies import Input, Output, State
from dash import html

# 각 페이지의 레이아웃을 임포트합니다.
from src.pages.summary.summary_layouts import summary_layout
# from src.pages.reputation.reputation_layouts import reputation_layout # 추후 추가될 페이지

def register_callbacks(app):
    """
    최상위 메뉴 이동 및 활성화 상태 변경을 위한 콜백을 등록합니다.
    """
    @app.callback(
        Output('page-content', 'children'),
        Output('menu-summary', 'className'),
        Output('menu-reputation', 'className'),
        # Output('menu-research', 'className'), # 추후 추가
        # Output('menu-cooperation', 'className'), # 추후 추가
        # Output('menu-global', 'className'), # 추후 추가
        Input('menu-summary', 'n_clicks'),
        Input('menu-reputation', 'n_clicks'),
        # Input('menu-research', 'n_clicks'), # 추후 추가
        # Input('menu-cooperation', 'n_clicks'), # 추후 추가
        # Input('menu-global', 'n_clicks'), # 추후 추가
    )
    def display_page(summary_clicks, reputation_clicks):
        """
        메뉴 버튼 클릭에 따라 다른 페이지 레이아웃을 반환합니다.
        """
        ctx = dash.callback_context
        button_id = 'menu-summary' # 기본값 설정

        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # 메뉴별 CSS 클래스 업데이트
        summary_class = 'menu-button'
        reputation_class = 'menu-button'

        if button_id == 'menu-summary':
            summary_class = 'menu-button active'
            content = summary_layout
        elif button_id == 'menu-reputation':
            reputation_class = 'menu-button active'
            content = html.H2("평판도 페이지 콘텐츠") # 평판도 페이지 레이아웃으로 교체 예정
        else:
            summary_class = 'menu-button active'
            content = summary_layout

        return content, summary_class, reputation_class

