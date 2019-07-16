import json
import os


#geo_json_data_test = json.loads(open('neighborhoods.geojson').read())
with open("neighborhoods.geojson") as f:
	geo_json_data_test = json.load(f)

for i in range(0,len(geo_json_data_test["features"])):
	print(geo_json_data_test["features"][i]["properties"])

#print(data["features"][0]["properties"]["name"])

# geojson_test = {}
#for i in geo_json_data_test["features"]:
#    print(i["properties"])