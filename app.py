import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import  Output, Input
from ipyslickgrid import show_grid
from markdown import Markdown
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

import pandas as pd
import datetime

data_pox = pd.read_csv('df_monkeyPoxTimeSerie.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO], 
                meta_tags=[{'name':'viewpoort', 
                            'content':'width=device-width, initial-scale= 1.0'}])

####  Set markdown text ###
Markdown_text = '''
Visualizing the data produced by the 
[Global.health](https://github.com/globaldothealth/monkeypox) 
team on the 2022 monkeypox outbreak.
'''


##### Set left controls tools ####

control = dbc.Card([
    html.Div([
        dbc.Label('Overview', className = 'text-uppercase font-weight-bold d-inline-block text-dark' ), 
        dbc.Label('Last Update : ' + str(data_pox['date'].iloc[-1]), className='text-warning d-inline-block font-italic badge', style={'padding-left':'15px'}),
        dcc.Dropdown(id= 'my_dropdown', 
                     placeholder= 'select countries', 
                     options= [{'label':c, 'value':c} for c  in sorted(data_pox.Country.unique())],
                     value = data_pox.Country.unique()[-1], 
                     multi = True),
        html.Hr(),
        dbc.Label('World & Country Data Informations',  className= 'text-uppercase, font-weight-bold  p-2 text-left'),
        dcc.Dropdown(id='my_dropdown2', className='dropdown open',
            options=[{'label':c, 'value':c} for  c in sorted(data_pox.Country.unique())],
            value='World',
            multi = False),
        dcc.Graph(id='indicator_confirmed', config = {'displayModeBar': False}),
        
        html.P('Global Cases :  '+ str(data_pox[data_pox['Country']=='World']['acc_confirmed'].max())),
        html.P('New Cases : '+ str(data_pox[data_pox['Country']=='World']['new_daily_cases'].iloc[-1]), 
               style = {'display':'inline-block'}),
        #dcc.Graph(id = 'indic'),
        html.Hr()
    ])
], body=True, style = {'padding-top': '15px', 'verticalAlign':'top'})

app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            html.H1('MonkeyPox Data Explorer in non endemics Countries', 
                    className =  'text-left text-capitalize text-primary', 
                    style = {'display':'inline-block'}),
            dcc.Markdown(children=Markdown_text)],width = 6),
        
    
        ], className = 'd-flex flex-row'),
    html.Hr(style = {'margin-top':'25px'}),
   
    dbc.Row([
        dbc.Col(control, md=3, className='align-top'),
        dbc.Col(dcc.Graph(id="ligne-graph"), md=9)
        
    ], className = 'd-flex flex-row')
    
])


@app.callback(Output('ligne-graph', 'figure'), [Input('my_dropdown', 'value')])
def update_ligneGraph(value):
    if type(value)!=str:
        df = data_pox[data_pox['Country'].isin(value)]
    else :
        df = data_pox[data_pox['Country']==value]
    fig = px.line(df, x='date', 
                  y = 'acc_confirmed', 
                  color = 'Country', 
                  line_shape = 'spline', 
                  hover_name = 'Country', 
                  hover_data = ['acc_confirmed', 'new_daily_cases', 'date'],
                  render_mode = 'svg',
                  labels={'acc_confirmed': 'Confirmed Cases', 
                          'new_daily_cases': 'Daily Cases'},
                  template = 'plotly_white')
    fig.update_layout(title = {'text': '<b>' + 'MonkeyPox : ' + '</b>' +  'Cumulative Confirmed Cases by Date, Country'},
                      font_family = 'Arial',width=800)
    
    return fig

@app.callback(Output('indicator_confirmed', 'figure'), [Input('my_dropdown2', 'value')])
def  update_indicator(value):
    value_confirmed = data_pox[data_pox['Country'].isin(value)]['acc_confirmed'].iloc[-1]- data_pox[data_pox['Country'].isin(value)]['acc_confirmed'].iloc[-2]
    delta_confirmed = data_pox[data_pox['Country'].isin(value)]['acc_confirmed'].iloc[-2]- data_pox[data_pox['Country'].isin(value)]['acc_confirmed'].iloc[-3]
    
    



if __name__ == '__main__':
    app.run_server(debug=True, port = 3000 )