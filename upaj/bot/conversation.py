import sys
import watson_developer_cloud
import pywapi
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from math import sqrt
from random import seed
from random import randrange
from csv import reader
import datetime
import time
from sklearn import datasets,linear_model
from pprint import pprint
import pandas as pd
import json

from sklearn.tree import DecisionTreeClassifier

DATA_GOV_API ='579b464db66ec23bdd000001f4159aa056f849bb6c7922a7a5c2cc99'


def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset


conversation = watson_developer_cloud.ConversationV1(
    username='e91c46f8-af25-4f34-8fef-2770b88a7ae6',
    password='kHshOoKQggLE',
    version='2018-03-08'
)

def get_response(chat):

    ''' Calls the Watson API for responses'''

    workspace_id = 'b1d807f3-080c-4b9a-bdee-dead8ed75a1b'
    response = conversation.message(workspace_id=workspace_id, input={'text': chat})
    return response

def main(query):

    intents = []
    entities = []

    watson_replies = get_response(query)
    response = watson_replies.result
    pprint(response)

    for intent in response['intents']:
        intents.append(intent['intent'])

    for entity in response['entities']:
        entities.append(entity)

    return message_type(intents, entities, response)


def message_type(intents, entities, response):

    if 'greetings' in intents:
        return greeting(response)

    if 'weather' in intents:
        return location_suggestions(entities)

    if 'crop_forecasting' in intents:
        return crop_forecasting(entities)

    if 'cost' in intents:
        return cost(response)

    if 'pesticide' in intents:
        return pesticide(entities)

    if 'goodbyes' in intents:
        return bye()

    if [] == intents:
        return rephrase(response)

def rephrase(response):

    ''' asks user to rephrase itself'''

    return response_encoder(response['output']['text'])

def greeting(response):

    ''' returns greetings messages'''

    return response_encoder(response['output']['text'])

def weather(location_id):

    ''' returns weather conditions for a given location '''

    weather_data = pywapi.get_weather_from_weather_com(location_id)
    pprint(weather_data)

    response = "Temperature : " + weather_data['current_conditions']['temperature'] + "C" + " Humidity : " + weather_data['current_conditions']['humidity'] + " Wind Speed : " + weather_data['current_conditions']['wind']['speed']

    return response


def location_suggestions(entities):

    ''' facilitates search of location '''

    location = entities[0]['value']

    data = pywapi.get_location_ids(location)
    if len(data) is 1:
        for loc_id, location in data.items():
            return weather(loc_id)
    else:
        print ('There are number quite a few location with similar set of name, please be specific')
        return response_encoder(data)


def pesticide(entities):

    ''' returns pesticide information '''

    value = entities[0]['value']
    data = load_csv('pesticides.csv')
    print(data)
    pest = str(-1)
    for i in range(1,len(data)):
        if (data[i][0].lower() == value.lower()):
            pest = data[i][1].lower()
            break


def cost(entities):

    crop_data = entities[0][['value']]
    output = msp(crop_data)
    print(output)


def response_encoder(response):

    ''' encodes message to the proper format '''

    message = {}
    message['bubbles'] = 1
    message['text'] = []

    if type(response) == str:
        message['text'].append('<div class="message new"><figure class="avatar"><img src="chathead.png" /></figure>' + response + '</div>')
    elif type(response) == dict:
        for key, value in response.items():
            message['text'].append('<div class="message new"><figure class="avatar"><img src="chathead.png" /></figure>' + value + '</div>')

        message['bubbles'] = len(response)

    return message


# def crop_forecasting(): # pass entities in this later

#     data = pd.read_table('~/Documnents/Datasets/Upaj/Cauliflower_as_on_date.xml')
#     print(data.head())

#     clf = DecisionTreeClassifier()
