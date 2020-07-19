import yaml

with open('config/config.yml') as config_obj:
    config_obj = yaml.load(config_obj, Loader=yaml.FullLoader)

if __name__ == '__main__':
    print(config_obj)
