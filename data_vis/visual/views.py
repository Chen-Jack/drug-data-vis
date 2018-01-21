# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

# '/Users/jack/Desktop/chem_se_SIDER.csv'


def chemical_side_effects(request):

    #Just getting the dimensions of your matrix
    csv_data = open('/Users/jack/Desktop/test.csv', 'r')
    total_row = 0
    for line in csv_data:
        total_row += 1
    total_col = len(line.split(','))
    csv_data.close()

    #Creating coordinates from csv file
    counter = 0
    coordinates = {} #A mapping of (chemicals , side effects)
    csv_data = open('/Users/jack/Desktop/test.csv', 'r') 
    for row in range(total_row):
        line = csv_data.readline()
        parsed_line = line.rstrip('\n').split(',')
        for col in range(total_col):
            if(parsed_line[col] == '1'):
                coordinates.update( { str(counter) : (str(row-1) , str(col-1)) } ) # -1 cause database starts at 0
                counter +=1 

    csv_data.close()
    return JsonResponse(coordinates)
   
       
    
