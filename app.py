import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import  Output, Input
from ipyslickgrid import show_grid
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

import pandas as pd
import datetime

data_pox = pd.read_csv('df_monkeyPox.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO], 
                meta_tags=[{'name':'viewpoort', 
                            'content':'width=device-width, initial-scale= 1.0'}])


##### Set left controls tools ####

control = dbc.Card([
    html.Div([
        dbc.Label('Overview', className = 'text-uppercase font-weight-bold'), 
        dcc.Dropdown(id= 'my_dropdown', 
                     placeholder= 'select countries', 
                     options= [{'label':c, 'value':c} for c  in sorted(data_pox.Country.unique())],
                     value = data_pox.Country.unique()[-1], 
                     multi = True),
        dbc.CardBody([
            html.P('Last Upgrade : ' + str(data_pox['date'].iloc[-1]),  
                   style = {'color': 'orange'}),
            
            html.H5(f"{str(data_pox[data_pox['Country']=='World']['acc_confirmed'].max())} World Confirmed Cases",  
                   className= 'bg-info',  style  = {'textAlign':'left'}),
            html.H6(f"{str(len(data_pox['Country'].unique()))} Countries ", 
                   className= "badge bg-info", style =  {'textAlign':'left'} )
        ])
    ])
], body=True)

app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            html.H1('MonkeyPox Data Explorer in non endemics Countries', className =  'text-left text-capitalize text-primary', 
                    style = {'display':'inline-block'}),
            dcc.Markdown('''
                         Visualizing the data produced by the [Global.health](https://github.com/globaldothealth/monkeypox) team on the 2022 monkeypox outbreak.
''')],width = 6),
        
    
        ], className = 'd-flex flex-row'),
    html.Hr(),
   
    dbc.Row([
        dbc.Col(control, md=4, className='align-top'),
        dbc.Col(dcc.Graph(id="ligne-graph"), md=8)
        
    ], align='center')
    
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
                  hover_data = ['acc_confirmed', 'confirmed', 'date'],
                  render_mode = 'svg',
                  labels={'acc_confirmed': 'Confirmed Cases', 
                          'confirmed': 'Daily Cases'},
                  template = 'plotly_white')
    fig.update_layout(title = {'text':"Monkey Pox Evolution"}, width=800)
    
    return fig
    



if __name__ == '__main__':
    app.run_server(debug=True, port = 3000 )