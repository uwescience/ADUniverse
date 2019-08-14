import folium
import sys
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

    # Based upon the amount of tree canopy in your rear yard the location and size of a detached
    # accessory dwelling unit may be limited.  You should consult with a design professional or a land use coach
    # at the applicant services center (link).  Information regarding the city’s tree protection ordinance can be found here (link).

    if not(df.empty):

        locations = np.asarray(df[pd.Index(['coordY', 'coordX'])])

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
                if (df.iloc[0]["treecanopy_prct"] > 30):
                    value += "Your home may have a significant tree canopy percentage that may restrict your ability to build a DADU"
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
                if (df.iloc[0]["side_sewer_conflict"] == 1):
                    value += "<br> Your home may have a conflicting side sewer with a neighbor or may need additional side sewer construction"

            value += "<br><br><a href="">More details on the eligibility criteria and your home's eligibility here</a>"
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
                                             + "Address: " + df_ngb.iloc[i]["address"],  max_width=2000)
                          ).add_to(neighbor)

        neighbor.add_to(new_map)
        folium.LayerControl().add_to(new_map)

    new_map.save("map.html")
    return open("map.html", "r").read()
