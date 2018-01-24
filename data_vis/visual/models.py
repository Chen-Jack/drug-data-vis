# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SideEffect(models.Model):
    name = models.CharField(max_length = 50)
    UMLS_CUI = models.CharField(max_length = 8)

    total_associated_genes = models.IntegerField(null = True, blank=True)
    total_associated_chemicals = models.IntegerField(null = True, blank=True)
    
    def __str__ (self):
        return self.name

    @staticmethod
    def initDatabase(): #Please only use this within the shell and only once.
        if(len(SideEffect.objects.all()) != 0): #The database is already filled with something
            print("The database is already filled.")
            return 
        
        SE_data = open('./data/SideEffectList.tsv', 'r')
        SE_data.readline() #Skipping the first line
        for entry in SE_data:
            parsed_entry = entry.strip('\n').split('\t')
            SideEffect.objects.create(name = parsed_entry[2], UMLS_CUI = parsed_entry[1])
        SE_data.close()

class Gene(models.Model):
    name = models.CharField(max_length = 300)
    HGNC = models.IntegerField()
    Symbol = models.CharField(max_length = 20)
    UniProt = models.CharField(max_length = 6)
    Chromosome = models.CharField(max_length = 50)

    total_associated_side_effects = models.IntegerField(null = True, blank = True)
    associated_side_effects = models.ManyToManyField(SideEffect, blank = True)

    total_associated_chemicals = models.IntegerField(null = True, blank=True)
 
    def __str__(self):
        return self.name

    @staticmethod
    def initDatabase():
        if(len(Gene.objects.all()) != 0): #The database is already filled with something
            print("The database is already filled.")
            return 
        
        gene_data = open('./data/protein_list.tsv', 'r')
        gene_data.readline() #Skipping the first line
        for entry in gene_data:
            parsed_entry = entry.strip('\n').split('\t')
            Gene.objects.create(name = parsed_entry[4], HGNC = parsed_entry[1], Symbol = parsed_entry[2], UniProt = parsed_entry[3], Chromosome = parsed_entry[5] )
        SE_data.close()


class Chemical(models.Model):
    CID = models.IntegerField()
    InChIKey = models.CharField(max_length = 27)
    SMILES = models.CharField(max_length = 1000)

    total_associated_side_effects = models.IntegerField(null=True, blank=True)
    associated_side_effects = models.ManyToManyField(SideEffect, blank=True)

    total_associated_genes = models.IntegerField(null=True, blank=True)
    associated_genes = models.ManyToManyField(Gene, blank = True)

    def __str__ (self):
        return 'CID: ' + str(self.CID)

    @staticmethod
    def initDatabase(): #Please only use this within the shell and only once
        if(len(Chemical.objects.all()) != 0): #The database is already filled with something
            print("The database is already filled.")
            return 
        
        CHEM_data = open('./data/SIDER_chemicals_stereo.tsv', 'r')
        CHEM_data.readline() #Skipping the first line
        for entry in CHEM_data:
            parsed_entry = entry.split('\t')
            Chemical.objects.create(CID = parsed_entry[1], InChIKey = parsed_entry[2], SMILES=parsed_entry[3])
        CHEM_data.close()
        
        


def initChemToSideEffectRelations():
    '''
    Establishes the Many-To-Many connection between Chemicals and Side Effects"
    '''
    #Just getting the dimensions of your matrix
    csv_data = open('/Users/jack/Desktop/chem_se_SIDER.csv', 'r')
    total_row = 0
    for line in csv_data:
        total_row += 1
    total_col = len(line.split(','))
    csv_data.close()
    
    print(total_row) # row = chem (1549)
    print(total_col) # col = side effects (4251)

    #Adding ManyToMany relations
    se_qs = SideEffect.objects.all()
    chem_qs = Chemical.objects.all()

    csv_data = open('/Users/jack/Desktop/chem_se_SIDER.csv', 'r') 
    for row in range(total_row):
        print(row)
        parsed_line = csv_data.readline().rstrip('\n').split(',')
        for col in range(total_col):
            if(parsed_line[col] == '1'): 
                chem_qs[row].side_effects.add(se_qs[col])
    csv_data.close()
    
def initChemToGeneRelations():
    '''
    Establishes the Many-To-Many connection between Chemical and Genes
    '''
    #Just getting the dimensions of your matrix
    csv_data = open('/Users/jack/Desktop/chem_gene_SIDER.csv', 'r')
    total_row = 0
    for line in csv_data:
        total_row += 1
    total_col = len(line.split(','))
    csv_data.close()
    
    print(total_row) #Row = Chem (1549)
    print(total_col) #Col = Gene (19116)

    #Adding ManyToMany relations
    gene_qs = Gene.objects.all()
    chem_qs = Chemical.objects.all()

    csv_data = open('/Users/jack/Desktop/chem_gene_SIDER.csv', 'r') 
    for row in range(total_row):
        print(row)
        parsed_line = csv_data.readline().rstrip('\n').split(',')
        for col in range(total_col):
            if(parsed_line[col] == '1'): 
                chem_qs[row].affected_genes.add(gene[col])
    csv_data.close()

def initGeneToSideEffectRelations():
    '''
    Establishes the Many-To-Many connection between Gene and SideEffects
    '''
    #Just getting the dimensions of your matrix
    csv_data = open('/Users/jack/Desktop/gene_se_Novartis.csv', 'r')
    total_row = 0
    for line in csv_data:
        total_row += 1
    total_col = len(line.split(','))
    csv_data.close()
    
    print(total_row) # Row = Gene  (19116)
    print(total_col) # Col = Side Effects (4251)

    #Adding ManyToMany relations
    gene_qs = Gene.objects.all()
    se_qs = SideEffect.objects.all()

    csv_data = open('/Users/jack/Desktop/gene_se_Novartis', 'r') 
    for row in range(total_row):
        print(row)
        parsed_line = csv_data.readline().rstrip('\n').split(',')
        for col in range(total_col):
            if(parsed_line[col] == '1'): 
                gene_qs[row].affected_genes.add(se_qs[col])
    csv_data.close()





def clearRelations():
    gene_qs = Gene.objects.all()
    chem_qs = Chemical.objects.all()
    se_qs = SideEffect.objects.all()

    for gene in gene_qs:
        gene.associated_side_effects.clear()
        gene.total_associated_chemicals = 0
        gene.total_associated_side_effects = 0
        gene.save()

    for chem in chem_qs:
        chem.associated_side_effects.clear()
        chem.associated_genes.clear()
        chem.total_associated_genes = 0
        chem.total_associated_side_effects = 0
        chem.save()
    
    for se in se_qs:
        se.total_associated_genes = 0
        se.total_associated_chemicals = 0
        se.save()