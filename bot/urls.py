from django.urls import re_path as url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('response', views.get_response, name='get_response'),
    path('farmer_trading', views.farmer_trading, name='farmer_trading'),
    path('trader_trading', views.trader_trading, name='trader_trading'),
    path('sendSMS', views.sendSMS, name='sendSMS'),

#     path('plot', views.plot, name = 'plot'),
#     path('rainfall_patterns', views.rainfall_patterns, name = 'rainfall_patterns'),
]
