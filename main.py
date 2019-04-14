import time
import ttn
import yaml

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)

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
time.sleep(60)
mqtt_client.close()

# using application manager client
app_client =  handler.application()
my_app = app_client.get()
print(my_app)
my_devices = app_client.devices()
print(my_devices)
