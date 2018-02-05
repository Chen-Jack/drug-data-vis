# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import SideEffect, Chemical, Gene


class HomeView(TemplateView):
    template_name = "home.html"

def get_single_chem(request, *args, **kwargs):
    '''
    Returns a JSON response of a single chemical object found
    using a CID
    '''
    CID_query = int(kwargs['ID'])
    chem_obj = Chemical.objects.get(CID = CID_query)
    if(chem_obj == None):
        return JsonResponse({})

    return JsonResponse({'CID': chem_obj.CID, 'InChIKey': chem_obj.InChIKey, \
    'total_associated_se': chem_obj.total_associated_side_effects, \
    'total_associated_genes': chem_obj.total_associated_genes})

def get_single_gene(request, *args, **kwargs):
    '''
    Returns a JSON response of a single gene found using HGNC
    '''

    HGNC_query = int(kwargs['ID'])
    gene_obj = Gene.objects.get(HGNC = HGNC_query)
    if(gene_obj == None):
        return JsonResponse({})

    return JsonResponse({'HGNC': gene_obj.HGNC, 'Symbol': gene_obj.Symbol, \
    'UniProt': gene_obj.UniProt, 'Chromosome': gene_obj.Chromosome,\
    'total_associated_side_effects': gene_obj.total_associated_side_effects,\
    'total_associated_chemicals': gene_obj.total_associated_chemicals})

def get_single_side_effect(request, *args, **kwargs):
    '''
    Returns a JSON response of a single side effect found using UMLS CUI
    '''
    UMLS_CUI_query= kwargs['ID']
    side_effect_obj = SideEffect.objects.get(UMLS_CUI = UMLS_CUI_query)
    if(side_effect_obj == None):
        return JsonResponse({})

    return JsonResponse({'name': side_effect_obj.name, 'UMLS_CUI': side_effect_obj.UMLS_CUI,\
    'total_associated_genes': side_effect_obj.total_associated_genes,\
    'total_associated_chems': side_effect_obj.total_associated_chems})



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
        entry = {'name': se.name, "UMLS_CUI": se.UMLS_CUI, 'total_associated_chemicals': se.total_associated_chemicals,\
        'total_associated_genes': se.total_associated_genes}
        data.update({str(counter): entry})
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
        entry = {'HGNC':gene.HGNC, 'Symbol': gene.Symbol, 'UniProt': gene.UniProt,\
        'Chromosome':gene.Chromosome, 'total_associated_side_effects': gene.total_associated_side_effects,\
        'total_associated_chemicals': gene.total_associated_chemicals}
        data.update({str(counter): entry})
        counter += 1
    return JsonResponse(data)

def get_related_chemicals(request, *args, **kwargs):
    if(kwargs['type'] == 'gene'):
        HGNC_query = int(kwargs['ID'])
        gene_obj = Gene.objects.get(HGNC = HGNC_query)
        chem_qs = gene_obj.chemical_set.all()

    elif(kwargs['type'] == "side_effect"):
        SE_Query = kwargs['ID']
        se_obj = SideEffect.objects.get(UMLS_CUI = SE_Query)
        chem_qs = se_obj.chemical_set.all()

    print("length is " + str(len(chem_qs)))
    data = {}
    counter = 0
    for chem in chem_qs:
        entry = {'CID':chem.CID, 'InChIKey': chem.InChIKey,\
        'total_associated_side_effects':chem.total_associated_side_effects,\
        'total_associated_genes': chem.total_associated_genes}
        data.update({str(counter):entry})
        counter += 1
    return JsonResponse(data)


