# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Chemical, SideEffect, Gene

# Register your models here.

admin.site.register(SideEffect)
admin.site.register(Chemical)
admin.site.register(Gene)