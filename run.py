import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# 구조화된 모듈에서 필요한 함수들을 불러옵니다.
from data_handler import get_all_data
from layouts import get_main_layout, get_kpi_layout, get_trend_layout
from callbacks import register_callbacks

# 대시보드 데이터 로딩
# 각 파일의 데이터를 튜플 형태로 받아옵니다.
(df_reputation, df_research, df_cooperation, df_global) = get_all_data()

# Dash 앱 초기화
app = dash.Dash(__name__)

# CSS 파일을 불러옵니다.
# styles.css는 프로젝트 루트 디렉토리에 있어야 합니다.
app.css.append_css({'external_url': '/static/styles.css'})

# 전체 레이아웃 정의
# get_main_layout 함수에 df_reputation을 전달하여 드롭다운 옵션을 생성합니다.
app.layout = get_main_layout(df_reputation)

# 콜백 함수 등록
# register_callbacks 함수에 app과 모든 데이터를 전달합니다.
register_callbacks(app, df_reputation, df_research, df_cooperation, df_global)

# App Engine을 위한 서버 변수 정의
server = app.server

# Waitress를 사용한 로컬 테스트용 코드 (선택 사항)
if __name__ == '__main__':
    # run.py와 동일한 디렉토리에 'data' 폴더가 있고, 그 안에 엑셀 파일이 있는지 확인하세요.
    app.run(debug=True)
