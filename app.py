import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import  Output, Input

import dash_table
from ipyslickgrid import show_grid

from markdown import Markdown
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

import pandas as pd
import datetime

from charts import fig_scatter, figpie,  continent_table

data_pox = pd.read_csv('df_monkeyPoxTimeSerie.csv')
date = data_pox['date'].unique()

## global data #####
global_cases = data_pox[data_pox['Country']=='World']['acc_confirmed'].max()
total_countries = len(data_pox.Country.unique())
number_of_days = len(data_pox.date.unique())

#### set datatable ####

df_table = data_pox.groupby('Country')['acc_confirmed'].max().reset_index().sort_values(by='acc_confirmed', ascending=False)
table = dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)


#### infos table continents

#table_continents = dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)


                 




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], 
                meta_tags=[{'name':'viewpoort', 
                            'content':'width=device-width, initial-scale= 1.0'}])

####  markdown text ###
Markdown_text = '''
Visualizing the data produced by the 
[Global.health](https://github.com/globaldothealth/monkeypox) 
team on the 2022 monkeypox outbreak.
'''


                     ##### CONTROLS SETTINGS ####

control = dbc.Card([
   
    html.Div([
        dbc.CardBody([
        dbc.Label('Last Update : ' + str(data_pox['date'].iloc[-1]), className='text-warning d-inline-block badge', style={'padding-left':'0px'}),
        dbc.Label('World & Country Data Informations',  className= 'text-uppercase, font-weight-bold  p-2 text-left')
        ]),
       
       # single  choice drop down
        dcc.Dropdown(id='my_dropdown2',
            options=[{'label':c, 'value':c} for  c in sorted(data_pox.Country.unique())],
            value='World',
            multi = False,
            style = {'width': '75%'}), 
       
    ]),
    html.Div([
        dbc.CardBody([
        html.P(f" {global_cases:,.0f} MonkeyPox Confirmed Cases"),
        html.P(f"{total_countries} Countries Concerned"),
        html.P(f"{number_of_days} days of Epidemy")
        
        ])
    ])
])

control_comparator = dbc.Card([
    html.Div([
        dbc.CardBody([
        dbc.Label('Last Update : ' + str(data_pox['date'].iloc[-1]), className='text-warning d-inline-block badge', style={'padding-left':'0px'}),
        dbc.Label('World & Country Data Informations',  className= 'text-uppercase, font-weight-bold  p-2 text-left')
        ]),
        
        #### multi choice dropdown fig 1
        dcc.Dropdown(id= 'my_dropdown', 
                     placeholder= 'select countries', 
                     options= [{'label':c, 'value':c} for c  in sorted(data_pox.Country.unique())],
                     value = data_pox.Country.unique()[-1], 
                     multi = True, 
                     style = {'width':'75%'}),
       
        
        
    ])
    
])

######## CONTROL MAP #######
control_map = dbc.Card([
    html.Div([
        dbc.CardBody([
        dbc.Label('Last Update : ' + str(data_pox['date'].iloc[-1]), className='text-warning d-inline-block badge', style={'padding-left':'0px'}),
        dbc.Label('World & Country Data Informations',  className= 'text-uppercase, font-weight-bold  p-2 text-left')
        ]),
        
       
        
    ])
    ])

###### CONTROL TABLE #####
control_table = dbc.Card([
    html.Div([
        dbc.CardBody([
        dbc.Label('Last Update : ' + str(data_pox['date'].iloc[-1]), className='text-warning d-inline-block badge', style={'padding-left':'0px'}),
        dbc.Label('World & Country Data Informations',  className= 'text-uppercase, font-weight-bold  p-2 text-left')
        ]),
        
    ])
    ])

#### CONTROL REVIEW #####
control_review = dbc.Card([
    html.Div([
        dbc.CardBody([
        dbc.Label('Last Update : ' + str(data_pox['date'].iloc[-1]), className='text-warning d-inline-block badge', style={'padding-left':'0px'}),
        dbc.Label('World & Country Data Informations',  className= 'text-uppercase, font-weight-bold  p-2 text-left')
        ]),
        
    ])
    ])





             ### LAYOUT SETTINGS #####  

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
        dbc.Tabs([
            #### Section general  informations ####
            dbc.Tab(label='General Informations', 
                    id = 'Tb_1',
                    children=[
                        dbc.Row([
                        dbc.Col(control, md=3, className='align-top', style = {'display':'inline-block'}),
                        dbc.Col(dcc.Graph(id='BarLineChart'), md=9, style={'display':'inline-block'})
                        ],className  = 'd-flex flex-row pt-2')]),
            
            #### Section compared Country ####
            dbc.Tab(label = 'Compared Country',
                    children=[
                        dbc.Row([
                           dbc.Col(control_comparator, md=3, className='align-top', style  = {'display':'inline-block'}),
                           dbc.Col(dcc.Graph(id= 'ligne-graph'), md=9,  style = {'display': 'inline-block'}),
                           ], className = 'd-flex flex-row pt-2')
                        ]),
            
           #### Section Map ###
            dbc.Tab(label = 'Map', 
                    children=[
                        dbc.Row([
                          dbc.Col(control_map, md=3, className='align-top'),
                          dbc.Col(dcc.Graph(id='animated_map', figure=fig_scatter), md=9) ], className= 'd-flex flex-row pt-2')
                        ]),
            
            #### Section Datatable ####
             dbc.Tab(label = 'Datatable', 
                    children=[
                        dbc.Row([
                        dbc.Col(html.Div(control_table), width = 3),
                        dbc.Col(html.Div(dbc.Table.from_dataframe(df_table, 
                                                                  striped=True, 
                                                                  bordered= True, 
                                                                  hover= True,
                                                                  responsive=True, 
                                                                  style =  {'margin-top':'10px'},
                                                                  size=9
                                                                  ), className='overflow-scroll'), 
                                width=9)
                        
                          
                         
                          ],className= 'd-flex flex-row pt-2', justify='center')
                                     
                       
                        ]),
             
            
            
            #### Section review ####
           dbc.Tab(label = 'Cases per Continent', 
                    children=[
                        dbc.Row([
                            dbc.Col(control_review,   md=3, className = 'align-top'),
                            dbc.Col(dcc.Graph(id='review',  figure=figpie), md=5, style = {'display': 'inline-block'}),
                            dbc.Col(continent_table, md= 3, style = {'padding-top':'10em'})
                            
                        ],  className = 'd-flex flex-row  pt-2')
                        ]),
            
            ], active_tab = 'tab-0', className = 'nav nav-pills nav-fill tab-content'),
        
        
    
    ],className = 'd-flex flex-row'),
    
])


###### CALLBACK SETTINGS ####



### line graph callback for comparator section ####
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
                      font_family = 'Arial',
                      width=900, 
                      height = 400,
                      xaxis  = dict(
                                    color = 'black', 
                                    showline =  False,
                                    showgrid = True,
                                    showticklabels=True, 
                                    ticks = 'outside',
                                    tickfont = dict(
                                        family  = 'Arial',
                                        color = 'grey',
                                        size=12,
                                       
                                    )),
                    yaxis=dict(
                                   color='black',
                                    showgrid=True,
                                    showticklabels=True,
                                    ticks='outside',
                                    tickfont=dict(
                                        family='Arial',
                                        color='grey',
                                        size=12
                       )
                       ) 
                      
                      
                      
                      
                      
                      
                      )
    
    return fig


    




@app.callback(Output('BarLineChart', 'figure'),  [Input('my_dropdown2', 'value')])
def new_barChart(value):
    df_lastbar =  data_pox[data_pox['Country']==value]
    df_lastbar['Rolling Ave.'] = df_lastbar['new_daily_cases'].rolling(window=7).mean().fillna(0)
    
    
    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = df_lastbar['acc_confirmed'].iloc[-1],
        delta = {"reference": df_lastbar['acc_confirmed'].iloc[-2], 
                 "valueformat": ".0f",
                 'font':{'size':15}},
        number = {'font' : {'size':15}},
        
        title = {"text": "<b>"+"Total Cases" + "</b>",  
                 'font':{'size':15}},
        domain = {'y': [0, 1], 'x': [0.25, 0.75]}))
    
    fig.add_trace(go.Bar(
            x = df_lastbar['date'].tail(30),
            y = df_lastbar['new_daily_cases'].tail(30),
            name = 'Daily confirmed Cases',
            marker_color = 'rgb(158,202,225)',
            marker_line_color = 'rgb(8, 48, 107)',
            opacity = 0.5,
            hoverinfo = 'text',
            hovertext = 
            '<b>Date</b>: '  + df_lastbar['date'].tail(30).astype(str) + '<br>' +
            '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in df_lastbar['new_daily_cases'].tail(30)] + '<br>' 
            
            
            )),
    
    
    fig.add_trace(go.Scatter(
        mode = 'lines',
        x = df_lastbar['date'].tail(30),
        y = df_lastbar['Rolling Ave.'].tail(30),
        name = 'Rolling Average oof last 7 days',
        line = dict(color='blue', width=2),
        hoverinfo = 'text',
        hovertext =
        '<b>Date</b>: ' +df_lastbar['date'].tail(30).astype(str) + '<br>' +
        '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in df_lastbar['Rolling Ave.'].tail(30)] + '<br>'
        
    ))
    
    fig.update_layout(title = {'text' :  '<b>' + value.upper() +  ' </b>' + ' : Last 30 Days Daily Confirmed Cases ',
                               'y': 0.93,
                               'x': 0.08,
                               'xanchor':'left',
                               'yanchor':'top'
                              },
                     
                      template = 'plotly_white',
                      legend =  {'orientation': 'h',
                                 'xanchor':'center', 
                                 'x':0.5, 
                                 'y':-0.3},
                      hovermode = 'closest',
                      margin = dict(r=0),
                      height= 400, 
                      width=900,
                      xaxis  = dict(
                                    color = 'black', 
                                    showline =  False,
                                    showgrid = True,
                                    showticklabels=True, 
                                    ticks = 'outside',
                                    tickfont = dict(
                                        family  = 'Arial',
                                        color = 'grey',
                                        size=12,
                                       
                                    )),
                        yaxis=dict(title='Daily Confirmed Cases',
                                   color='black',
                                    showgrid=True,
                                    showticklabels=True,
                                    ticks='outside',
                                    tickfont=dict(
                                        family='Arial',
                                        color='grey',
                                        size=12
                       )
                       )
                      
                      
                      
                      
                      ),
    
    return fig

    

    
    
    



if __name__ == '__main__':
    app.run_server(debug=True, port = 3000 )