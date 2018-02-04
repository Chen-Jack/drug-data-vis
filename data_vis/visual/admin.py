# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Chemical, SideEffect, Gene, se_similarity,gene_similarity,chem_similarity

# Register your models here.

admin.site.register(SideEffect)
admin.site.register(Chemical)
admin.site.register(Gene)
admin.site.register(se_similarity)
admin.site.register(gene_similarity)
admin.site.register(chem_similarity)