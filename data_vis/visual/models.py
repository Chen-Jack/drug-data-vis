# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SideEffect(models.Model):
    name = models.CharField(max_length = 50)
    UMLS_CUI = models.CharField(max_length = 8)

    def __str__ (self):
        return self.name

    @staticmethod
    def fillDataBase(): #Please only use this within the shell and only once
        if(len(SideEffect.objects.all()) != 0): #The database is already filled with something
            print("The database is already filled.")
            return 
        
        SE_data = open('./data/SideEffectList.tsv', 'r')
        SE_data.readline() #Skipping the first line
        for entry in SE_data:
            parsed_entry = entry.split('\t')
            SideEffect.objects.create(name = parsed_entry[2], UMLS_CUI = parsed_entry[1])
        SE_data.close()

class Chemical(models.Model):
    CID = models.IntegerField()
    InChIKey = models.CharField(max_length = 27)
    SMILES = models.CharField(max_length = 1000)

    def __str__ (self):
        return 'CID: ' + str(self.CID)

    @staticmethod
    def fillDataBase(): #Please only use this within the shell and only once
        if(len(Chemical.objects.all()) != 0): #The database is already filled with something
            print("The database is already filled.")
            return 
        
        CHEM_data = open('./data/SIDER_chemicals_stereo.tsv', 'r')
        CHEM_data.readline() #Skipping the first line
        for entry in CHEM_data:
            parsed_entry = entry.split('\t')
            Chemical.objects.create(CID = parsed_entry[1], InChIKey = parsed_entry[2], SMILES=parsed_entry[3])
        CHEM_data.close()