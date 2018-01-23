# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

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

class SideEffect(models.Model):
    name = models.CharField(max_length = 50)
    UMLS_CUI = models.CharField(max_length = 8)
    caused_by = models.ManyToManyField(Chemical, blank=True)

    def __str__ (self):
        return self.name

    @staticmethod
    def fillDataBase(): #Please only use this within the shell and only once.
        if(len(SideEffect.objects.all()) != 0): #The database is already filled with something
            print("The database is already filled.")
            return 
        
        SE_data = open('./data/SideEffectList.tsv', 'r')
        SE_data.readline() #Skipping the first line
        for entry in SE_data:
            parsed_entry = entry.split('\t')
            SideEffect.objects.create(name = parsed_entry[2], UMLS_CUI = parsed_entry[1])
        SE_data.close()

def initRelation():

    #Just getting the dimensions of your matrix
    csv_data = open('/Users/jack/Desktop/chem_se_SIDER.csv', 'r')
    total_row = 0
    for line in csv_data:
        total_row += 1
    total_col = len(line.split(','))
    csv_data.close()
    
    print(total_row) #There are 1549 chemicals
    print(total_col) #There are 4251 side effects

    #Creating coordinates from csv file
    se_qs = SideEffect.objects.all()
    chem_qs = Chemical.objects.all()

    csv_data = open('/Users/jack/Desktop/chem_se_SIDER.csv', 'r') 
    csv_data.readline() #Skip the first line
    for row in range(total_row-1): #I already read the first line above
        line = csv_data.readline()
        print(row)
        parsed_line = line.rstrip('\n').split(',')
        for col in range(total_col):
            if(col !=0 and parsed_line[col] == '1'): 
                se_qs[col-1].caused_by.add(chem_qs[row]) #-1 from col since we don't want to read the first col
          
    csv_data.close()

def clearRelation():
    se_qs = SideEffect.objects.all()
    for se in se_qs:
        se.caused_by.clear()