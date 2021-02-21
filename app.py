from os import getcwd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json
import datetime

app = dash.Dash(__name__)

label_mapping = {'1': 'GYRO_X','2': 'GYRO_Y', '3': 'GYRO_Z','4': 'ACC_X','5': 'ACC_Y', '6': 'ACC_Z'}

filepath = getcwd() + "/data/1613328522385.csv"

convert = lambda x: datetime.datetime.fromtimestamp(float(x) / 1e3)

df = pd.read_csv(filepath, sep=",", parse_dates=['timestamp'], date_parser=convert).drop(['measurement_id'], axis='columns')

sensorIdx = {1: 'GYRO_X',2: 'GYRO_Y', 3: 'GYRO_Z',4: 'ACC_X',5: 'ACC_Y', 6: 'ACC_Z'}

gyro_x_df = df.query('sensor_setup_id == 1')
sensors = gyro_x_df['sensor_setup_id'].map(sensorIdx)
gyro_x_fig = px.line(gyro_x_df,x="timestamp",y="signal_value")

gyro_y_df = df.query('sensor_setup_id == 2')
sensors = gyro_y_df['sensor_setup_id'].map(sensorIdx)
gyro_y_fig = px.line(gyro_y_df,x="timestamp",y="signal_value")

gyro_z_df = df.query('sensor_setup_id == 3')
sensors = gyro_z_df['sensor_setup_id'].map(sensorIdx)
gyro_z_fig = px.line(gyro_z_df,x="timestamp",y="signal_value")

acc_x_df = df.query('sensor_setup_id == 4')
sensors = acc_x_df['sensor_setup_id'].map(sensorIdx)
acc_x_fig = px.line(acc_x_df,x="timestamp",y="signal_value")

acc_y_df = df.query('sensor_setup_id == 5')
sensors = acc_y_df['sensor_setup_id'].map(sensorIdx)
acc_y_fig = px.line(acc_y_df,x="timestamp",y="signal_value")

acc_z_df = df.query('sensor_setup_id == 6')
sensors = acc_z_df['sensor_setup_id'].map(sensorIdx)
acc_z_fig = px.line(acc_z_df,x="timestamp",y="signal_value")

df_map =  df.query('sensor_setup_id == 7 | sensor_setup_id == 8')

df_map = df_map.pivot(index='timestamp', columns='sensor_setup_id')
df_map = df_map.reset_index()
df_map.columns = ['timestamp','lat','lon'] 

fig_map = px.line_mapbox(df_map, lat='lat', lon='lon', zoom=10, height=600)
fig_map.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=10, mapbox_center_lat = df_map.loc[0,'lat'], mapbox_center_lon = df_map.loc[0,'lon'], margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H1(children='GYRO_X'),

            html.Div(children='''
                GYRO_X values with 20Hz
            '''),

            dcc.Graph(
                id='graph1',
                figure=gyro_x_fig
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='GYRO_Y'),

            html.Div(children='''
                 GYRO_Y values with 20Hz
            '''),

            dcc.Graph(
                id='graph2',
                figure=gyro_y_fig
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='GYRO_Z'),

            html.Div(children='''
                GYRO_Z values with 20Hz
            '''),

            dcc.Graph(
                id='graph3',
                figure=gyro_z_fig
            ),  
        ], className='six columns'),        
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.Div([
            html.H1(children='ACC_X'),

            html.Div(children='''
                ACC_X values with 20Hz
            '''),

            dcc.Graph(
                id='graph4',
                figure=acc_x_fig
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='ACC_Y'),

            html.Div(children='''
                 ACC_Y values with 20Hz
            '''),

            dcc.Graph(
                id='graph5',
                figure=acc_y_fig
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='ACC_Z'),

            html.Div(children='''
                ACC_Z values with 20Hz
            '''),

            dcc.Graph(
                id='graph6',
                figure=acc_z_fig
            ),  
        ], className='six columns'),        
    ], className='row'),
    html.Div([
        html.Div([
            html.H1(children='GPS'),

            html.Div(children='''
                GPS track of current drive
            '''),

            dcc.Graph(
                id='graph7',
                figure=fig_map
            ),  
        ], className='six columns')     
    ], className='row'),
])

if __name__ == '__main__':
    app.run_server(debug=True)