# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import SideEffect, Chemical
import json
# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"


   
def get_chemical_list(request, *args, **kwargs):
    chemical_list = Chemical.objects.all()
    qs = {}
    counter = 0
    for chemical in chemical_list:
        qs.update({
            str(counter): (chemical.CID, chemical.InChIKey, chemical.SMILES)
        })
        counter += 1
    return JsonResponse(qs)

def get_related_side_effects(request, *args, **kwargs):
   
    pass
    # return JsonResponse()