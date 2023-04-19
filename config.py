"""Выносим отдельно все токены"""
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TG_TOKEN = config['API_TOKENS']['TG_TOKEN']
OPEN_WEATHER_TOKEN = config['API_TOKENS']['OPEN_WEATHER_TOKEN']
EXCHANGERATE_TOKEN = config['API_TOKENS']['EXCHANGERATE_TOKEN']
