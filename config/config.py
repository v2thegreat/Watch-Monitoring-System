import yaml

with open('config.yml') as config_file:
    config_file = yaml.load(config_file, Loader=yaml.FullLoader)

if __name__ == '__main__':
    print(config_file)
