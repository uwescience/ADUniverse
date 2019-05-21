# Python program to get a google map  
# image of specified location using  
# Google Static Maps API 
  
# importing required modules 
import requests 
import util
  
# Enter your api key here 
api_key = util.getKey()
  
  
# center defines the center of the map, 
# equidistant from all edges of the map.  
center = "Brooklyn+Bridge,New+York"

# url variable store url 
url = "https://maps.googleapis.com/maps/api/staticmap?center=%s"
url += "&zoom=13&size=600x300&maptype=roadmap&markers=color:blue"
url += "%s" + "7Clabel:S"
url += "%s" + "7C40.702147,-74.015794&markers=color:green"
url += "%s" + "7Clabel:G"
url += "%s" + "7C40.711614,-74.012318&markers=color:red"
url += "%s" + "7Clabel:C"
url += "%s" + "7C40.718217,-73.998284&key=%s"
url = url % (center, "%", "%", "%", "%", "%", "%", api_key)
  
# get method of requests module 
# return response object 
r = requests.get(url)
  
# wb mode is stand for write binary mode 
f = open('map_file.png', 'wb') 
  
# r.content gives content, 
# in this case gives image 
f.write(r.content) 
  
# close mthod of file object 
# save and close the file 
f.close() 
