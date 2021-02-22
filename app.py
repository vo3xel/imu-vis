from os import getcwd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json
import datetime
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

convert = lambda x: datetime.datetime.fromtimestamp(float(x) / 1e3)

options = []
for filename in os.listdir(getcwd() + '/data'):
    if filename.endswith(".csv"):
        options.append({'value': str(filename), 'label': str(convert(filename.split(".")[0])).split('.')[0]})
        continue
    else:
        continue

label_mapping = {'1': 'GYRO_X','2': 'GYRO_Y', '3': 'GYRO_Z','4': 'ACC_X','5': 'ACC_Y', '6': 'ACC_Z'}

filepath = getcwd() + "/data/1613979587872.csv"

convert = lambda x: datetime.datetime.fromtimestamp(float(x) / 1e3)

df = pd.read_csv(filepath, sep=",", parse_dates=['timestamp'], date_parser=convert).drop(['measurement_id'], axis='columns')

sensorIdx = {1: 'GYRO_X',2: 'GYRO_Y', 3: 'GYRO_Z',4: 'ACC_X',5: 'ACC_Y', 6: 'ACC_Z'}

def create_imu_figures(data_frame,signal_id):
    imu_df = data_frame.query('sensor_setup_id == ' + str(signal_id))
    imu_df['sensor_setup_id'].map(sensorIdx)
    imu_df_fig = px.line(imu_df,x="timestamp",y="signal_value")
    return imu_df_fig

def create_map_figure(data_frame):
    df_map = data_frame.query('sensor_setup_id == 7 | sensor_setup_id == 8')
    df_map = df_map.pivot(index='timestamp', columns='sensor_setup_id')
    df_map = df_map.reset_index()
    df_map.columns = ['timestamp','lat','lon']
    fig_map = px.line_mapbox(df_map, lat='lat', lon='lon', zoom=10, height=600)
    fig_map.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=10, mapbox_center_lat = df_map.loc[0,'lat'], mapbox_center_lon = df_map.loc[0,'lon'], margin={"r":0,"t":0,"l":0,"b":0})
    return fig_map

gyro_x_fig = create_imu_figures(df,1)
gyro_y_fig = create_imu_figures(df,2)
gyro_z_fig = create_imu_figures(df,3)

acc_x_fig = create_imu_figures(df,4)
acc_y_fig = create_imu_figures(df,5)
acc_z_fig = create_imu_figures(df,6)

fig_map = create_map_figure(df)

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='INSECTT IMU data visualizer'),
        dcc.Dropdown(
            id='csv-dropdown',
            options=options
        ),
        html.Div(id='dd-output-container')
    ], className='row'),
    html.Div([
        html.H1(children='GYRO_X'),
        html.Div(children='''
            GYRO_X values with 20Hz
        '''),
        dcc.Graph(
            id='graph1',
            figure=gyro_x_fig
        ),  
    ], className='row'),
    html.Div([
        html.H1(children='GYRO_Y'),
        html.Div(children='''
            GYRO_Y values with 20Hz
        '''),
        dcc.Graph(
            id='graph2',
            figure=gyro_y_fig
        ),  
    ], className='row'),
    html.Div([
        html.H1(children='GYRO_Z'),
        html.Div(children='''
            GYRO_Z values with 20Hz
        '''),
        dcc.Graph(
            id='graph3',
            figure=gyro_z_fig
        ),  
    ], className='row'),        
    html.Div([
        html.H1(children='ACC_X'),
        html.Div(children='''
            ACC_X values with 20Hz
        '''),
        dcc.Graph(
            id='graph4',
            figure=acc_x_fig
        ),  
    ], className='row'),
    html.Div([
        html.H1(children='ACC_Y'),
        html.Div(children='''
            ACC_Y values with 20Hz
        '''),
        dcc.Graph(
                id='graph5',
                figure=acc_y_fig
        ),  
    ], className='row'),
    html.Div([
        html.H1(children='ACC_Z'),
        html.Div(children='''
            ACC_Z values with 20Hz
        '''),
        dcc.Graph(
            id='graph6',
            figure=acc_z_fig
        ),  
    ], className='row'),        
    html.Div([
        html.H1(children='GPS'),
        html.Div(children='''
            GPS track of current drive
        '''),
        dcc.Graph(
            id='graph7',
            figure=fig_map
        ),  
    ], className='row'),
])

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('csv-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)