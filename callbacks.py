import dash
from dash.dependencies import Input, Output
from layouts import get_kpi_layout, get_trend_layout

def register_callbacks(app, df_reputation, df_research, df_cooperation, df_global):
    """
    대시보드 상호작용을 위한 모든 콜백 함수를 등록합니다.
    """
    @app.callback(
        Output("main-content", "children"),
        Output("trend-button", "className"),
        Input("trend-button", "n_clicks"),
        Input("year-selector", "value")
    )
    def update_layout(n_clicks, selected_year):
        """
        '3개년 추이' 버튼 클릭과 년도 선택에 따라 메인 콘텐츠를 업데이트합니다.
        """
        is_trend_view = n_clicks is not None and n_clicks % 2 != 0
        current_year = selected_year
        prev_year = current_year - 1
        
        dataframes = (df_reputation, df_research, df_cooperation, df_global)

        if is_trend_view:
            button_class = 'toggle-button on'
            content = get_trend_layout(dataframes)
        else:
            button_class = 'toggle-button'
            content = get_kpi_layout(current_year, prev_year, dataframes)
        
        return content, button_class
