import folium
import sys
import constant as C
import adusql as ads
import numpy as np
import pandas as pd



def update_map(value, coords=C.SEATTLE, zoom=C.INIT_ZOOM):
    yearbuilt = 1

    if value != None:
        yearbuilt = 1
        adunit = ads.Connection("adunits.db")
        df = adunit.getParcelCoords(value)
        # df.to_csv("df.csv")
        # coords = (newCoords.latitude[0], newCoords.longitude[0])
        coords = (df.coordY[0], df.coordX[0])
        # coords = (df.iloc[0]["coordY"]["coordX"])
        # float max digits is not long enough
        zoom = 18

        # def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
        #     geojson = {'type': 'FeatureCollection', 'features': []}
        #     feature = {'type': 'Feature',
        #                'properties': {},
        #                'geometry': {'type': 'Polygon',
        #                             'coordinates': []}}
        #     for _, row in df.iterrows():
        #         feature['geometry']['coordinates'].append([row[lon], row[lat]])
        #         for prop in properties:
        #             feature['properties'][prop] = row[prop]
        #         geojson['features'] = feature
        #     return geojson

        # cols = ['adu_eligible', 's_hood', 'zone_ind', 'sqftlot',
        #         'ls_indic', 'lotcov_indic', 'lotcoverage', 'sm_lotcov_ind', 'sm_lotcov',
        #         'yrbuilt', 'daylightbasement', 'sqftfinbasement',  'shoreline_ind',
        #         'parcel_flood', 'parcel_landf', 'parcel_peat',
        #         'parcel_poteslide', 'parcel_riparian', 'parcel_steepslope',
        #         ]
        # geojson = df_to_geojson(df, cols, lat='coordX', lon='coordY')

    new_map = folium.Map(location=coords, zoom_start=zoom)

    # with open('myfile.geojson', 'w') as f:
    #     json.dump(geojson, f)

    # with open('myfile2.geojson', 'w') as f2:
    #     geojson.write(f2)
    #     f2.close()
    if value != None:
        # parcel = folium.map.FeatureGroup(name="parcel",
        #                                  overlay=True, control=True, show=True,)

        # for i in range(0, len(geojson["features"])):
        #     print(len(geojson["features"]))
        #     print(i)
        #     print(geojson["features"][i]["geometry"])
        #     feature = folium.features.GeoJson(geojson["features"][i]["geometry"],
        #                                       name=(geojson["features"][i]["properties"]["sqftlot"]),
        #                                       style_function=style_function,
        #                                       highlight_function=highlight_function,)
        #     folium.Popup(
        #                  "Square feet of lot: " + geojson["features"][i]["properties"]["sqftlot"], max_width=200).add_to(feature)
        #     parcel.add_child(feature)

        # parcel = folium.features.GeoJson(geojson, style_function=style_function, highlight_function=highlight_function) #### Anag
        # print(geojson["features"][0]["geometry"])

        # folium.Popup()
        # folium.Marker(coords, popup=folium.Popup("<b><h4>Is this home ADU eligible? </h4></b>" +
        #     str(df.iloc[0]["adu_eligible"]) + "<br><h5><i>Details</i></h5>" +
        #     "<br>Neighborhood: " + str(df.iloc[0]["s_hood"]) +
        #     "<br>Is this a Single Family zoned home? " + str(df.iloc[0]["zone_ind"]) +
        #     "<br>Square feet of lot: " + str(df.iloc[0]["sqftlot"]) +
        #     "<br> ls_indic " + str(df.iloc[0]["ls_indic"]) +
        #     "<br> lotcov_indic " + str(df.iloc[0]["lotcov_indic"]) +
        #     "<br> lotcoverage " + str(df.iloc[0]["lotcoverage"]) +
        #     "<br> sm_lotcov_ind " + str(df.iloc[0]["sm_lotcov_ind"]) +
        #     "<br> sm_lotcov " + str(df.iloc[0]["sm_lotcov"]) +
        #     "<br> Year House Built " + str(df.iloc[0]["yrbuilt"]) +
        #     "<br> Does this home have a daylight basement? " + str(df.iloc[0]["daylightbasement"]) +
        #     "<br> Square foot in basement " + str(df.iloc[0]["sqftfinbasement"]) +
        #     "<br> Does this lot border a shoreline? " + str(df.iloc[0]["shoreline_ind"]) +
        #     "<br><i>Environmentally Critical Areas assessment</i>" +
        #     "<br>Is this parcel on a steep slope? " + str(df.iloc[0]["parcel_steepslope"]) +
        #     "<br>Is this parcel on a previously flooded area? " + str(df.iloc[0]["parcel_flood"]) +
        #     "<br>Is this parcel on a potential slide area? " + str(df.iloc[0]["parcel_poteslide"]),
        #     max_width=2000)
        #     ).add_to(new_map)

        # locations = geojson["features"]["geometry"]["coordinates"]

        locations = np.asarray(df[pd.Index(['coordY', 'coordX'])])
        # print(locations)

        folium.Polygon(locations=locations, color='blue', weight=6, fill_color='red',
                       fill_opacity=0.5, fill=True,
                       popup=folium.Popup("<b><h4>For a DADU, this home is </h4></b>" +
                                          "<h4>" + str(df.iloc[0]["adu_eligible"]) + "</h4>" + "<br>For an AADU, this home is Eligible" + "<br><i>Details</i>" +
                                          "<br>Neighborhood: " + str(df.iloc[0]["s_hood"]) +
                                          "<br>Is this a Single Family zoned home? " + str(df.iloc[0]["zone_ind"]) +
                                          "<br>Square feet of lot: " + str(df.iloc[0]["sqftlot"]) +
                                          "<br> Is this lot large enough to house a DADU? " + str(df.iloc[0]["ls_indic"]) +
                                          "<br> For lots bigger than 5000 square feet, is lot coverage sufficient for a DADU? " + str(df.iloc[0]["lotcov_indic"]) +
                                          "<br> For lots bigger than 5000 square feet, what is the lot coverage? " + str(df.iloc[0]["lotcoverage"]) +
                                          "<br> For lots smaller than 5000 square feet, is lot coverage sufficient for a DADU? " + str(df.iloc[0]["sm_lotcov_ind"]) +
                                          "<br> For lots smaller than 5000 square feet, what is the lot coverage? " + str(df.iloc[0]["sm_lotcov"]) +
                                          "<br> Year House Built: " + str(df.iloc[0]["yrbuilt"]) +
                                          # "<br> Does this home have a daylight basement? " + str(df.iloc[0]["daylightbasement"]) +
                                          # "<br> Square foot in basement " + str(df.iloc[0]["sqftfinbasement"]) +
                                          "<br> Does this lot border a shoreline? " + str(df.iloc[0]["shoreline_ind"]) +
                                          "<br><i>Environmentally Critical Areas assessment</i>" +
                                          "<br>Is this parcel on a steep slope? " + str(df.iloc[0]["parcel_steepslope"]) +
                                          "<br>Is this parcel on a previously flooded area? " + str(df.iloc[0]["parcel_flood"]) +
                                          "<br>Is this parcel on a potential slide area? " +
                                          str(df.iloc[0]["parcel_poteslide"]),
                                          max_width=2000),
                       tooltip='Click me!',).add_to(new_map)

        # feature = folium.features.GeoJson(geojson["features"]["geometry"],
        #     name=None, style_function=style_function, highlight_function=highlight_function,)
        # folium.Popup("Square feet of lot: " + str(geojson["features"]["properties"]["sqftlot"]), max_width=300).add_to(feature)
        # parcel.add_child(feature)
        # feature.add_to(new_map)

        # parcel.add_to(new_map)

    new_map.save("map.html")
    return 'The home you selected was built in year "{}"'.format(yearbuilt), open("map.html", "r").read()

# space holder for some features
