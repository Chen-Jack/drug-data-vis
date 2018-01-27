# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import SideEffect, Chemical, Gene


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
    se_qs = None

    if(kwargs['type'] == 'chemical'):
        CID_query = int(kwargs['ID']) 
        chem_obj = Chemical.objects.get(CID = CID_query)
        se_qs = chem_obj.associated_side_effects.all()

    elif(kwargs['type'] == 'gene'):
        HGNC_query = int(kwargs['ID'])
        gene_obj = Gene.objects.get(HGNC = HGNC_query)
        se_qs = gene_obj.associated_side_effects.all()

    data={}
    counter = 0
    for se in se_qs:
        data.update({str(counter):(se.name, se.UMLS_CUI, se.total_associated_chemicals, se.total_associated_genes)})
        counter += 1

    return JsonResponse(data)


def get_related_genes(request, *args, **kwargs):
    if(kwargs['type'] == 'chemical'):
        CID_query = int(kwargs['ID'])
        chem_obj = Chemical.objects.get(CID = CID_query)
        gene_qs = chem_obj.associated_genes.all()

    elif(kwargs['type'] == "side_effect"):
        SE_Query = kwargs['ID']
        se_obj = SideEffect.objects.get(UMLS_CUI = SE_Query)
        gene_qs = se_obj.gene_set.all()

    data = {}
    counter = 0
    for gene in gene_qs:
        data.update({str(counter): (gene.HGNC, gene.Symbol, gene.UniProt, gene.Chromosome, gene.total_associated_side_effects, gene.total_associated_chemicals)})
        counter += 1
    return JsonResponse(data)

def get_related_chemicals(request, *args, **kwargs):
    if(kwargs['type'] == 'gene'):
        HGNC_query = int(kwargs['ID'])
        gene_obj = Gene.objects.get(HGNC = HGNC_query)
        chem_qs = gene_obj.chemical_set.all()

    elif(kwargs['type'] == "side_effect"):
        print("yes, all chemicsals related to side effect chosen")
        SE_Query = kwargs['ID']
        se_obj = SideEffect.objects.get(UMLS_CUI = SE_Query)
        chem_qs = se_obj.chemical_set.all()

    print("length is " + str(len(chem_qs)))
    data = {}
    counter = 0
    for chem in chem_qs:
        data.update({str(counter):(chem.CID, chem.InChIKey, chem.total_associated_side_effects, chem.total_associated_genes)})
        counter += 1
    return JsonResponse(data)

