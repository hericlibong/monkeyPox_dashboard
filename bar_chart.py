import pandas as pd
import plotly.graph_objects as go
import random
import datapane as dp



# load csv files

CafRanking  = pd.read_csv('bar_chart_race_FIFA/data/afrika_rank.csv')
emoji = pd.read_csv('bar_chart_race_FIFA/data/emojiflags.csv')

#Data preparation

CafRanking = pd.merge(CafRanking, emoji[['country', 'flag']], 
                      left_on = 'country_team', 
                      right_on='country', 
                      how = 'inner')
CafRanking = CafRanking.drop(columns=['country'])

# Add color code

colors = []
    
for i in range(len(CafRanking['country_team'].unique())):
    colors.append('#%06X' % random.randint(0, 0xFFFFFF)) #create random colors
        
df_colors = CafRanking.drop_duplicates(subset=['country_team'], keep='first')  #drop duplicate to create df_colors with unique category
df_colors['code_color'] = colors
CafRanking = pd.merge(CafRanking, df_colors[['country_team', 'code_color']], how='inner', on = ['country_team'])# merge df_colors with entire dataframe


#building frame

list_dates = CafRanking['date'].unique().tolist()# List of unique dates

dict_keys = [str(i) for i in range(len(list_dates))]# list of Keys 

# Create dict frame

x_frame = {}

for d, f in zip(list_dates, dict_keys):
    dataframe = CafRanking[CafRanking['date']==d] 
    dataframe = dataframe.nlargest(n=10, columns=['total_points'])#nlargest(): select num bars on graph
                                                                    
    dataframe = dataframe.sort_values(by=['date', 'total_points'])
    x_frame[f]=dataframe


#Creat Figure

config = {'responsive':True}

fig = go.Figure( 
    data = [ 
           go.Bar(   
               x = x_frame['0']['total_points'],
               y = x_frame['0']['country_team'],
               orientation = 'h',
               text = x_frame['0']['flag'],
               texttemplate='%{y}%{text}<br>%{x}',
               textposition = 'outside',
               width = 0.8,
               marker = dict(color = x_frame['0']['code_color']),
               hoverlabel = dict(align='right'),
               hoverinfo = 'text',
               
               hovertext = 
                       '<b>Flag</b>: ' + x_frame['0']['flag'] + '<br>' +
                       '<b>Country</b>: ' + x_frame['0']['country_team'].astype(str) + '<br>'+
                       '<b>Points</b>: ' + x_frame['0']['total_points'].astype(str) + '<br>' +
                       '<b>FIFA Rank</b>: ' + x_frame['0']['rank'].astype(str) + '<br>'
                       '<b>Date</b>: ' + x_frame['0']['date'].astype(str) + '<br>'
                       
                       
              
           ),
        
    ],


# custom layout for data start
    layout= go.Layout(
        xaxis = dict(range=[0, 1800], autorange=False, 
                     title = dict(text = '<b> TOTAL POINTS</b>', font = dict(size=8)), 
                     tickfont=dict(size=8)),
        yaxis = dict(range = [-1, 10.5],
            autorange=False,
            showticklabels=False,
            tickfont = dict(size=25)),
        template = 'plotly_white',
        hovermode = 'closest',
        title = dict(text='<b>TOP 10 AFRICAN TEAMS CAF/FIFA RANKING RACE : 1992 - 2022</b>' + '<br>' +
                           '<b>Leader</b>: Nigeria '+ '<br>',
                     
                     font = dict(size=13), 
                     xanchor='center',
                     x=0.5,
                      font_family = 'Courier New, monospace'),
        
        #add button to layout
        updatemenus=[
            dict(type="buttons",
                 x=0.1,
                 y=-0.07,
                 direction = 'right',
                 buttons=[dict(label="Play",
                               method="animate",
                               args=[None,
                                     {"frame": {"duration": 350, "redraw": True},
                                      'transition':{'duration':175, 'easing':'linear'}, 
                                  'fromcurrent' : True}]),
                          dict(label="Pause",
                               method="animate",
                               args=[[None],{"frame": {"duration": 0, "redraw": True}, 
                                             "mode": "immediate","transition": {"duration": 0}}]),
                     
                     ])]),
    
    
    
    
    
    #     # add frame
    frames =  [
        go.Frame(
            data =[
                go.Bar(x=value['total_points'], 
                       y=value['country_team'], 
                       orientation='h', 
                       text =  value['flag'],
                       textfont = {'size': 12},        
                       marker = {'color':value['code_color']},
                       texttemplate='%{y}%{text}<br>%{x}',
                       hoverinfo =  'text',
                       hovertext = 
                       '<b>Flag</b>: ' + value['flag'].astype(str) + '<br>' +
                       '<b>Country</b>: ' + value['country_team'].astype(str) + '<br>'+
                       '<b>Points</b>: ' + value['total_points'].astype(str) + '<br>' +
                       '<b>FIFA Rank</b>: ' + value['rank'].astype(str) + '<br>'+
                       '<b>Date</b>: ' + value['date'] + '<br>'
                        
                      ),
              
                
                
               
                ],# custom frame layout for running frame
            layout = go.Layout(
                xaxis = dict(range = [0, 1800],autorange=False, tickfont=dict(size=8)),
                yaxis = dict(range = [-1, 10.5], autorange=False, tickfont=dict(size=8, color=value['code_color'].values[9]), 
                              showticklabels=False),
                 hovermode = 'closest',
                title = dict(text='<b>TOP 10 AFRICAN TEAMS CAF/FIFA RANKING RACE : </b>' +str(value['date'].values[0]) + '<br>' +
                                '<b> Current Leader  : </b>' + str(value['country_team'].values[9]) + str(value['flag'].values[9]) + '<br>'+ 
                                 '<b> FIFA Leader Rank </b> :' + str(value['rank'].values[9]),
                             font = dict(size=13),
                             xanchor = 'center', 
                             yanchor = 'top', 
                             font_family = 'Courier New, monospace'
                             
                             
                ),
               )
        )
        for key, value in x_frame.items()
    ],

)

fig.update_layout(template = 'plotly_white') 
fig.update_yaxes(automargin=True)


#fig.update_xaxes(nticks = 20)

fig.show(config = config)


#add final stats

#dp.Report(dp.Plot(fig, responsive =True)).upload(name='top ten african football team ranking race4', open = True)


    