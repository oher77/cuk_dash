from dash import html
import pandas as pd
import re

# 공통 컴포넌트: 순위 KPI 카드 생성
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
                arrow_color = '#dc3545'
                change_text = f"{abs(change):.0f}"
            elif change > 0:
                arrow = '▼'
                arrow_color = '#007bff'
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

# 공통 컴포넌트: 일반 KPI 카드 생성
def create_kpi_card(title, value, prev_value, suffix='', color='gray'):
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
        elif suffix == '억원':
            change_text = f"{change:.0f}"
            display_value = f"{current_val:.0f}{suffix}"
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
