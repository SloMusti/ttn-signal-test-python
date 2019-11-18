# ttn-signal-test-python
Simple script to read data from multiple applications on TheThingsNetwork and analyse signal level on multipel gateways. Particularly useful for gateway testing and node testing when comparing antennas or similar.

## Setup
Download this repository. Set up the environment, recommended to use python virtual environment `pip install virtualenv`.

```
git clone https://github.com/SloMusti/ttn-signal-test-python
cd ttn-signal-test-python
python3 -m venv ./env
source env/bin/activate
pip install -r requirements.txt
```

## Prepare config
Create the config file `config.yaml` with the following structure, you can have multiple TTN applications defined, data will be shown for all nodes sending on those applications.
```
 <your app name>:
   id: <ttn application id>
   key: <ttn application key> 
```

## Run the application
Run the application within the active virtual environment with `python main.py` and expect a similar output to:
```
###### ns-mapper-1
gateway_novisad_popovica          -71.42 dBm       0.00 km
###### mb-mapper-1
eui-fcc23dfffe0a7553             -105.50 dBm       7.19 km
maribor-pohorje-gateway          -104.17 dBm       7.18 km
maribor-center-gateway            -89.00 dBm       0.04 km
irnas-1                           -87.50 dBm       0.00 km
maribor-tyrseva-s59dxx            -69.33 dBm       0.00 km
```
