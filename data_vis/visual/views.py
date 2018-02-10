# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import SideEffect, Chemical, Gene, chem_similarity, se_similarity, gene_similarity

class HomeView(TemplateView):
    template_name = "home.html"

#Single access functions
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
    'total_associated_chems': side_effect_obj.total_associated_chemicals})

#Self model similarity functions
def get_chem_similarity(request, *args, **kwargs):
    '''
    Returns a JSON response of a collection of edges and it's weights
    '''
    chem_obj = Chemical.objects.get(CID = int(kwargs['ID']))
    sim_set = chem_similarity.objects.filter(chem_a = chem_obj)
    data = {}
    counter = 0
    for item in sim_set:
        data.update({str(counter): {'source': item.chem_a.CID , 'target': item.chem_b.CID, 'weight': item.similarity}})
        counter += 1

    return JsonResponse(data)

def get_side_similarity(request, *args, **kwargs):
    '''
    Returns a JSON response of a collection of edges and it's weights
    '''
    se_obj = SideEffect.objects.get(UMLS_CUI = kwargs['ID'])
    se_set = se_similarity.objects.filter(se_a = se_obj)
    data = {}
    counter = 0
    for item in se_set:
        data.update({str(counter): {'source': item.se_a.UMLS_CUI , 'target': item.se_b.UMLS_CUI, 'weight': item.similarity}})
        counter += 1

    return JsonResponse(data)

def get_gene_similarity(request, *args, **kwargs):
    gene_obj = Gene.objects.get(HGNC = int(kwargs['ID']))
    gene_set = gene_similarity.objects.filter(gene_a = gene_obj)
    data = {}
    counter = 0
    for item in gene_set:
        if(item.interaction != 0):
            data.update({str(counter):{'type': 'interaction', 'source': item.gene_a.HGNC , 'target': item.gene_b.HGNC, 'weight': item.interaction} })
            counter += 1
        if(item.similarity != 0):
            data.update({str(counter): {'type': 'similarity', 'source': item.gene_a.HGNC , 'target': item.gene_b.HGNC, 'weight': item.similarity}})
            counter +=1
        counter += 1

    return JsonResponse(data)

#Neighboring functions
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

# def get_similarity_data(request, *args, **kwargs):
#     if(kwargs['type'] == 'chemical'):
#         return get_chem_similarity()
#     elif(kwargs['type'] == 'side_effect'):
#         pass
#     elif(kwargs['type'] == 'gene'):
#         pass
#     else:
#         print("error getting similarity data")
