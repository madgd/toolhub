#!/usr/bin/env python
# encoding: utf-8
"""
    @author: madgd
    @license: (C) Copyright 2020-2021 madgd. All Rights Reserved.
    @contact: madgdtju@gmail.com
    @software: 
    @file: urls.py
    @time: 2020/10/29 10:05 上午
    @desc:
"""
from django.urls import path

from . import views

app_name = "excel_merge"
urlpatterns = [
    path('', views.index, name='index'),
    path('merge/', views.merge, name='merge')
]