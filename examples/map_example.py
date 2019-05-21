import folium
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

FILE = "Seattle_Real_Time_Fire_911_Calls.csv" 
SEATTLE_COORDINATES = (47.6062, -122.3321)
data = pd.read_csv(FILE)
 
# for speed purposes
MAX_RECORDS = 10
  
# create empty map zoomed in on San Francisco
map = folium.Map(location=SEATTLE_COORDINATES, zoom_start=12)
 
# add a marker for every record in the filtered data, use a clustered view
for _, row in data[0:MAX_RECORDS].iterrows():
  popup = folium.Popup(row['Address'], max_width=100)
  html_str="""
     <a href="https://www.ibm.com/" target="_blank"> Details.</a> 
      """
  iframe = folium.IFrame(html=html_str, width=100, height=50)
  popup = folium.Popup(iframe, max_width=2650)
  folium.Marker([row['Latitude'], row['Longitude']], popup=popup).add_to(map)
map.save("map.html")

# Dashify

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash("SeattleADU", 
    external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1("Seattle map"),
    html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
        width="100%", height="500"),
    html.H3("Lot Size"),
    dcc.Slider(
            id='my-range-slider',
            min=1000,
            max=20000,
            step=100,
            value=4000
        ),
    html.Div(id='output-container-range-slider'),
    #html.Iframe(id="parent", srcDoc=html_frames, width="100%",
    #    height="600"),
    #html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
    #    width="100%", height="600")
])

@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
