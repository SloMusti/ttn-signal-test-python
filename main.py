# TTN signal analysis tool for multiple devices in multiple applications
# Run for a while and obtain an accurate signal level through averaging
# Note that changing SF or otehr parameters invalidates this

# config.yml file must be present, sample input
""" <your app name>:
   id: <ttn application id>
   key: <ttn application key> """

# Sample output:
""" ###### ns-mapper-1
gateway_novisad_popovica          -71.42 dBm       0.00 km
###### mb-mapper-1
eui-fcc23dfffe0a7553             -105.50 dBm       7.19 km
maribor-pohorje-gateway          -104.17 dBm       7.18 km
maribor-center-gateway            -89.00 dBm       0.04 km
irnas-1                           -87.50 dBm       0.00 km
maribor-tyrseva-s59dxx            -69.33 dBm       0.00 km """

import time
import ttn
import yaml
import traceback
import geopy.distance

#dictionary to store all data
device_dict = {}

def average(lst):
    return sum(lst) / len(lst)

def uplink_callback(msg, client):
  #print("Received uplink from ", msg.dev_id)
  try:
    #check if device is in the list
    if msg.dev_id in device_dict.keys():
        #device is in the list already
        pass
    else:
        #create a ditionary for this device
        gw_dict = {}
        device_dict[msg.dev_id]=gw_dict

    # print for every gateway that has received the message and extract RSSI
    for gw in msg.metadata.gateways:
      gateway_id = gw.gtw_id
      rssi = float(gw.rssi)

      #check if gw in the list
      if gateway_id in device_dict[msg.dev_id].keys():
          device_dict[msg.dev_id][gateway_id]["rssi"].append(rssi)
          #print(rssi)
      else:
        #note location may be missing and is handled
        try:
          gw_loc = (float(gw.latitude),float(gw.longitude))
          dev_loc = (float(msg.payload_fields.lat),float(msg.payload_fields.lon))
          distance = geopy.distance.vincenty(gw_loc, dev_loc).km
        except Exception as e: 
          #print(e)
          #traceback.print_exc()
          distance = 0

        device_dict[msg.dev_id][gateway_id]={"distance":distance,"rssi":[rssi]}

    print("###### " + msg.dev_id)
    for key, value in device_dict[msg.dev_id].items():
      print("{0:<30}{1:10.2f} dBm {2:10.2f} km".format(key,average(value["rssi"]),value["distance"]))
  except Exception as e: 
    print(e)
    traceback.print_exc()


# load config file, to store keys separtely and not commit to git
with open("config.yml", 'r') as ymlfile:
    try:
        cfg = yaml.safe_load(ymlfile)
    except yaml.YAMLError as exc:
            print(exc)

#note there may be multiple entries, currently taking the last one through iteration, assuming one entry
for section in cfg:
    app_id=cfg[section]["id"]
    print(cfg[section]["id"])
    access_key =cfg[section]["key"]
    print(cfg[section]["key"])

    handler = ttn.HandlerClient(app_id, access_key)

    # using mqtt client
    mqtt_client = handler.data()
    mqtt_client.set_uplink_callback(uplink_callback)
    mqtt_client.connect()
while True:
  pass
mqtt_client.close()

