import folium
import sys
import constant as C
import adusql as ads
import numpy as np
import pandas as pd


def update_map(value, coords=C.SEATTLE, zoom=C.INIT_ZOOM):

    if value != None:
        adunit = ads.Connection("adunits.db")
        df = adunit.getParcelCoords(value)
        df.to_csv("df.csv")
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

        # re implement this using switch case
        def output():
            value = "<center><h4>Your home's ADU Eligibility</h4></center>"
            if (df.iloc[0]["zone_ind"] == 0):
                value += "<h5> For an AADU, this home is <b>Ineligible</b></h5> This is not a single family zoned home"
            elif (df.iloc[0]["zone_ind"] == 1):
                value += "<br><h5> For an AADU, this home is <b>Eligible</b></h5> Here are some pre-approved AADU plans to consider."
            value += "<h5> For a DADU, this home is " + "<b>" + \
                str(df.iloc[0]["adu_eligible"]) + "</b></h5>"
            if (str(df.iloc[0]["adu_eligible"]) == "Eligible"):
                value += "Here are some pre-approved DADU plans to consider."
            if (df.iloc[0]["zone_ind"] == 1 and str(df.iloc[0]["adu_eligible"]) == "Eligible" and pd.isna(df.iloc[0]["ADU"])):
                value += "<br>This home is eligible to build both an ADU AND a DADU!."
            if (df.iloc[0]["adu_eligible"] == "Ineligible"):
                value += "<h5><i>Potential Problems for DADUs</i></h5>"
            if (df.iloc[0]["zone_ind"] == 0):
                value += "<br> This is not a single family zoned home"
            if (df.iloc[0]["ls_indic"] == 0):
                value += "<br> This lot is not large enough to house a DADU"
            if (df.iloc[0]["lotcov_indic"] == 0):
                value += "<br> There is insufficient lot coverage on this parcel to build a DADU"
            if (not pd.isna(df.iloc[0]["ADU"])):
                value += "<br> There is already at least one existing ADU on this property"
            if (df.iloc[0]["shoreline_ind"] == 1):
                value += "<br> This home is next to the shoreline. DADUs cannot be built by shorelines"
            if (df.iloc[0]["zone_ind"] == 1):
                value += "<h5><i>Potential considerations of concern for ADUs and DADUs: </i></h5>"
                if (df.iloc[0]["parcel_steepslope"] == 1):
                    value += "<br> Your home may have some steep areas that may make it more costly to permit and build an ADU"
                if (df.iloc[0]["parcel_flood"] == 1):
                    value += "<br> Your home may have been flooded in the past. This may make it more costly to permit and build an ADU"
                if (df.iloc[0]["parcel_poteslide"] == 1):
                    value += "<br> Your home may be a potential slide area. This may make it more costly to permit and build an ADU"
                if (df.iloc[0]["parcel_landf"] == 1):
                    value += "<br> Your home may be located on (or close to a?) a landfill. This may make it more costly to permit and build an ADU"
                if (df.iloc[0]["parcel_peat"] == 1):
                    value += "<br> Your home may be a peat settlement. This may make it more costly to permit and build an ADU"
                if (df.iloc[0]["parcel_riparian"] == 1):
                    value += "<br> Your home may be on a riparian corridor. This may make it more costly to permit and build an ADU"

            value += "<br><br><a href="">More details on the eligibility criteria and your home's eligibility here</a>"

            return value

        # FIXME: fill_color is bad keyword
        # folium.Polygon(locations=locations, color='blue', weight=6, fill_color='red',
        folium.Polygon(locations=locations, color='blue', weight=6,
                       fill_opacity=0.5, fill=True,
                       # FIXME: fill_color is bad keyword
                       # popup=folium.Popup(output(), max_width=2000, fill_color="green", show=True),
                       popup=folium.Popup(output(), max_width=2000, show=True),
                       # popup=folium.Popup("<h5> For a DADU, this home is " + "<b>" +
                       #                    str(df.iloc[0]["adu_eligible"]) + "</b></h5>" + "<h5> For an AADU, this home is <b>Eligible</b></h5>" + "<h5><i>Essential Criteria</i></h5>" +
                       #                    " Is this a Single Family zoned home? " + str(df.iloc[0]["zone_ind"]) +
                       #                    "<br> Is this lot large enough to house a DADU? " + str(df.iloc[0]["ls_indic"]) +
                       #                    "<br> Is lot coverage sufficient for a DADU? " + str(df.iloc[0]["lotcov_indic"]) +
                       #                    "<br> Existing ADUs or DADUs on this property " + str(df.iloc[0]["ADU"]) +
                       #                    "<br>Potential considerations of concern: <b>None</b>" +
                       #                    "<br><br><a href="">More details on the eligibility criteria and your home's eligibility here</a>",

                       #                    max_width=2000),
                       # popup=folium.Popup(output(), max_width=2000, fill_color="green", show=True),
                       tooltip='Click me!',).add_to(new_map)

        neighbor = folium.map.FeatureGroup(name="neighbor",
                                           overlay=True, control=True, show=True,)
        df_ngb = pd.read_csv("neighbor.csv")
        # import pdb
        # pdb.set_trace()

        for i in range(0, len(df_ngb)):
            folium.Marker(location=[df_ngb.iloc[i]['coordY'], df_ngb.iloc[i]['coordX']],
                          popup=folium.Popup(df_ngb.iloc[i]["address"], max_width=2000)
                          ).add_to(neighbor)

        neighbor.add_to(new_map)
        folium.LayerControl().add_to(new_map)

        # feature = folium.features.GeoJson(geojson["features"]["geometry"],
        #     name=None, style_function=style_function, highlight_function=highlight_function,)
        # folium.Popup("Square feet of lot: " + str(geojson["features"]["properties"]["sqftlot"]), max_width=300).add_to(feature)

        # parcel.add_child(feature)
        # feature.add_to(new_map)

        # parcel.add_to(new_map)

    new_map.save("map.html")
    return open("map.html", "r").read()

# space holder for some features
