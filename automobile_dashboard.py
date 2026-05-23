"""
Final Project - Part 2: Automobile Sales Dashboard
XYZAutomotives — Interactive Recession Analysis Dashboard
Run with: python automobile_dashboard.py
Then open browser at: http://127.0.0.1:8050
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ── Load Data ──────────────────────────────────────────────────────────────
df = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/'
    'historical_automobile_sales.csv'
)

year_list = sorted(df['Year'].unique().tolist())

# ── App Initialization ──────────────────────────────────────────────────────
app = Dash(__name__)

# ── TASK 2.1: Layout with Title ─────────────────────────────────────────────
app.layout = html.Div([

    html.H1(
        'Automobile Sales Statistics Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': '28px',
            'font-family': 'Arial, sans-serif',
            'padding': '20px',
            'background-color': '#f9f9f9',
            'border-bottom': '2px solid #ddd'
        }
    ),

    # ── TASK 2.2: Dropdown menus ─────────────────────────────────────────
    html.Div([
        html.Div([
            html.Label('Select Statistics Report:', style={'font-weight': 'bold', 'font-size': '16px'}),
            dcc.Dropdown(
                id='dropdown-statistics',
                options=[
                    {'label': '📉 Recession Period Statistics', 'value': 'Recession Period Statistics'},
                    {'label': '📅 Yearly Statistics',           'value': 'Yearly Statistics'}
                ],
                placeholder='Select a report type...',
                value='Recession Period Statistics',
                style={'width': '100%', 'font-size': '14px'}
            )
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label('Select Year:', style={'font-weight': 'bold', 'font-size': '16px'}),
            dcc.Dropdown(
                id='select-year',
                options=[{'label': str(y), 'value': y} for y in year_list],
                placeholder='Select a year...',
                style={'width': '100%', 'font-size': '14px'}
            )
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'})

    ], style={
        'display': 'flex',
        'justify-content': 'space-around',
        'padding': '20px',
        'background-color': '#ffffff',
        'border-bottom': '1px solid #eee'
    }),

    # ── TASK 2.3: Output Divisions ────────────────────────────────────────
    html.Div([
        html.Div(id='output-container', className='chart-grid',
                 style={'width': '100%'})
    ], style={'padding': '20px', 'background-color': '#f4f4f4', 'min-height': '80vh'})

], style={'font-family': 'Arial, sans-serif'})


# ── TASK 2.4 & 2.5 & 2.6: Callbacks ─────────────────────────────────────────
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_year_dropdown(selected_statistics):
    """Disable year dropdown when Recession report is selected."""
    return selected_statistics == 'Recession Period Statistics'


@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):

    # ── TASK 2.5: Recession Period Statistics ────────────────────────────
    if selected_statistics == 'Recession Period Statistics':
        rec_data = df[df['Recession'] == 1]

        # Chart 1: Average Automobile Sales by Year (line)
        yearly_rec_sales = rec_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(
            yearly_rec_sales, x='Year', y='Automobile_Sales',
            title='<b>Average Automobile Sales During Recession</b>',
            markers=True,
            color_discrete_sequence=['#E63946']
        ).update_layout(title_x=0.5))

        # Chart 2: Average Sales by Vehicle Type (bar)
        avg_sales_vehicle = rec_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart2 = dcc.Graph(figure=px.bar(
            avg_sales_vehicle, x='Vehicle_Type', y='Automobile_Sales',
            title='<b>Average Sales by Vehicle Type (Recession)</b>',
            color='Vehicle_Type',
            color_discrete_sequence=px.colors.qualitative.Set2
        ).update_layout(title_x=0.5, showlegend=False))

        # Chart 3: Pie — Advertising Expenditure Share by Vehicle Type
        exp_rec = rec_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart3 = dcc.Graph(figure=px.pie(
            exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
            title='<b>Advertising Expenditure Share by Vehicle Type (Recession)</b>',
            color_discrete_sequence=px.colors.qualitative.Pastel
        ).update_layout(title_x=0.5))

        # Chart 4: Unemployment Rate Effect on Sales (bar)
        unemp_data = rec_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index() \
            if 'unemployment_rate' in rec_data.columns else \
            rec_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()

        unemp_col = 'unemployment_rate' if 'unemployment_rate' in rec_data.columns else 'Unemployment_Rate'

        chart4 = dcc.Graph(figure=px.bar(
            unemp_data, x=unemp_col, y='Automobile_Sales',
            color='Vehicle_Type',
            title='<b>Effect of Unemployment Rate on Sales (Recession)</b>',
            color_discrete_sequence=px.colors.qualitative.Set1
        ).update_layout(title_x=0.5))

        return [
            html.Div([chart1, chart2], style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px'}),
            html.Div([chart3, chart4], style={'display': 'flex', 'gap': '20px'})
        ]

    # ── TASK 2.6: Yearly Statistics ───────────────────────────────────────
    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = df[df['Year'] == input_year]

        # Chart 1: Monthly Automobile Sales (line)
        monthly_sales = df.groupby('Month')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(
            monthly_sales, x='Month', y='Automobile_Sales',
            title=f'<b>Monthly Automobile Sales — {input_year}</b>',
            markers=True,
            color_discrete_sequence=['#457B9D']
        ).update_layout(title_x=0.5))

        # Chart 2: Monthly Advertising Expenditure (line)
        monthly_adv = yearly_data.groupby('Month')['Advertising_Expenditure'].sum().reset_index()
        chart2 = dcc.Graph(figure=px.line(
            monthly_adv, x='Month', y='Advertising_Expenditure',
            title=f'<b>Monthly Advertising Expenditure — {input_year}</b>',
            markers=True,
            color_discrete_sequence=['#2A9D8F']
        ).update_layout(title_x=0.5))

        # Chart 3: Vehicle Type Sales (bar)
        vehicle_sales = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
        chart3 = dcc.Graph(figure=px.bar(
            vehicle_sales, x='Vehicle_Type', y='Automobile_Sales',
            title=f'<b>Sales by Vehicle Type — {input_year}</b>',
            color='Vehicle_Type',
            color_discrete_sequence=px.colors.qualitative.Bold
        ).update_layout(title_x=0.5, showlegend=False))

        # Chart 4: Advertising Expenditure by Vehicle Type (pie)
        adv_vehicle = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart4 = dcc.Graph(figure=px.pie(
            adv_vehicle, values='Advertising_Expenditure', names='Vehicle_Type',
            title=f'<b>Advertising Share by Vehicle Type — {input_year}</b>',
            color_discrete_sequence=px.colors.qualitative.Pastel
        ).update_layout(title_x=0.5))

        return [
            html.Div([chart1, chart2], style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px'}),
            html.Div([chart3, chart4], style={'display': 'flex', 'gap': '20px'})
        ]

    return html.Div(
        '⬆️ Please select a statistics type (and a year for Yearly Statistics).',
        style={'text-align': 'center', 'color': 'gray', 'font-size': '18px', 'margin-top': '50px'}
    )


# ── Run ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=8050)
