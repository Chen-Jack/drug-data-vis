# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SideEffect(models.Model):
    name = models.CharField(max_length = 50)
    UMLS_CUI = models.CharField(max_length = 8)
    intermodel = models.ManyToManyField('self', through='se_similarity', symmetrical=False)

    total_associated_genes = models.IntegerField(null = True, blank=True)
    total_associated_chemicals = models.IntegerField(null = True, blank=True)

    
    def __str__ (self):
        return self.name

    @staticmethod
    def initDatabase(): #Please only use this within the shell and only once.
        if(len(SideEffect.objects.all()) != 0): 
            print("The database is already filled.")
            return 
        
        SE_data = open('./data/SideEffectList.tsv', 'r')
        SE_data.readline() #Skipping the first line
        for entry in SE_data:
            parsed_entry = entry.strip('\n').split('\t')
            SideEffect.objects.create(name = parsed_entry[2], UMLS_CUI = parsed_entry[1])
        SE_data.close()

class Gene(models.Model):
    HGNC = models.IntegerField()
    Symbol = models.CharField(max_length = 20)
    UniProt = models.CharField(max_length = 300)
    Chromosome = models.CharField(max_length = 50)
    intermodel = models.ManyToManyField('self', through='gene_similarity', symmetrical=False)

    total_associated_side_effects = models.IntegerField(null = True, blank = True)
    associated_side_effects = models.ManyToManyField(SideEffect, blank = True)

    total_associated_chemicals = models.IntegerField(null = True, blank=True)
 
    def __str__(self):
        return self.Symbol

    @staticmethod
    def initDatabase():
        if(len(Gene.objects.all()) != 0): 
            print("The database is already filled.")
            return 
        
        gene_data = open('./data/protein_list.tsv', 'r')
        gene_data.readline() #Skipping the first line
        counter = 0
        for entry in gene_data:
            parsed_entry = entry.strip('\n').split('\t')
            Gene.objects.create(HGNC = int(parsed_entry[1][5:]), Symbol = parsed_entry[2], UniProt = parsed_entry[3], Chromosome = parsed_entry[4] )
        gene_data.close()


class Chemical(models.Model):
    CID = models.IntegerField()
    InChIKey = models.CharField(max_length = 27)
    SMILES = models.CharField(max_length = 1000)
    intermodel = models.ManyToManyField('self', through='chem_similarity', symmetrical=False)

    total_associated_side_effects = models.IntegerField(null=True, blank=True)
    associated_side_effects = models.ManyToManyField(SideEffect, blank=True)

    total_associated_genes = models.IntegerField(null=True, blank=True)
    associated_genes = models.ManyToManyField(Gene, blank = True)

    def __str__ (self):
        return 'CID: ' + str(self.CID)

    @staticmethod
    def initDatabase(): #Please only use this within the shell and only once
        if(len(Chemical.objects.all()) != 0):
            print("The database is already filled.")
            return 
        
        CHEM_data = open('./data/SIDER_chemicals_stereo.tsv', 'r')
        CHEM_data.readline() #Skipping the first line
        for entry in CHEM_data:
            parsed_entry = entry.split('\t')
            Chemical.objects.create(CID = parsed_entry[1], InChIKey = parsed_entry[2], SMILES=parsed_entry[3])
        CHEM_data.close()


#Intermediate Tables for intermodel similarities and interactions, not meant to be used standalone models
class se_similarity(models.Model):
    se_a = models.ForeignKey(SideEffect, related_name='se_a_set')
    se_b = models.ForeignKey(SideEffect, related_name='se_b_set')
    similarity = models.FloatField(null=True, blank=True)

    def __str__(self):
        return('<' + str(self.se_a) + ', ' + str(self.se_b) + '> '+ str(self.similarity) )

def parse_se_similarity():
    if(len(se_similarity.objects.all()) != 0):
        print("Your similarity table already has entries in it.")
        return
    se_sim_data = open('/Users/jack/Downloads/se_se_blank.csv', 'r')
    dim =  len(se_sim_data.readline().split(',')) #Grabbing the dimension
    print("dim", dim)
    se_sim_data.close()

    se_sim_data = open('/Users/jack/Downloads/se_se_blank.csv', 'r')

    for i in range(dim):
        parsed_line = se_sim_data.readline().strip('\n').split(',')
        print(i)
        for j in range(i):
            if(parsed_line[j] != '0' and parsed_line[j] != '1'):
                se_a = SideEffect.objects.all()[i]
                se_b = SideEffect.objects.all()[j]
                se_similarity.objects.create(se_a = se_a , se_b=se_b, similarity = float(parsed_line[j]))
                
    se_sim_data.close()

    print("Finished establishing side effect - side effect similarities.")
   
class chem_similarity(models.Model):
    chem_a= models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name='chem_a_set')
    chem_b = models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name='chem_b_set')
    similarity = models.FloatField(null=True, blank=True)

    def __str__(self):
        return('<' + str(self.chem_a) + ', ' + str(self.chem_b) + '> '+ str(self.similarity) )    

def parse_chem_similarity():
    if(len(chem_similarity.objects.all()) != 0):
        print("Your similarity table already has entries in it.")
        return
    #Determining dimensions
    chem_sim_data = open('/Users/jack/Downloads/chem_chem_SIDER.csv', 'r')
    dim =  len(chem_sim_data.readline().split(',')) #Grabbing the dimension
    chem_sim_data.close()

    chem_sim_data = open('/Users/jack/Downloads/chem_chem_SIDER.csv', 'r')

    for i in range(dim):
        parsed_line = chem_sim_data.readline().strip('\n').split(',')
        print(i)
        for j in range(i):
            if(parsed_line[j] != '0' and parsed_line[j] != '1'):
                chem_a = Chemical.objects.all()[i]
                chem_b = Chemical.objects.all()[j]
                chem_similarity.objects.create(chem_a = chem_a , chem_b=chem_b, similarity = float(parsed_line[j]))
                
    chem_sim_data.close()

    print("Finished establishing chem-chem similarities.")
    

class gene_similarity(models.Model):
    gene_a = models.ForeignKey(Gene, related_name='gene_a_set')
    gene_b = models.ForeignKey(Gene, related_name='gene_b_set')
    similarity = models.FloatField(null=True, blank=True)
    interaction = models.FloatField(null=True, blank=True)


    def __str__(self):
        return('<' + str(self.gene_a) + ', ' + str(self.gene_b) + '> '+ str(self.similarity) )

def parse_gene_similarity():
    if(len(gene_similarity.objects.all()) != 0):
        print("Your similarity table already has entries in it.")
        return
    #Determining dimensions
    gene_sim_data = open('/Users/jack/Downloads/prot_prot_sim.csv', 'r')
    dim =  len(gene_sim_data.readline().split(','))
    gene_sim_data.close()

    #Begin parsing

    gene_sim_data = open('/Users/jack/Downloads/prot_prot_sim.csv', 'r')
    gene_interaction_data = open('/Users/jack/Downloads/ppi_biogrid.csv', 'r')

    for i in range(dim):
        parsed_sim_line = gene_sim_data.readline().strip('\n').split(',')
        parsed_int_line = gene_interaction_data.readline().strip('\n').split(',')
        print(i)
        for j in range(i):
            if((parsed_sim_line[j] != '0' and parsed_sim_line[j] != '1') or \
            (parsed_int_line[j] != '0')):
                gene_a = Gene.objects.all()[i]
                gene_b = Gene.objects.all()[j]
                gene_similarity.objects.create(gene_a = gene_a , gene_b=gene_b, \
                similarity = float(parsed_sim_line[j]), interaction = float(parsed_int_line[j]))
                
    gene_sim_data.close()       
    gene_int_data.close()

    print("Finished establishing gene-gene relations.")

#Many To Many Functions
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
                chem_qs[row].associated_side_effects.add(se_qs[col])
    csv_data.close()

    for chem in chem_qs:
        chem.total_associated_side_effects = len(chem.associated_side_effects.all())
        chem.save()

    for se in se_qs:
        se.total_associated_chemicals = len(se.chemical_set.all())
        se.save()
    
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
                chem_qs[row].associated_genes.add(gene_qs[col])
    csv_data.close()

    for chem in chem_qs:
        chem.total_associated_genes = len(chem.associated_genes.all())
        chem.save()

    for gene in gene_qs:
        gene.total_associated_chemicals = len(gene.chemical_set.all())
        gene.save()

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

    csv_data = open('/Users/jack/Desktop/gene_se_Novartis.csv', 'r') 
    for row in range(total_row):
        print(row)
        parsed_line = csv_data.readline().rstrip('\n').split(',')
        for col in range(total_col):
            if(parsed_line[col] == '1'): 
                gene_qs[row].associated_side_effects.add(se_qs[col])
    csv_data.close()

    for gene in gene_qs:
        gene.total_associated_side_effects = len(gene.associated_side_effects.all())
        gene.save()

    for se in se_qs:
        se.total_associated_genes = len(se.gene_set.all())
        se.save()

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