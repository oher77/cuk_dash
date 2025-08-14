from dash.dependencies import Input, Output
from dash import html, dcc
import pandas as pd
import plotly.graph_objs as go
import re

# 재사용 가능한 컴포넌트들을 임포트합니다.
from src.components.common_components import create_ranking_card, create_kpi_card

# 전역 데이터프레임과 색상 팔레트를 저장할 변수
global_dfs = {}
item_colors = {}

def register_callbacks(app, global_data):
    """
    요약 페이지에 필요한 모든 콜백 함수를 등록합니다.
    """
    global global_dfs, item_colors
    global_dfs = global_data
    item_colors = global_data['item_colors']
    
    # 3개년 추이 그래프 함수들을 정의합니다.
    def get_reputation_trend_figure():
        df_reputation = global_dfs['df_reputation']
        fig = go.Figure()
        
        for institution in ['QS', 'THE', 'ARWU']:
            column = f'{institution}_Rank'
            if column in df_reputation.columns:
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
        df_research = global_dfs['df_research']
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
        df_cooperation = global_dfs['df_cooperation']
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
        df_global = global_dfs['df_global']
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


    @app.callback(
        Output("summary-content", "children"),
        Output("trend-button", "className"),
        Input("trend-button", "n_clicks"),
        Input("year-selector", "value")
    )
    def update_summary_layout(n_clicks, selected_year):
        is_trend_view = n_clicks is not None and n_clicks % 2 != 0
        current_year = selected_year
        prev_year = current_year - 1

        df_reputation = global_dfs['df_reputation']
        df_research = global_dfs['df_research']
        df_cooperation = global_dfs['df_cooperation']
        df_global = global_dfs['df_global']

        # 데이터가 존재하는지 확인하는 로직
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
        return content, button_class

