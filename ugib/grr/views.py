from datetime import datetime
from pprint import pprint
import csv
import re
import requests
import glob
import os
import io

import xlsxwriter
from docxtpl import DocxTemplate
from xlsxwriter.workbook import Workbook
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from crud.views import create_uniq_id
from crud.models import History, UdsMeta, Bascet, Order, UserInfo
from .models import UdsMetaGrrStage, UdsMetaGrrAccom
from crud.HelperUdsMeta import HelperUdsMet, HelperUdsMetApr
from crud.forms import LoginForm, UdsMetaForm, WordDocFilling, RegisterForm, MyChangePassword
from crud.history import decor
from .tables import UdsMetaGrrAccomTable, UdsMetaGrrStageTable
from .filters import  UdsMetaGrrStageFilter, UdsMetaGrrAccomFilter


def test(request):
    return HttpResponse("dsds")

class UdsMetaGrrStageHTMxTableView(SingleTableMixin, FilterView): # представление для базовой страницы
    table_class = UdsMetaGrrStageTable
    def get_queryset(self):
        try:
            bascet = Bascet.objects.get(my_user_id = self.request.user.id).udsMeta.all()
        except:
            bascet = []
        uds_meta_apr = UdsMetaGrrStage.objects.all()
        for i in bascet:
            uds_meta_apr = uds_meta_apr.filter(~Q(oid = i.oid))
        return uds_meta_apr.order_by("-oid")
    filterset_class = UdsMetaGrrStageFilter
    paginate_by = 25
    login_form = LoginForm()
    register_form =  RegisterForm()
    def get_table_kwargs(self):# Здесь исключаются из поля видимости столбцы недоступные пользователю не принадлежащему определенной группе
        if self.request.user.is_active:
            if self.request.user.groups.filter(name = "common_user").exists():   
                return {
                    'exclude':('Delete','Update'),
                    }
            else:
                return {
                    'exclude':('Bascet'),
                    
                    }
        else:
            return {
                    'exclude':('Bascet','Delete','Update')
                    }    
            
    
    def post(self, request,*args, **kwargs):
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)
        super_user_username = ("vahrushev@tsnigri.ru", "uvarova@tsnigri.ru", "gening@tsnigri.ru", "uscharova@tsnigri.ru", "test@mail.ru", "mukhina@tsnigri.ru", "t1@mail.ru") # пользователи с доступ к CRUD-операциям
        user = request.user
        if 'del' in request.POST:
            try:
                UdsMetaGrrStageObj = UdsMetaGrrStage.objects.get(oid = request.POST["oid"])
                @decor 
                def arr():
                    return "del"
                arr(user, UdsMetaGrrStage.objects.get(oid =  request.POST["oid"]))
                UdsMetaGrrStageObj.delete()
            except ObjectDoesNotExist:
                return redirect('/grr-stage/')
            return redirect('/grr-stage/')
        
        elif 'exc' in request.POST:
            form_data = HelperUdsMet.create_dict_from_uds(UdsMetaGrrStage.objects.get(oid = request.POST['oid']))#обернуть в тру execept
            
            with open('stockitems_misuper.csv', 'w', newline="", encoding="cp1251") as myfile:  
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",", dialect=csv.Dialect.delimiter)
                wr.writerow(HelperUdsMet._all_columns,)
                wr.writerow(list(form_data.values()))
                
            for csvfile in glob.glob(os.path.join('.', '*.csv')):
                workbook = xlsxwriter.Workbook()
                workbook = Workbook(csvfile[:-4] + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='cp1251') as f:
                    reader = csv.reader(f)
                    for r, row in enumerate(reader):
                        for c, col in enumerate(row):
                            worksheet.write(r, c, col)
                workbook.close()
                
            filename = 'stockitems_misuper.xlsx'
            with io.open( filename, mode ='rb') as myfile:  
                response = HttpResponse(
                    myfile,
                    content_type='text/xlsx'
                )
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
        
        elif 'export_exel' in request.POST:
            allUdsMetaGrrStage = UdsMetaGrrStage.objects.all().order_by("-oid")
            with open('stockitems_misuper.csv', 'w', newline="", encoding="utf-8") as myfile:  
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",", dialect=csv.Dialect.delimiter)
                wr.writerow(HelperUdsMet._all_columns,)
                for i in allUdsMetaGrrStage:
                    form_data = HelperUdsMet.create_dict_from_uds(i)
                    wr.writerow(list(form_data.values()))

            for csvfile in glob.glob(os.path.join('.', '*.csv')):
                workbook = xlsxwriter.Workbook()
                workbook = Workbook(csvfile[:-4] + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for r, row in enumerate(reader):
                        for c, col in enumerate(row):
                            worksheet.write(r, c, col)
                workbook.close()
                
            filename = 'stockitems_misuper.xlsx'
            response = FileResponse(open(filename, 'rb'))
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['X-Sendfile'] = filename
            return response
               
        elif 'login' in request.POST:
            if login_form.is_valid():
                user = authenticate(username = login_form.cleaned_data["username"], password = login_form.cleaned_data["password"])
            
                if user is not None:
                    login(request, user)
                    return redirect("/grr-stage/")
                
        elif 'register' in request.POST:
            if register_form.is_valid(password=request.POST["password"]):
                if register_form.cleaned_data["username"] in super_user_username:
                    try:
                        user = User(username = register_form.cleaned_data["username"], 
                                    first_name = request.POST["first_name"], last_name = request.POST["last_name"], \
                                    is_staff = True
                        )
                        user.set_password(register_form.cleaned_data["password"])
                        user.save()
                        user_info = UserInfo(user_id = user.id, departament = request.POST["departament"], position = request.POST["position"])
                        user_info.save()
                    except:
                        pass
                else:
                    user = User(username = register_form.cleaned_data["username"], first_name = request.POST["first_name"], last_name =request.POST["last_name"],
                                 is_superuser = False)
                    user.set_password(register_form.cleaned_data["password"])
                    user.save()
                    group = Group.objects.get(pk = 1)
                    group.user_set.add(user)
                    user_info = UserInfo(user_id = user.id, departament = request.POST["departament"], position = request.POST["position"])
                    user_info.save()
                aut_user = authenticate(username = user.username, password = register_form.cleaned_data["password"])
            
                if aut_user is not None:
                    login(request, user)
                    return redirect("/grr-stage/")
            else:
                return redirect('/grr-stage/')#сделать доп ошибку
                    
                    
        elif 'create' in request.POST:
            try:          
                form_data = HelperUdsMetApr.credte_dict_from_js_dict(request.POST)
                UdsMetaGrrStage.objects.create(**form_data)
        
                @decor
                def arr():
                    return "create"
                arr(user, UdsMetaGrrStage.objects.get(uniq_id =  form_data["uniq_id"])) 
                
            except IntegrityError:
                pass
            return redirect('/grr-stage/') 
        
        elif 'update' in request.POST:
            form_data = HelperUdsMetApr.credte_dict_from_js_dict(request.POST)
            
            try:
                UdsMetaGrrStage.objects.filter(oid = form_data["oid"]).update(**form_data)  
                @decor
                def arr():
                    return "update"
                arr(user, UdsMetaGrrStage.objects.get(uniq_id =  form_data["uniq_id"]))
            except ObjectDoesNotExist:
                
                return redirect("/grr-stage/")
        
        elif 'upd_one' in request.POST:
            try:
                UdsMetaGrrStage.objects.filter(oid = request.POST["oid"]).update(**{request.POST['cls']:request.POST['upd_val']})
                @decor
                def arr():
                        return "update"
                arr(user, UdsMetaGrrStage.objects.get(oid =  int(request.POST["oid"])))
                return redirect("/grr-stage/")
            except ObjectDoesNotExist:
                return redirect("/grr-stage/")
        
        elif 'bascet' in request.POST:
            UdsMetaGrrStageObj = UdsMetaGrrStage.objects.get(oid = request.POST["oid"])
            user = request.user
            bascet, created  = Bascet.objects.get_or_create(my_user = user)
            UdsMetaGrrStageObj.bascets.add(bascet)
            
            @decor
            def arr():
                return "bascet"
            arr(user, UdsMetaGrrStage.objects.get(oid =  request.POST["oid"]))
            
            return redirect('/grr-stage/') 
            
        return redirect("/grr-stage/")
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # stor_phys_dict = {} 
        # buff = UdsMetaGrrStage.objects.order_by("-oid")
        # for i in buff:
        #     stor_phys_dict.update({i.status: stor_phys_dict.get(i.status, 0) + 1})
        # context["stor_phys_p"] = dict(sorted(stor_phys_dict.items(), reverse=True,key=lambda item: item[1]))        
        # pprint(context["stor_phys_p"])
        buff = UdsMetaGrrStage.objects.order_by("-oid").first() 
        context["form"] = self.login_form
        context["register_form"] = self.register_form
        context["user"] = self.request.user
        context["common_user"] = self.request.user.groups.filter(name = "common_user").exists()
        context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
        context["choise"] = "grr_stage"
        d, m, y = (context["current_date"].split('.'))# 14.10.2022
        old_uniq = buff.uniq_id
        old_date = buff.stor_date
        try:
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
        except AttributeError:
            pass
        if context["current_date"] == old_date:
            context["uniq_id"] = f"g14s01y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g14s01y{y}m{m}d{d}n{1}e"
        return context

    
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "grr/index/index_table_grr_stage_partial.html"
        else:
            template_name = "grr/index/index_table_grr_stage_htmx.html"
        return template_name


def get_html_grr_stage(request):
    context = {}
    context["user"] = request.user
    context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
    iniz = request.user.first_name.split(" ")
    iniz = iniz[0][0] + "." + iniz[1][0] + "."#Создание инициалов из Имени и Отчества
    context["iniz"] = iniz
    context["userInfo"] = UserInfo.objects.get(user_id = request.user.id)
    date = context["current_date"].replace(".", "_")
    buff = UdsMetaGrrStage.objects.order_by("-oid").first()  
    # buff2 = UdsMeta.objects.filter(obj_sub_group = "02RFGF").order_by("-oid").first()
    if 'oid' in request.GET:
        context["record"] = UdsMetaGrrStage.objects.get(oid = request.GET["oid"])
        return render(request, 'crud/form/update.html', context=context)
    if "GRR-STAGE" == request.GET["choise"]:
        context["choise"] = "grr-stage"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "grr/form/grr_stage.html", context=context)
    if "GRR-ACCOM" == request.GET["choise"]:
        context["choise"] = "grr-accom"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "grr/form/grr_accom.html", context=context)
    
    


class UdsMetaGrrAccomHTMxTableView(SingleTableMixin, FilterView): # представление для базовой страницы
    table_class = UdsMetaGrrAccomTable
    def get_queryset(self):
        try:
            bascet = Bascet.objects.get(my_user_id = self.request.user.id).udsMeta.all()
        except:
            bascet = []
        uds_meta_grr_accom = UdsMetaGrrAccom.objects.all()
        for i in bascet:
            uds_meta_grr_accom = uds_meta_grr_accom.filter(~Q(oid = i.oid))
        return uds_meta_grr_accom.order_by("-oid")
    filterset_class = UdsMetaGrrAccomFilter
    paginate_by = 25
    login_form = LoginForm()
    register_form =  RegisterForm()
    def get_table_kwargs(self):# Здесь исключаются из поля видимости столбцы недоступные пользователю не принадлежащему определенной группе
        if self.request.user.is_active:
            if self.request.user.groups.filter(name = "common_user").exists():   
                return {
                    'exclude':('Delete','Update'),
                    }
            else:
                return {
                    'exclude':('Bascet'),
                    
                    }
        else:
            return {
                    'exclude':('Bascet','Delete','Update')
                    }    
            
    
    def post(self, request,*args, **kwargs):
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)
        super_user_username = ("vahrushev@tsnigri.ru", "uvarova@tsnigri.ru", "gening@tsnigri.ru", "uscharova@tsnigri.ru", "test@mail.ru", "mukhina@tsnigri.ru", "t1@mail.ru") # пользователи с доступ к CRUD-операциям
        user = request.user
        if 'del' in request.POST:
            try:
                UdsMetaGrrAccomObj = UdsMetaGrrAccom.objects.get(oid = request.POST["oid"])
                @decor 
                def arr():
                    return "del"
                arr(user, UdsMetaGrrAccom.objects.get(oid =  request.POST["oid"]))
                UdsMetaGrrAccomObj.delete()
            except ObjectDoesNotExist:
                return redirect('/grr-accom/')
            return redirect('/grr-accom/')
        
        elif 'exc' in request.POST:
            form_data = HelperUdsMet.create_dict_from_uds(UdsMetaGrrAccom.objects.get(oid = request.POST['oid']))#обернуть в тру execept
            
            with open('stockitems_misuper.csv', 'w', newline="", encoding="cp1251") as myfile:  
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",", dialect=csv.Dialect.delimiter)
                wr.writerow(HelperUdsMet._all_columns,)
                wr.writerow(list(form_data.values()))
                
            for csvfile in glob.glob(os.path.join('.', '*.csv')):
                workbook = xlsxwriter.Workbook()
                workbook = Workbook(csvfile[:-4] + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='cp1251') as f:
                    reader = csv.reader(f)
                    for r, row in enumerate(reader):
                        for c, col in enumerate(row):
                            worksheet.write(r, c, col)
                workbook.close()
                
            filename = 'stockitems_misuper.xlsx'
            with io.open( filename, mode ='rb') as myfile:  
                response = HttpResponse(
                    myfile,
                    content_type='text/xlsx'
                )
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
        
        elif 'export_exel' in request.POST:
            allUdsMetaGrrAccom = UdsMetaGrrAccom.objects.all().order_by("-oid")
            with open('stockitems_misuper.csv', 'w', newline="", encoding="utf-8") as myfile:  
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",", dialect=csv.Dialect.delimiter)
                wr.writerow(HelperUdsMet._all_columns,)
                for i in allUdsMetaGrrAccom:
                    form_data = HelperUdsMet.create_dict_from_uds(i)
                    wr.writerow(list(form_data.values()))

            for csvfile in glob.glob(os.path.join('.', '*.csv')):
                workbook = xlsxwriter.Workbook()
                workbook = Workbook(csvfile[:-4] + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for r, row in enumerate(reader):
                        for c, col in enumerate(row):
                            worksheet.write(r, c, col)
                workbook.close()
                
            filename = 'stockitems_misuper.xlsx'
            response = FileResponse(open(filename, 'rb'))
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['X-Sendfile'] = filename
            return response
               
        elif 'login' in request.POST:
            if login_form.is_valid():
                user = authenticate(username = login_form.cleaned_data["username"], password = login_form.cleaned_data["password"])
            
                if user is not None:
                    login(request, user)
                    return redirect("/grr-accom/")
                
        elif 'register' in request.POST:
            if register_form.is_valid(password=request.POST["password"]):
                if register_form.cleaned_data["username"] in super_user_username:
                    try:
                        user = User(username = register_form.cleaned_data["username"], 
                                    first_name = request.POST["first_name"], last_name = request.POST["last_name"], \
                                    is_staff = True
                        )
                        user.set_password(register_form.cleaned_data["password"])
                        user.save()
                        user_info = UserInfo(user_id = user.id, departament = request.POST["departament"], position = request.POST["position"])
                        user_info.save()
                    except:
                        pass
                else:
                    user = User(username = register_form.cleaned_data["username"], first_name = request.POST["first_name"], last_name =request.POST["last_name"],
                                 is_superuser = False)
                    user.set_password(register_form.cleaned_data["password"])
                    user.save()
                    group = Group.objects.get(pk = 1)
                    group.user_set.add(user)
                    user_info = UserInfo(user_id = user.id, departament = request.POST["departament"], position = request.POST["position"])
                    user_info.save()
                aut_user = authenticate(username = user.username, password = register_form.cleaned_data["password"])
            
                if aut_user is not None:
                    login(request, user)
                    return redirect("/grr-accom/")
            else:
                return redirect('/grr-accom/')#сделать доп ошибку
                    
                    
        elif 'create' in request.POST:
            try:          
                form_data = HelperUdsMetApr.credte_dict_from_js_dict(request.POST)
                UdsMetaGrrAccom.objects.create(**form_data)
        
                @decor
                def arr():
                    return "create"
                arr(user, UdsMetaGrrAccom.objects.get(uniq_id =  form_data["uniq_id"])) 
                
            except IntegrityError:
                pass
            return redirect('/grr-accom/') 
        
        elif 'update' in request.POST:
            form_data = HelperUdsMetApr.credte_dict_from_js_dict(request.POST)
            
            try:
                UdsMetaGrrAccom.objects.filter(oid = form_data["oid"]).update(**form_data)  
                @decor
                def arr():
                    return "update"
                arr(user, UdsMetaGrrAccom.objects.get(uniq_id =  form_data["uniq_id"]))
            except ObjectDoesNotExist:
                
                return redirect("/grr-accom/")
        
        elif 'upd_one' in request.POST:
            try:
                UdsMetaGrrAccom.objects.filter(oid = request.POST["oid"]).update(**{request.POST['cls']:request.POST['upd_val']})
                @decor
                def arr():
                        return "update"
                arr(user, UdsMetaGrrAccom.objects.get(oid =  int(request.POST["oid"])))
                return redirect("/grr-accom/")
            except ObjectDoesNotExist:
                return redirect("/grr-accom/")
        
        elif 'bascet' in request.POST:
            UdsMetaGrrAccomObj = UdsMetaGrrAccom.objects.get(oid = request.POST["oid"])
            user = request.user
            bascet, created  = Bascet.objects.get_or_create(my_user = user)
            UdsMetaGrrAccomObj.bascets.add(bascet)
            
            @decor
            def arr():
                return "bascet"
            arr(user, UdsMetaGrrAccom.objects.get(oid =  request.POST["oid"]))
            
            return redirect('/grr-accom/') 
            
        return redirect("/grr-accom/")
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # stor_phys_dict = {} 
        # buff = UdsMetaGrrStage.objects.order_by("-oid")
        # for i in buff:
        #     stor_phys_dict.update({i.obj_assoc_inv_nums: stor_phys_dict.get(i.obj_assoc_inv_nums, 0) + 1})
        # context["stor_phys_p"] = dict(sorted(stor_phys_dict.items(), reverse=True,key=lambda item: item[1]))        
        # pprint(context["stor_phys_p"])
        buff = UdsMetaGrrAccom.objects.order_by("-oid").first() 
        context["choise"] = "grr_accom"
        context["form"] = self.login_form
        context["register_form"] = self.register_form
        context["user"] = self.request.user
        context["common_user"] = self.request.user.groups.filter(name = "common_user").exists()
        context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
        d, m, y = (context["current_date"].split('.'))# 14.10.2022
        old_uniq = buff.uniq_id
        old_date = buff.stor_date
        try:
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
        except AttributeError:
            pass
        if context["current_date"] == old_date:
            context["uniq_id"] = f"g14s01y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g14s01y{y}m{m}d{d}n{1}e"
        return context

    
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "grr/index/index_table_grr_accom_partial.html"
        else:
            template_name = "grr/index/index_table_grr_accom_htmx.html"
        return template_name
