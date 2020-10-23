#!/usr/bin/env python
# encoding: utf-8
"""
    @author: madgd
    @license: (C) Copyright 2020-2021 madgd. All Rights Reserved.
    @contact: madgdtju@gmail.com
    @software: 
    @file: urls.py
    @time: 2020/10/22 6:02 下午
    @desc:
"""
from django.urls import path

from . import views

app_name = "excel_split"
urlpatterns = [
    path('', views.index, name='index'),
    path('split/', views.split, name='split')
]