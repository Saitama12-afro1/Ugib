from datetime import datetime
from pprint import pprint
import csv
import re
import glob
import os
import io

import xlsxwriter
from docxtpl import DocxTemplate
from xlsxwriter.workbook import Workbook
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.contrib.auth.hashers import PBKDF2PasswordHasher


from crud.views import create_uniq_id, UdsMetaHTMxTableView
from crud.models import History, UdsMeta, Bascet, Order, UserInfo
from .models import UdsMetaGrrStage, UdsMetaGrrAccom
from crud.HelperUdsMeta import HelperUdsMet, HelperUdsMetApr
from crud.forms import LoginForm, UdsMetaForm, WordDocFilling, RegisterForm, MyChangePassword
from crud.history import decor
from .tables import UdsMetaGrrAccomTable, UdsMetaGrrStageTable
from .filters import  UdsMetaGrrStageFilter, UdsMetaGrrAccomFilter



class UdsMetaGrrStageHTMxTableView(UdsMetaHTMxTableView, SingleTableMixin, FilterView): # представление для базовой страницы
    table_class = UdsMetaGrrStageTable
    data_models = UdsMetaGrrStage
    redirect_url = "/grr-stage/"
    filterset_class = UdsMetaGrrStageFilter
    paginate_by = 25
    login_form = LoginForm()
    register_form =  RegisterForm()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # stor_phys_dict = {} 
        # buff = UdsMetaGrrStage.objects.order_by("-oid")
        # for i in buff:
        #     stor_phys_dict.update({i.status: stor_phys_dict.get(i.status, 0) + 1})
        # context["stor_phys_p"] = dict(sorted(stor_phys_dict.items(), reverse=True,key=lambda item: item[1]))        
        # pprint(context["stor_phys_p"])
        
        context["choise"] = "grr_stage"
        return context

    
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "grr/index/grr_stage/index_table_grr_stage_partial.html"
        else:
            template_name = "grr/index/grr_stage/index_table_grr_stage_htmx.html"
        return template_name


def get_html_grr_stage(request):
    context = {}
    context["user"] = request.user
    context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
    iniz = request.user.first_name.split(" ")
    iniz = iniz[0][0] + "." + iniz[1][0] + "."#Создание инициалов из Имени и Отчества
    context["iniz"] = iniz
    context["userInfo"] = UserInfo.objects.get(user_id = request.user.id)
    # buff2 = UdsMeta.objects.filter(obj_sub_group = "02RFGF").order_by("-oid").first()
    print(request.GET)
    if 'oid' in request.GET:
        context["record"] = UdsMetaGrrStage.objects.get(oid = request.GET["oid"])
        return render(request, 'crud/form/update_apr.html', context=context)
    if 'oid_accom' in request.GET:
        context["record"] = UdsMetaGrrAccom.objects.get(oid = request.GET["oid_accom"])
        return render(request, 'crud/form/update_apr.html', context=context)
    if "GRR-STAGE" == request.GET["choise"]:
        context["choise"] = "grr-stage"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "grr/form/grr_stage.html", context=context)
    if "GRR-ACCOM" == request.GET["choise"]:
        context["choise"] = "grr-accom"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "grr/form/grr_accom.html", context=context)
    
    

class UdsMetaGrrAccomHTMxTableView(UdsMetaHTMxTableView,SingleTableMixin, FilterView): # представление для базовой страницы
    table_class = UdsMetaGrrAccomTable
    data_models = UdsMetaGrrAccom
    redirect_url = "/grr-accom/"
    
    filterset_class = UdsMetaGrrAccomFilter
    paginate_by = 25
    login_form = LoginForm()
    register_form =  RegisterForm()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stor_phys_dict = {} 
        # buff = UdsMeta.objects.order_by("-oid")
        # for i in buff:
        #     stor_phys_dict.update({i.stor_folder: stor_phys_dict.get(i.stor_folder, 0) + 1})
        # context["stor_phys_p"] = dict(sorted(stor_phys_dict.items(), reverse=True,key=lambda item: item[1]))        
        # pprint(context["stor_phys_p"])
        context["choise"] = "grr_accom"
        
        return context

    
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "grr/index/grr_accom/index_table_grr_accom_partial.html"
        else:
            template_name = "grr/index/grr_accom/index_table_grr_accom_htmx.html"
        return template_name
