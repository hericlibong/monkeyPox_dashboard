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

## global cases
global_cases = data_pox[data_pox['Country']=='World']['acc_confirmed'].max()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO], 
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
        dbc.Label('Overview', className = 'text-uppercase font-weight-bold d-inline-block text-dark' ), 
        dbc.Label('Last Update : ' + str(data_pox['date'].iloc[-1]), className='text-warning d-inline-block font-italic badge', style={'padding-left':'15px'}),
        
        ### Global cases
        dbc.Label('Global Cases :  '+ str(global_cases)),
        
        #### multi choice dropdown fig 1
        dcc.Dropdown(id= 'my_dropdown', 
                     placeholder= 'select countries', 
                     options= [{'label':c, 'value':c} for c  in sorted(data_pox.Country.unique())],
                     value = data_pox.Country.unique()[-1], 
                     multi = True),
        html.Hr(),
        dbc.Label('World & Country Data Informations',  className= 'text-uppercase, font-weight-bold  p-2 text-left'),
       
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
        
        html.Hr()
    ])
], body=True, style = {'padding-top': '15px', 'verticalAlign':'top'})

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