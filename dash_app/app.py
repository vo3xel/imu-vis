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
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

convert = lambda x: datetime.datetime.fromtimestamp(float(x) / 1e3)

options = []
df = {}

for filename in os.listdir(getcwd() + '/data'):
    if filename.endswith(".csv"):
        df[str(filename)] = pd.read_csv(getcwd() + '/data/' + filename, sep=",", parse_dates=['timestamp'], date_parser=convert).drop(['measurement_id'], axis='columns')
        options.append({'value': str(filename), 'label': str(convert(filename.split(".")[0])).split('.')[0]})

first_file = list(df.keys())[0]

convert = lambda x: datetime.datetime.fromtimestamp(float(x) / 1e3)

sensorIdx = {1: 'GYRO_X',2: 'GYRO_Y', 3: 'GYRO_Z',4: 'ACC_X',5: 'ACC_Y', 6: 'ACC_Z'}

def create_imu_figures(filename,signal_id):
    data_frame = df[filename]
    imu_df = data_frame.query('sensor_setup_id == ' + str(signal_id))
    imu_df['sensor_setup_id'].map(sensorIdx)
    imu_df_fig = px.line(imu_df,x="timestamp",y="signal_value")
    return imu_df_fig

def create_map_figure(filename):
    data_frame = df[filename]
    df_map = data_frame.query('sensor_setup_id == 7 | sensor_setup_id == 8')
    df_map = df_map.pivot(index='timestamp', columns='sensor_setup_id')
    df_map = df_map.reset_index()
    df_map.columns = ['timestamp','lat','lon']
    fig_map = px.line_mapbox(df_map, lat='lat', lon='lon', zoom=15, height=600)
    fig_map.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=15, mapbox_center_lat = df_map.loc[0,'lat'], mapbox_center_lon = df_map.loc[0,'lon'], margin={"r":0,"t":0,"l":0,"b":0})
    return fig_map

def imu_sensor_div(signal_id):
    return html.Div([
        html.H1(children=sensorIdx[signal_id]),
        html.Div(children='''
            {sid} values with 20Hz
        '''.format(sid=sensorIdx[signal_id])),
        dcc.Graph(id=sensorIdx[signal_id]),  
    ], className='row')

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='INSECTT IMU data visualizer'),
        dcc.Dropdown(
            id='csv-dropdown',
            options=options,
            value=first_file
        ),
    ], className='row'),
    imu_sensor_div(1),
    imu_sensor_div(2),
    imu_sensor_div(3),        
    imu_sensor_div(4),
    imu_sensor_div(5),
    imu_sensor_div(6),        
    html.Div([
        html.H1(children='GPS'),
        html.Div(children='''
            GPS track of current drive
        '''),
        dcc.Graph(id='gps_map'),
    ], className='row'),
])

@app.callback(
    [dash.dependencies.Output(sensorIdx[1], 'figure'), dash.dependencies.Output(sensorIdx[2], 'figure'), dash.dependencies.Output(sensorIdx[3], 'figure'), \
    dash.dependencies.Output(sensorIdx[4], 'figure'), dash.dependencies.Output(sensorIdx[5], 'figure'), dash.dependencies.Output(sensorIdx[6], 'figure'), \
    dash.dependencies.Output('gps_map', 'figure') ],
    [dash.dependencies.Input('csv-dropdown', 'value')])
def update_output(value):
    gyro_x_fig = create_imu_figures(value,1)
    gyro_y_fig = create_imu_figures(value,2)
    gyro_z_fig = create_imu_figures(value,3)

    acc_x_fig = create_imu_figures(value,4)
    acc_y_fig = create_imu_figures(value,5)
    acc_z_fig = create_imu_figures(value,6)

    fig_map = create_map_figure(value)
    return gyro_x_fig, gyro_y_fig, gyro_z_fig, acc_x_fig, acc_y_fig, acc_z_fig, fig_map

if __name__ == '__main__':
    app.run_server(debug=False)