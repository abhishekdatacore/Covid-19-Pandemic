import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
]

patients = pd.read_csv("state_wise_daily data file.csv")

# Summary counts
total = patients.shape[0]
active = patients[patients['Status'] == 'Confirmed'].shape[0]
recovered = patients[patients['Status'] == 'Recovered'].shape[0]
deaths = patients[patients['Status'] == 'Deceased'].shape[0]

# Dropdowns
options = [
    {'label':'All', 'value':'All'},
    {'label':'Hospitalized', 'value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased','value':'Deceased'}
]

options1 = [
    {'label':'All', 'value':'All'},
    {'label':'Mask', 'value':'Mask'},
    {'label':'Sanitizer','value':'Sanitizer'},
    {'label':'Oxygen','value':'Oxygen'}
]

options2 = [
    {'label':'All','value':'Status'},
    {'label':'Red Zone', 'value':'Red Zone'},
    {'label':'Blue Zone','value':'Blue Zone'},
    {'label':'Green Zone','value':'Green Zone'},
    {'label':'Orange Zone','value':'Orange Zone'}
]

App = dash.Dash(__name__, external_stylesheets=external_stylesheets)

App.layout = html.Div([

    # Title
    html.H1("COVID-19 DASHBOARD", style={'color':'#fff', 'text-align':'center'}),

    # Subtitle
    html.H3("A Data-Driven Analysis of Cases, Recoveries, and Deaths",
            style={'color':'white', 'text-align':'center'}),

    # Cards Row
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='text-light'),
                    html.H4(active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered Cases", className='text-light'),
                    html.H4(recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ],className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Deaths", className='text-light'),
                    html.H4(deaths, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ],className='col-md-3')
    ],className='row'),

    # Line + Pie
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='plot-graph', options=options1, value='All'),
                    dcc.Graph(id='graph')
                ],className='card-body')
            ],className='card bg-primary')   # Line chart card = blue
        ],className='col-md-6'),

        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='my_dropdown', options=options2, value='Red Zone', style={"width": "100%"}),
                    dcc.Graph(id='the_graph')
                ],className='card-body')
            ],className='card bg-success')   # Pie chart card = green
        ],className='col-md-6')
    ],className='row'),

    # Bar
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value='All'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card bg-warning')  # Bar chart card = yellow
        ], className='col-md-12')
    ],className='row')

], className= 'container',
    style={
            "backgroundColor": "black",
            "minHeight": "100vh",
            "padding": "20px"
})


# Bar chart callback
@App.callback(Output('bar','figure'), [Input('picker','value')])
def update_graph(type):
    fig = go.Figure()
    if type=='All':
        fig = go.Figure([go.Bar(x=patients['State'], y=patients['Total'])])
    elif type=="Hospitalized":
        fig = go.Figure([go.Bar(x=patients['State'], y=patients['Hospitalized'])])
    elif type=="Recovered":
        fig = go.Figure([go.Bar(x=patients['State'], y=patients['Recovered'])])
    elif type=="Deceased":
        fig = go.Figure([go.Bar(x=patients['State'], y=patients['Deceased'])])

    fig.update_layout(title="State Total Count", plot_bgcolor='orange',
                      width=1200, height=500,
                      xaxis=dict(automargin=True, tickangle=45))
    return fig


# Line chart callback
@App.callback(Output('graph','figure'), [Input('plot-graph','value')])
def generate_graph(type):
    fig = go.Figure()
    if type=='All':
        fig.add_trace(go.Scatter(x=patients['Status'], y=patients['Total'], mode='lines', name='Total'))
    elif type=='Mask':
        fig.add_trace(go.Scatter(x=patients['Status'], y=patients['Mask'], mode='lines', name='Mask'))
    elif type=='Sanitizer':
        fig.add_trace(go.Scatter(x=patients['Status'], y=patients['Sanitizer'], mode='lines', name='Sanitizer'))
    elif type=='Oxygen':
        fig.add_trace(go.Scatter(x=patients['Status'], y=patients['Oxygen'], mode='lines', name='Oxygen'))

    fig.update_layout(title="Commodities Total Count", plot_bgcolor='pink',
                      width=600, height=400,
                      xaxis=dict(automargin=True))
    return fig


# Pie chart callback
@App.callback(Output('the_graph','figure'),
              [Input('my_dropdown','value')])
def generate_pie(my_dropdown):
    piechart = px.pie(data_frame=patients, names=my_dropdown, hole=0.3,
                      width=600, height=400,
                      title="Zone Distribution")
    return piechart


if __name__ == '__main__':
    App.run(debug=True)

