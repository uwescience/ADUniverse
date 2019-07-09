import folium
import json
import sys
from folium.plugins import Search
import geojson

def make_map():

    SEATTLE_COORDINATES = (47.6062, -122.3321)
    zoom_start = 12

    # create empty map zoomed in on San Francisco
    map = folium.Map(location=SEATTLE_COORDINATES, zoom_start=zoom_start, control_scale=True)

    # add neighborhoods on top of this. This is an experiment to be replaced with a polygon geojson
    geo_json_data = json.load(open('neighborhoods.geojson'))
    # parcel_data = json.load(open('Zoned_Parcels_forJSON.json'))
    # parcel2_data = json.load(open('Zoned_Parcels_forJSON_Featur.json'))


    # regular style of polygons


    def style_function(feature):
        return {
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0,
            'lineOpacity': 1,
        }


    def highlight_function(feature):
        return {
            'fillColor': 'blue',
            'weight': 2,
            'lineColor': 'black',
            'lineWeight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0.5,
            'lineOpacity': 1,
        }


    # apply the neighborhood outlines to the map
    neighborhoods = folium.features.GeoJson(geo_json_data,
                                   style_function=style_function,
                                   highlight_function=highlight_function,
                                   )
    # parcels = folium.features.GeoJson(parcel_data,
    #                                style_function=style_function,
    #                                highlight_function=highlight_function,
    #                                )

    neighborhoods2 = folium.map.FeatureGroup(name="neighborhoods2", overlay=True, control=True, show=True,)

    with open("neighborhoods.geojson") as f:
        geo_json_data_test = json.load(f)

    for i in range(0,len(geo_json_data_test["features"])):
        c = folium.features.GeoJson(geo_json_data_test["features"][i]["geometry"],
            name=(geo_json_data_test["features"][i]["properties"]["name"]),
            style_function=style_function,
            highlight_function=highlight_function,)
        folium.Popup(geo_json_data_test["features"][i]["properties"]["name"], geo_json_data_test["features"][i]["properties"]["nhood"]).add_to(c)
        neighborhoods2.add_child(c)

    import pdb; pdb.set_trace()  
    neighborhoods2.add_to(map)
    print(neighborhoods)
    print(neighborhoods2)

    neighborhoodsearch = Search(
        layer=neighborhoods2,
        geom_type='Polygon',
        placeholder='Search for a neighborhood name',
        collapsed=False,
        search_label='name',
        weight=3,
        fillColor="black",
        fillOpacity = 0.6
    ).add_to(map)
    # We need to fix kwargs and popups of polygons iterating through geojson


    # print(geo_json_data[1,:])
    # geo_json_data_df = pd.DataFrame.from_dict(geo_json_data)
    # geo_json_data_df.to_csv(r'/Users/Anaavu/Documents/GitHub/ADUniverse/app/geo_json_data_df.csv')


    # add a marker for every record in the filtered data, use a clustered view
    for _, row in data[0:MAX_RECORDS].iterrows():
        popup = folium.Popup("Feasibility: " + str(row['Random Number']) +
                             "<br> Address: " + str(row['Address']), max_width=300)
        # html_str = """
        # <a href="https://www.ibm.com/" target="_blank"> Details.</a>
        # """
        # iframe = folium.IFrame(html=html_str, width=100, height=50)
        # popup = folium.Popup(iframe, max_width=2650)
        folium.Marker([row['Latitude'], row['Longitude']], popup=popup).add_to(map)




        #     popup = folium.Popup(i['name'])
        # c.add_to(map)

    map.save("map.html")