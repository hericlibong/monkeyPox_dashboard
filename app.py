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

data_pox = pd.read_csv('df_monkeyPoxTimeSerie.csv')
date = data_pox['date'].unique()

## global cases
global_cases = data_pox[data_pox['Country']=='World']['acc_confirmed'].max()

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
        dcc.Dropdown(id='my_dropdown2', className='dropdown open',
            options=[{'label':c, 'value':c} for  c in sorted(data_pox.Country.unique())],
            value='World',
            multi = False),
        dcc.Graph(id='indicator_confirmed', config = {'displayModeBar': False},  style={'padding-top':'15px'}),
        dash_table.DataTable(id='datatable', 
                             style_cell={'font-family':'Arial'},
                             style_data_conditional=[{'if' :{'column_id':'labels'},
                                                      'textAlign':'left'}] + [{
                                                          'if':{'row_index':'odd'},
                                                          'backgroundColor': 'rgb(248, 248, 248)'
                                                          }], style_header={
                                                              'backgroundColor': 'rgb(230, 230,  230)',
                                                              'fontWeight':'bold',
                                                              'textAlign':'left'}),
        
       
    ])
], body=True, style = {'padding-top': '15px', 'verticalAlign':'top'})

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
                     multi = True),
        
        
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
ontrol_review = dbc.Card([
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
                    children=[
                        dbc.Row([
                        dbc.Col(control, md=3, className='align-top'),
                        
                        dbc.Col(dcc.Graph(id='BarLineChart'), md=9)
                        ],className  = 'd-flex flex-row pt-2')]),
            #### Section compared Country ####
            dbc.Tab(label = 'Compared Country',
                    children=[
                        dbc.Row([
                           dbc.Col(control_comparator, md=3, className='align-top'),
                           dbc.Col(dcc.Graph(id= 'ligne-graph'), md=9)
                           ], className = 'd-flex flex-row pt-2')
                        ]),
            
           #### Section Map ###
            dbc.Tab(label = 'Map', 
                    children=[
                        dbc.Row([
                          dbc.Col(control_map, md=3, className='align-top'),
                          dbc.Col(dcc.Graph(id='animated_map'), md =9) ], className= 'd-flex flex-row pt-2')
                        ]),
            
            #### Section Datatable ####
             dbc.Tab(label = 'Datatable', 
                    children=[
                        dbc.Row([
                          dbc.Col(control_map, md=3, className='align-top'),
                          dbc.Col(dcc.Graph(id='table'), md =9) 
                        ], className= 'd-flex flex-row pt-2')
                        ]),
            
            
            
            #### Section review ####
           dbc.Tab(label = 'Review', 
                    children=[
                        dbc.Row([
                          dbc.Col(control_map, md=3, className='align-top'),
                          dbc.Col(dcc.Graph(id='review'), md =9) 
                        ], className= 'd-flex flex-row pt-2')
                        ]),
            
            ], active_tab = 'General  Informations', className = 'nav nav-pills nav-fill'),
        
        
    
    ],className = 'd-flex flex-row'),
    
])


###### CALLBACK SETTINGS ####

#@app.callback(Output("tab-content", "children"),[Input("tabs", "active_tab")])


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
                      font_family = 'Arial',width=800)
    
    return fig


### lineBarGraph callback for general information section ###
@app.callback(Output('BarLineChart', 'figure'), [Input('my_dropdown2', 'value')])
def update_BarLineChart(value):
    df_barchart= data_pox[data_pox['Country']==value]
    df_barchart['Rolling Ave.'] = df_barchart['new_daily_cases'].rolling(window=7).mean().fillna(0)
    
    return {
        'data' : [go.Bar(
            x = df_barchart['date'].tail(30),
            y = df_barchart['new_daily_cases'].tail(30),
            name = 'Daily Confirmed Cases', 
            marker = dict(color ='orange'),
            hoverinfo = 'text',
            hovertext = 
            '<b>Date</b>: ' + df_barchart['date'].tail(30).astype(str) + '<br>' +
            '<b>Daily Cases</b>: ' + [f'{x:,.0f}' for x in df_barchart['new_daily_cases'].tail(30)] + '<br>' +
            '<b>Country/b>: ' + df_barchart['Country'].tail(30).astype(str) + '<br>'
        ),
                  go.Scatter(
                      x = df_barchart['date'].tail(30),
                      y = df_barchart['Rolling Ave.'].tail(30),
                      mode = 'lines',
                      name = 'Rolling Average of the last 7 days - daily cases',
                      line = dict(width=2,  color='blue'),
                      hoverinfo = 'text',
                      hovertext = 
                       '<b>Date</b>: ' + df_barchart['date'].tail(30).astype(str) + '<br>' +
                       '<b>Daily Cases</b>: ' + [f'{x:,.0f}' for x in df_barchart['Rolling Ave.'].tail(30)] + '<br>' 
                      
                  )],
        'layout':go.Layout(
            title={'text': 'Last 30 Days Daily Confirmed Cases: ' + value,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'black',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='black',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Date</b>',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Daily Confirmed Cases</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )
                       )
        )
}
    
#####  Get Map Graph #####

 
# @app.callback(Output('animated_map', 'figure'),[Input('drop_map', 'value')])
# def get_map(value):
#     data_map = data_pox.loc[~(data_pox['Country'].isin(['World']))]
#     #data_map =  data_map.groupby(['Country', 'latitude', 'longitude'])['acc_confirmed'].max().reset_index()
#     fig = px.scatter_geo(data_map,
#                      lat='latitude',
#                      lon='longitude',
#                     hover_name='Country',
#                     size = 'acc_confirmed',
#                     size_max = 30,
#                     scope = 'world',
#                     color='Country',
#                     projection = 'equirectangular', 
#                     animation_frame='date')
#     return fig 
   
      
    





@app.callback(Output('indicator_confirmed', 'figure'), [Input('my_dropdown2', 'value')])
def  update_indicator(value):
    value_confirmed = data_pox[data_pox['Country']==value]['acc_confirmed'].iloc[-1] - data_pox[data_pox['Country']==value]['acc_confirmed'].iloc[-2]
    delta_confirmed = data_pox[data_pox['Country']==value]['acc_confirmed'].iloc[-2] - data_pox[data_pox['Country']==value]['acc_confirmed'].iloc[-3]
    return {
        'data': [go.Indicator(
            mode = 'number+delta',
            value = value_confirmed,
            delta = {'reference': delta_confirmed,
                     'position':'right',
                     'valueformat': ',g',
                     'relative':False,
                     'font':{'size':15}},
            number= {'valueformat':',',
                     'font':{'size':10}},
            domain = {'y': [1, 0.5], 'x':  [1, 0.5]}
            
        )],
        
        'layout': go.Layout(
            title = {'text': 'Count', 
                     'y': 1,
                   'x': 0.5,
                   'xanchor': 'right',
                   'yanchor': 'top'}, 
            font = dict(color='blue'),
            height= 50
    
        )
    }
    
@app.callback([Output('datatable', 'data'), Output('datatable', 'columns')], [Input('my_dropdown2', 'value')])
def get_table(value):
    table_df = data_pox.groupby(['Country']).agg(New=('new_daily_cases', 'last'), Total =('acc_confirmed', 'max')).reset_index()
    columns = ['New', 'Total']
    infos  = {
        'labels': columns,
        'data': [table_df[table_df['Country']==value][col].iloc[0] for col in columns]
        }
    table = pd.DataFrame(infos)
    data = table.to_dict('rows')
    header =[ {'id':'labels',  'name':'Cases'}, {'id':'data', 'name':'Total'}]
    return data, header
    
    
    



if __name__ == '__main__':
    app.run_server(debug=True, port = 3000 )