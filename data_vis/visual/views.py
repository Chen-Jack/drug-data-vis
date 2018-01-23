# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import SideEffect, Chemical


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
    CID_query = int(kwargs['CID']) 
    chem_obj = Chemical.objects.get(id = CID_query)
    se_list = chem_obj.sideeffect_set.all()

    data={}
    counter = 0
    for se in se_list:
        data.update({str(counter):(se.name, se.UMLS_CUI, str(se.caused_by))})
        counter += 1

    return JsonResponse(data)
