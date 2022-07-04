import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc



#  General Map data
mapbox_token = 'pk.eyJ1IjoiaGVyaWMiLCJhIjoiY2lwcHh2cHpwMDA1aWhybnBqbHQzOXQydCJ9.4CM5ZOcHIkaSnKnXywwJlA'
data_pox  =  pd.read_csv('df_MonkeyPoxTimeSerie.csv')
datapx_max = data_pox.groupby(['Country', 'latitude', 'longitude'])['acc_confirmed'].max().reset_index()
datapx_max = datapx_max.loc[~(datapx_max['Country'].isin(['World']))]


#general  map fig 
fig_scatter =  px.scatter_mapbox(
    datapx_max,
    lat = 'latitude',
    lon = 'longitude',
    hover_name = 'Country',
    size = 'acc_confirmed',
    color = 'acc_confirmed',
    color_continuous_scale=px.colors.sequential.Jet,
    size_max=40,
    zoom=1,
    height = 600,
    labels ={'acc_confirmed': '<b>Confirmed Cases</b>'},
    
    custom_data = ['acc_confirmed', 'Country']  
)

fig_scatter.update_layout( mapbox_accesstoken = mapbox_token, title = '<b>MonkeyPox</b>: Confirmed cases over thew World in non-endemics Countries')
fig_scatter.update_traces( name = '<b>Report</b>',
                  opacity = 0.8,
                  hoverinfo='name',
                  marker_symbol = 'circle',
                  text = datapx_max['Country'],
                  ids = datapx_max['acc_confirmed'],
                 hovertext=
                 '<b>Pays</b>: '  + datapx_max['Country'] + '<br>',
                 hovertemplate = '<br>'.join([
                     "Cas: %{customdata[0]}",
                     "Country: %{customdata[1]}",
                
                 ]))


#data pie  continent

data_pie =  data_pox.loc[~(data_pox['Country'].isin(['World']))]
data_pie  = data_pie.groupby(['Country', 'Continents'])['acc_confirmed'].max().reset_index()
datapie =  data_pie.groupby('Continents')['acc_confirmed'].sum().reset_index()
#print(datapie)

#pie  chart
labels =  list(datapie['Continents'])
values = list(datapie['acc_confirmed'])

figpie = go.Figure(
    data = [go.Pie(
        labels = labels,
        values  = values,
        textinfo = 'label+percent',
        textposition = 'inside',
        insidetextorientation = 'radial',
        hole = .3
        
    )]
)
figpie.update_layout(title = 'Percent of Cases per Continent', 
                     legend_orientation = 'h')


##### table  infos ###

continent_table = dbc.Table.from_dataframe(datapie, striped=True, bordered=True, hover=True)


                 