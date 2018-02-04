from .models import *

#Intermediate Tables for intermodel similarities and interactions, not meant to be used standalone models
class se_similarity(models.Model):
    se_a = models.ForeignKey(SideEffect, related_name='se_a_set')
    se_b = models.ForeignKey(SideEffect, related_name='se_b_set')
    similarity = models.FloatField(null=True, blank=True)

        
class chem_similarity(models.Model):
    chem_a= models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name='chem_a_set')
    chem_b = models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name='chem_b_set')
    similarity = models.FloatField(null=True, blank=True)

class gene_similarity(models.Model):
    gene_a = models.ForeignKey(Gene, related_name='gene_a_set')
    gene_b = models.ForeignKey(Gene, related_name='gene_b_set')
    similairty = models.FloatField(null=True, blank=True)
    interaction = models.FloatField(null=True, blank=True)