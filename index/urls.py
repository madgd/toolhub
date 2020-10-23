#!/usr/bin/env python
# encoding: utf-8
"""
    @author: madgd
    @license: (C) Copyright 2020-2021 madgd. All Rights Reserved.
    @contact: madgdtju@gmail.com
    @software: 
    @file: urls.py
    @time: 2020/10/23 2:06 下午
    @desc:
"""
from django.urls import path

from . import views

app_name = "index"
urlpatterns = [
    path('', views.index, name='index'),
]