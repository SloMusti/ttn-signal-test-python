import time
import ttn
import yaml
import traceback

import geopy.distance

#procesing messages and measuring signal
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


#MSG(app_id='maribor-mapper', dev_id='mb-mapper-1', hardware_serial='009A5AF08D02DBD0', port=1, counter=378949, payload_raw='wjngiyKCATAM', payload_fields=MSG(alt=304, hdop=1.2, lat=46.565216574979814, lon=15.658318737645061), metadata=MSG(time='2019-04-14T07:32:42.909810497Z', frequency=867.5, modulation='LORA', data_rate='SF7BW125', airtime=56576000, coding_rate='4/5', gateways=[MSG(gtw_id='eui-58a0cbfffe800657', timestamp=367038860, time='2019-04-14T07:32:42.551888Z', channel=0, rssi=-59, snr=7, rf_chain=0, latitude=46.56487, longitude=15.658201, location_source='registry')], latitude=46.565678, longitude=15.659616, location_source='registry'))

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

