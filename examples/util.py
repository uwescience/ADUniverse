def getKey():
  with open("../apikey.key", "r") as fd:
    return fd.read()

def getMapboxToken():
  with open("../mapbox_token.key", "r") as fd:
    return fd.read()
