import yaml

# load config file, to store keys separtely and not commit to git
with open("config.yml", 'r') as ymlfile:
    try:
        cfg = yaml.safe_load(ymlfile)
    except yaml.YAMLError as exc:
            print(exc)

for section in cfg:
    print(section)
    print(cfg[section]["id"])
    print(cfg[section]["key"])