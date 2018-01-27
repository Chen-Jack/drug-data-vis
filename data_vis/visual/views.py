# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import SideEffect, Chemical


class HomeView(TemplateView):
    template_name = "home.html"


def get_chemical_list(request, *args, **kwargs):
    '''
    API endpoint that returns all chemicals in the database.
    Chemical: (CID, InChiKey, total_side_effects, total_genes)
    '''
    chemical_list = Chemical.objects.all()
    qs = {}
    counter = 0
    for chemical in chemical_list:
        total_side_effects = chemical.total_associated_side_effects
        total_genes = chemical.total_associated_genes
        qs.update({
            str(counter): (chemical.CID, chemical.InChIKey, total_side_effects, total_genes )
        })
        counter += 1
    return JsonResponse(qs)

def get_related_side_effects(request, *args, **kwargs):
    '''
    API endpoint that returns all side_Effect entries given some CID 
    Side effect: (Name, UMLS_CUI)
    '''
    CID_query = int(kwargs['CID']) 
    chem_obj = Chemical.objects.get(CID = CID_query)
    se_qs = chem_obj.associated_side_effects.all()

    data={}
    counter = 0
    for se in se_qs:
        data.update({str(counter):(se.name, se.UMLS_CUI)})
        counter += 1

    return JsonResponse(data)

def get_related_genes(request, *args, **kwargs):
    
    CID_query = int(kwargs['CID'])
    chem_obj = Chemical.objects.get(CID = CID_query)
    gene_qs = chem_obj.associated_genes.all()

    data = {}
    counter = 0
    for gene in gene_qs:
        data.update({str(counter): (gene.HGNC, gene.Symbol, gene.UniProt, gene.Chromosome, gene.total_associated_side_effects, gene.total_associated_chemicals)})
        counter += 1
    return JsonResponse(data)
