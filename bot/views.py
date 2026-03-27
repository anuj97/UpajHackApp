from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.templatetags.static import static
from . import conversation as cn
import sys
import js2py
# from urllib2 import urlopen
import pprint
import json
import csv
from bs4 import BeautifulSoup
import requests

import pandas as pd
import csv

#for sending sms


# adding models
from .models import Farmer, Trader
# Create your views here.
crop = []
prod = []
rain_year = []
rain = []
total_states = []


def home(request):
    global crop
    global prod
    global rain
    global rain_year
    global total_states
    data = pd.read_csv('csv_files/check.csv')
    state = "madhya pradesh"
    year = "2011"
    crop = []
    prod = []
    rain = []
    rain_year = []
    total_states = []
    rain_state = "madhya pradesh"
    for d in data['state']:
        if(d not in total_states):
            total_states.append(d)
    # print("helllloooooo")
    # print(total_states)
    try:
        if(request.method == "POST"):
            state = request.POST['state'].lower()
            year = request.POST['year']
            # print(state)

    except:
        state = "madhya pradesh"
        year = 2010


    try:
        if(request.method == "POST"):
            rain_state = request.POST['rain_state'].lower()

    except:
        rain_state = "madhya pradesh"


    data = data.groupby(['state', 'crop', 'year'], as_index = False)['production '].sum()
    data = data.loc[(data['state'] == state) & (data['year'] == int(year))]
    data = data.sort_values('production ', ascending = False)
    data = data.head()
    for obj in data['crop']:
        crop.append(obj)
    for obj in data['production ']:
        prod.append(obj)



    data = pd.read_csv('csv_files/rainfall_data.csv')
    data = data.loc[data['SUBDIVISION'] == rain_state]
    data = data.fillna(data.mean(numeric_only=True))

    for r in data['ANNUAL']:
        rain.append(r)
    for y in data['YEAR']:
        rain_year.append(str(y))

    # print(rain)
    # print(rain_year)

    r = requests.get("https://www.thebetterindia.com/topics/farming/")
    soup = BeautifulSoup(r.text,'html.parser')
    links = []
    for link in soup.findAll('a', attrs={'class' : 'g1-frame'}):
        links.append(link.get('href'))

    soup2 = BeautifulSoup(r.text, 'html.parser')
    titles = []

    for link in links:
        temp = link
        arr = temp.split('/')
        size = len(arr)
        titles.append(arr[size-2])
    final = []
    for title in titles:
        title = title.replace('-', ' ')
        final.append(title)

    fin = zip(links, final)

    farmers_trade = Farmer.objects.all()
    traders_trade = Trader.objects.all()


    # farmer trading
    object = {
        "crop" : crop,
        "prod" : prod,
        "state" : state,
        "year" : year,
        "rain" : rain,
        "rain_year" : rain_year,
        "rain_state" : rain_state,
        "total_states" : total_states,
        "fin" : fin,
        "farmers_trade" : farmers_trade,
        "traders_trade" : traders_trade,
    }
    return render(request, 'bot/index.html', object)

def get_response(request):
    query = request.POST['query']

    response = cn.chatDriver(query)

    return JsonResponse(response, safe=False)


def farmer_trading(request):
    name = request.POST['farmer_name']
    phone = request.POST['phone']
    crop_name = request.POST['crop_name']
    price = request.POST['your_price']

    if not Farmer.objects.filter(name = name, crop_name = crop_name).exists():
        db = Farmer()
        db.name = name
        db.phone = phone
        db.crop_name = crop_name
        db.price = price
        db.save()
        return home(request)

    else:
        return HttpResponse("unable to process at the moment")


def trader_trading(request):
    name = request.POST['farmer_name']
    phone = request.POST['phone']
    crop_name = request.POST['crop_name']
    price = request.POST['your_price']

    if not Trader.objects.filter(name = name, crop_name = crop_name, phone=phone).exists():
        db = Trader()
        db.name = name
        db.phone = phone
        db.crop_name = crop_name
        db.price = price
        db.save()
        return home(request)

    else:
        return HttpResponse("unable to process at the moment")



def sendSMS(request):
    URL = 'http://www.way2sms.com/api/v1/sendCampaign'
    req_params = {
        'apikey':'B55AJV5G3ANFWGRGLVH1MQ3WJ590OXSC',
        'secret':'LM1AFN34JNWPDLZ3',
        'usetype':'stage',
        'phone': '6387207970',
        'message':'Hello Devang',
        'senderid':'upajme',
    }

    result = requests.post(URL, req_params)
    print(result.text)

    return home(request)

# def plot(request):


#     # df = pd.DataFrame({'production' : prod}, index = crop)
#     # plot = df.plot.pie(y='production', figsize=(10, 10))
#     # print(plot)
#     return render(request, 'bot/index.html', {"crop" : crop, "prod" : prod, "state" : state, "year" : year})

# def rainfall_patterns(request):
#     global rain
#     global rain_year
#     rain = []
#     rain_year = []
#     if(request.method == "POST"):
#         rain_state = request.POST['rain_state']
#         if(rain_state == ""):
#             rain_state = "madhya pradesh"

#     data = pd.read_csv('csv_files/rainfall_data.csv')
#     data = data.loc[data['SUBDIVISION'] == rain_state]
#     data = data.fillna(data.mean())

#     for r in data['ANNUAL']:
#         rain.append(r)
#     for y in data['YEAR']:
#         rain_year.append(str(y))

#     # print(rain)
#     # print(rain_year)
#     return render(request, 'bot/index.html', {"rain" : rain, "rain_year" : rain_year, "rain_state" : rain_state})
