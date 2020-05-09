from django.shortcuts import get_object_or_404,get_list_or_404, render
from django.template import loader
from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib import messages 
# Create your views here.
from django.http import HttpResponse
from .models import *
#from .forms import *
from .forms import LiquorStoreForm, StoreOwnerForm, ConsumerForm
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
import pytz


import datetime

# start_time = '9:00'
# end_time = '18:00'
# slot_time = 10



class Utils:

    def getNextSlot(start_time='9:00',end_time='18:00',slot_time=10,days=0):
    # Get store 
    # Start date from today to next 5 day
    
        print ('start_time:' + start_time + ',end_time:' + end_time + ',slot_time:' ,slot_time)
        #print (slot_time)

        start_date = datetime.datetime.now().date()
        end_date = datetime.datetime.now().date() + datetime.timedelta(days=days)

        days = []
        date = start_date
        while date <= end_date:
            hours = []
            time = datetime.datetime.strptime(start_time, '%H:%M')
            end = datetime.datetime.strptime(end_time, '%H:%M')
            while time <= end:
                hours.append(time.strftime("%H:%M"))
                time += datetime.timedelta(minutes=slot_time)
            date += datetime.timedelta(days=1)
            days.append(hours)

        print(days)
        # for hours in days:
        #     print(hours) 
        return days       