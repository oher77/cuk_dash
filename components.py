import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import re

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

def create_ranking_card(title, current_data, prev_data, color='gray'):
    """
    국제 및 국내 순위를 표시하는 KPI 카드를 생성합니다.
    """
    try:
        current_rank = current_data.get(f'{title.split(" ")[0]}_Rank')
        prev_rank = prev_data.get(f'{title.split(" ")[0]}_Rank')
        current_domestic_rank = current_data.get(f'{title.split(" ")[0]}_Rank_Domestic')
        prev_domestic_rank = prev_data.get(f'{title.split(" ")[0]}_Rank_Domestic')
    except (KeyError, TypeError):
        current_rank = "N/A"
        prev_rank = "N/A"
        current_domestic_rank = "N/A"
        prev_domestic_rank = "N/A"

    rank_value = f"{current_rank}" if not pd.isna(current_rank) else "미공개"
    rank_class = 'kpi-value global' if not pd.isna(current_rank) else 'kpi-value kpi-na'
    domestic_rank_value = f"{current_domestic_rank}" if not pd.isna(current_domestic_rank) else "미공개"
    domestic_rank_class = 'kpi-value' if not pd.isna(current_domestic_rank) else 'kpi-value kpi-na'

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
    
    if pd.isna(current_rank):
        arrow_int, change_text_int = '', ''
    if pd.isna(current_domestic_rank):
        arrow_dom, change_text_dom = '', ''

    return html.Div([
        html.H4(title, className='kpi-title'),
        html.Div(className='kpi-value-container', children=[
            html.Div(className='ranking-item', children=[
                html.P("국제", className='ranking-label'),
                html.P(rank_value, className=rank_class, style={'color': color, 'margin': '0'}),
                html.Div(className='kpi-change', children=[
                    html.Span(arrow_int, style={'color': arrow_color_int}),
                    html.Span(f" {change_text_int}", style={'color': arrow_color_int})
                ])
            ]),
            html.Div(className='ranking-item', children=[
                html.P("국내", className='ranking-label'),
                html.P(domestic_rank_value, className=domestic_rank_class, style={'color': color, 'margin': '0'}),
                html.Div(className='kpi-change', children=[
                    html.Span(arrow_dom, style={'color': arrow_color_dom}),
                    html.Span(f" {change_text_dom}", style={'color': arrow_color_dom})
                ])
            ])
        ])
    ], className='kpi-card')

def create_kpi_card(title, value, prev_value, suffix='', color='gray'):
    """
    일반적인 KPI 카드를 생성합니다.
    """
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

def get_reputation_trend_figure(df_reputation):
    """
    평가기관별 국제 순위 추이 그래프를 생성합니다.
    """
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

def get_research_trend_figure(df_research):
    """
    연구비 및 피인용지수 추이 그래프를 생성합니다.
    """
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

def get_cooperation_trend_figure(df_cooperation):
    """
    산학협력 추이 그래프를 생성합니다.
    """
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

def get_global_trend_figure(df_global):
    """
    외국인 유학생 수 추이 그래프를 생성합니다.
    """
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
