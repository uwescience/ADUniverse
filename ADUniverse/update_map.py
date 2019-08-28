import folium
import constant as C
import adusql as ads
import numpy as np
import pandas as pd
from common_data import app_data


def update_map(df, df_ngb, coords=C.SEATTLE, zoom=C.INIT_ZOOM):

    if not(df.empty):
        coords = (df.coordY[0], df.coordX[0])

        zoom = 18

    new_map = folium.Map(location=coords, zoom_start=zoom)

    if not(df.empty):

        locations = np.asarray(df[pd.Index(['coordY', 'coordX'])])

        # re implement this using switch case
        def output():
            value = "<center><h4>Your home's Eligibility for an ADU</h4></center>"
            if (df.iloc[0]["zone_ind"] == 0):
                value += "<h5> For an AADU, this home is <b>not eligible</b></h5> because it is not located in a single-family zone"
            elif (df.iloc[0]["zone_ind"] == 1):
                value += "<br><h5> For an AADU, this home is <b>eligible</b></h5> Here are some pre-approved AADU plans to consider."
            value += "<h5> For a DADU, this home is " + "<b>" + \
                str(df.iloc[0]["adu_eligible"]) + "</b></h5>"
            if (str(df.iloc[0]["adu_eligible"]) == "Eligible"):
                value += "Here are some pre-approved DADU plans to consider."
            if (df.iloc[0]["zone_ind"] == 1 and str(df.iloc[0]["adu_eligible"]) == "Eligible" and pd.isna(df.iloc[0]["ADU"])):
                value += "<br>This property is eligible to build both an AADU and a DADU!"
            if (df.iloc[0]["adu_eligible"] == "Ineligible"):
                value += "<h5><i>Potential Challenges for DADUs</i></h5>"
            if (df.iloc[0]["zone_ind"] == 0):
                value += "<br> Your property is not located on a single-family zone"
            if (df.iloc[0]["ls_indic"] == 0):
                value += "<br> Your property does not meet the minimum lot size for a DADU"
            if (df.iloc[0]["lot_dim_indic"] == "no"):
                value += "<br> Your lot's dimensions are not large enough to house a DADU"
            if (df.iloc[0]["lotcov_indic"] == 0):
                value += "<br> Given lot coverage limits, your property appears not to have sufficient available lot area to build a DADU"
            if (not pd.isna(df.iloc[0]["ADU"])):
                value += "<br> At least one ADU already exists on your property"
            if (df.iloc[0]["shoreline_ind"] == 1):
                value += "<br> Your property is located within 200 feet of a designated shoreline (i.e., the Shoreline District). \
                DADUs are not allowed in the Shoreline District"
            if (df.iloc[0]["zone_ind"] == 1):
                value += "<h5><i>Potential considerations of concern for AADUs and DADUs: </i></h5>"
                if (df.iloc[0]["yrbuilt"] < 1959):
                	value += "Given the age of your home, you converting existing space to an AADU could require substantial changes or upgrades to meet current building codes"
                if (df.iloc[0]["treecanopy_prct"] > 30):
                    value += "Your home may have a significant tree canopy percentage that may restrict your ability to build a DADU"
                if (df.iloc[0]["parcel_steepslope"] == 1):
                    value += "<br> Your property appears to have some steep areas that may make it more costly to permit and build an ADU and/or limit where you can site a DADU"
                if (df.iloc[0]["parcel_flood"] == 1):
                    value += "<br> Your property appears to be located in a floods-prone area. This may make it more costly or difficult to design, permit, and build an ADU"
                if (df.iloc[0]["parcel_poteslide"] == 1):
                    value += "<br> Your property appears to be located in a potential slide area. This may make it more costly or difficult to design, permit, and build an ADU"
                if (df.iloc[0]["parcel_landf"] == 1):
                    value += "<br> Your property appears to be located on a former landfill. This may make it more costly or difficult to design, permit, and build an ADU"
                if (df.iloc[0]["parcel_peat"] == 1):
                    value += "<br> Your property appears to be located in an area prone to peat settlement. This may make it more costly or difficult to design, permit, and build an ADU"
                if (df.iloc[0]["parcel_riparian"] == 1):
                    value += "<br> Your property appears to be located within a riparian corridor. This may make it more costly or difficult to design, permit, and build an ADU"
                if (df.iloc[0]["side_sewer_conflict"] == 1):
                    value += "<br> Your property appears to have a side sewer conflict. This could affect or limit the size or location of an ADU on your lot."
                else:
                    if (df.iloc[0]["intersecting_sewer"] == 1):
                        value += "<br> Your property has a side sewer that crosses another lot. You may need to reroute or construct a new side sewer for a DADU"
                    if (df.iloc[0]["landlocked_parcel"] == 1):
                        value += "<br> Your lot appears to be landlocked. Your ADU may require a new side sewer through a neighboring lot."

            value += "<br><br>More details on the eligibility criteria and your home's eligibility below"
            value += "<br>Check for neighborhood covenants"

            return value

        folium.Polygon(locations=locations, color='blue', weight=6,
                       fill_opacity=0.5, fill=True,
                       popup=folium.Popup(output(), max_width=2000, show=True),
                       tooltip='Click me!',).add_to(new_map)

        neighbor = folium.map.FeatureGroup(name="neighbor",
                                           overlay=True, control=True, show=True,)

        for i in range(0, len(df_ngb)):
            folium.Marker(location=[df_ngb.iloc[i]['latitude'], df_ngb.iloc[i]['longitude']],
                          popup=folium.Popup("Type: " + df_ngb.iloc[i]["ADU_type"] + "<br>"
                                             "Permitted in: " +
                                             str(int(df_ngb.iloc[i]["year_issue"])) + "<br>"
                                             + "Address: " + df_ngb.iloc[i]["address"],  max_width=2000)
                          ).add_to(neighbor)

        neighbor.add_to(new_map)
        folium.LayerControl().add_to(new_map)

    new_map.save("map.html")
    return open("map.html", "r").read()
