from datetime import datetime
from multiprocessing import get_context
from pprint import pprint
import csv
import re
from secrets import choice
from turtle import position
from urllib import request
import requests
import json

from docxtpl import DocxTemplate

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.core.mail import send_mail
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.db.models.query import QuerySet


from .models import History, UdsMeta, Bascet, Order, UserInfo
from .HelperUdsMeta import HelperUdsMet
from .forms import LoginForm, UdsMetaForm, WordDocFilling, RegisterForm
from .history import decor
from .tables import UdsMetaTable, HistoryTable
from .filters import  UdsMetaFilters, HistoryFilter


def index(request):
    context = {}
    user = request.user
    allUdsMeta = UdsMeta.objects.all().order_by("-oid")
    login_form = LoginForm() 
    if user.is_active:
        try:
            context["Bascet"] = Bascet.objects.get(my_user_id = user.id).udsMeta.all()
        except ObjectDoesNotExist:
            context["Bascet"] = []
    else:
        context["Bascet"] = []
    paginator = Paginator(allUdsMeta,20)# Возможно изменить
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if 'update'  in request.POST:
            print(request.headers)
            form_data = HelperUdsMet.create_dict_from_query_set_without_oid(request.POST)  
            try:
                UdsMeta.objects.filter(oid = request.POST["oid"]).update(**form_data)
                @decor
                def arr():
                    return "update"
                arr(user, UdsMeta.objects.get(uniq_id =  request.POST["uniq_id"]))
            except ObjectDoesNotExist:
                pass
            return redirect("/")
        
        elif 'del' in request.POST:
            form_data = HelperUdsMet.create_dict_from_query_set(request.POST)
            try:
                udsMetaObj = UdsMeta.objects.get(oid = form_data["oid"])
                @decor # не работает при удалении связя слетают
                def arr():
                    return "del"
                arr(user, UdsMeta.objects.get(uniq_id =  request.POST["uniq_id"]))
                udsMetaObj.delete()
            except ObjectDoesNotExist:
                return redirect('/')
            return redirect('/')
        
        elif 'create' in request.POST:
            try:          
                form_data = HelperUdsMet.create_dict_from_query_set_without_oid(request.POST)
                UdsMeta.objects.create(**form_data)
        
                @decor
                def arr():
                    return "create"
                arr(user, UdsMeta.objects.get(uniq_id =  request.POST["uniq_id"]))
                
            except IntegrityError:
                pass
                        
        elif 'exp' in request.POST:
            form_data = HelperUdsMet.create_dict_from_query_set(request.POST)
            
            with open('stockitems_misuper.csv', 'w', newline="", encoding="cp1251") as myfile:  
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",", dialect=csv.Dialect.delimiter)
                wr.writerow(HelperUdsMet._all_columns,)
                wr.writerow(list(form_data.values()))
                
            with open('stockitems_misuper.csv', encoding="cp1251") as myfile:
                response = HttpResponse(myfile, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=stockitems_misuper.csv'
                return response
        
        elif 'login'  in request.POST:
            if login_form.is_valid():
                user = authenticate(username = login_form.cleaned_data["username"], password = login_form.cleaned_data["password"])
            
                if user is not None:
                    login(request, user)
                    return redirect("/")
            
        elif 'bascet' in request.POST:
            udsMetaObj = UdsMeta.objects.get(oid = request.POST["oid"])
            user = request.user
            bascet, created  = Bascet.objects.get_or_create(my_user = user)
            udsMetaObj.bascets.add(bascet)
            @decor
            def arr():
                return "bascet"
            arr(user, UdsMeta.objects.get(uniq_id =  request.POST["uniq_id"]))
            return redirect('/')
        
    if user.groups.filter(name = "common_user").exists():
        template = 'crud/index/index_for_common_user.html'
    else:
        template = "crud/index/index2.html"     
    context["page_obj"] = page_obj
    context["user"] = user
    context["login_form"] = login_form
    return render(request, template,context=context)




def profile(request):
    context = {}
    user = request.user
    form = WordDocFilling()
    context["orders"] = user.orders.all()
    context["history"] = []
    try:
        context["allUdsMeta"] = Bascet.objects.get(my_user_id = user.id).udsMeta.all()
    except ObjectDoesNotExist:
            allUdsMeta  = []
            context["allUdsMeta"] = allUdsMeta
    if request.method == 'POST':
        if "create_order" in request.POST:
            
            @decor
            def arr():
                return "create_order"
            arr(user, UdsMeta.objects.get(uniq_id =  request.POST["uniq_id"]), orderObj = True)
            
            form = WordDocFilling(request.POST)
            cont = { 'name_doc':'Запрашиваемый документ','col_labels': ['№ п/п', 'Директория хранения', 'Инвентарные номера в каталогах учета',
                                    'Автор (авторы)', 'Название объекта', 'Год составления объекта', 'Примечание'],
                    'mass': [] }
            
            for udsMEtaObj in context["allUdsMeta"]:
                buff = [udsMEtaObj.oid, udsMEtaObj.stor_folder, udsMEtaObj.obj_assoc_inv_nums, udsMEtaObj.obj_authors, udsMEtaObj.obj_name, udsMEtaObj.obj_year, 'test']
                cont['mass'].append({'cols':buff})
            if form.is_valid():
                cont["position"] = form.cleaned_data["position"]
                cont["departament"] = form.cleaned_data["departament"]
                cont["position"] = form.cleaned_data["position"]
                cont["username"] = form.cleaned_data["username"]
                cont["task"] = form.cleaned_data["task"]
            try:
                doc = DocxTemplate("crud/source/blank.docx")
                doc.render(cont)
                doc.save("crud/source/final_blank.docx")
                bascet = Bascet.objects.get(my_user_id = user.id)
                
                for i in context["allUdsMeta"]:
                    order = Order(datetimeAppend = datetime.now(), status = False, udsMeta_id = i.uniq_id)
                    order.save()
                    user.orders.add(order)

                    
                bascet.udsMeta.clear()
                return redirect("/profile")
            except PermissionError:
                pass
            # send_mail(
            #     'test',
            #     doc,
            #     'chernyshov@tsnigri.ru',
            #     ['chernyshov@tsnigri.ru'],
            #     fail_silently=False,
            # )
        elif "confirm_order" in request.POST:
            orders =  Order.objects.all()
            for el in orders:
                el.status = not el.status
                el.save()
           
            return redirect("/profile")

        
    def generate_str_for_count(num):
        array = ["заявка", "заявок", "заявки"]
        num = num % 100
        if num >= 11 and num <= 19:
            return(f"{num} {array[1]}")
        elif num % 10 == 1:
            return(f"{num} {array[0]}")
        elif num % 10 > 1 and num % 10 < 5:
            return(f"{num} {array[2]}")
        else: 
            return(f"{num} {array[1]}")
    
    context["count_elements_in_bascet"] = generate_str_for_count(len(context["allUdsMeta"]))
    
    if user.groups.filter(name = "common_user"):
        template = "crud/profile/profile_for_common_user.html"
    else: 
        context["orders"] = Order.objects.all()
        template = "crud/profile/profile.html"
    
    context["form"] = form
    paginator = Paginator(context["orders"],20)# Возможно изменить
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context["page_obj"] =  page_obj
    return render(request, template, context=context)

def logout(request):
    django_logout(request)
    return redirect("/")


def bascet(request):
    user = request.user
    allUdsMeta = Bascet.objects.filter(my_user_id = user.id).first().udsMeta.all().order_by("-oid")
    context = {}
    
    paginator = Paginator(allUdsMeta,20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    bascet = Bascet.objects.get(my_user_id = user.id)
    context["allUdsMeta"] = allUdsMeta
    context["page_obj"] = page_obj
    
    if request.method == 'POST':
        if "del" in request.POST:
            bascet.udsMeta.remove(UdsMeta.objects.get(oid = request.POST["oid"]))
        elif "create_order" in request.POST:
            cont = {'name_doc':'Запрашиваемый документ','col_labels': ['№ п/п', 'Директория хранения', 'Инвентарные номера в каталогах учета',
                    'Автор (авторы)', 'Название объекта', 'Год составления объекта', 'Примечание'],
                    'mass': [] }
            i = UdsMeta.objects.get(oid = request.POST["oid"])
            
            @decor
            def arr():
                return "create_order"
            arr(user, i, orderObj = True)
            
            buff = [i.oid, i.stor_folder, i.obj_assoc_inv_nums, i.obj_authors, i.obj_name, i.obj_year, 'test']
            cont['mass'].append({'cols':buff})
            try:
                doc = DocxTemplate("crud/source/blank.docx")
                doc.render(cont)
                doc.save("crud/source/final_blank.docx")
                bascet.udsMeta.remove(i)
            except PermissionError:
                pass
        
    if user.groups.filter(name = "common_user"):
        template = "crud/bascet.html"
    else:
        template = None
            
    return render(request, template, context=context)


def page_not_found(request, exception):
    return render(request,'crud/errors/404.html', {'path': request.path}, status = 404 )


def history_views(request):
    context = {}
    user = request.user
    context["history"] = History.objects.all()
    context["table"] = HistoryTable(context["history"])
    if user.groups.filter(name = "common_user"):
        template ="crud/history/history_for_common_user.html"
        context["history"] = user.histories.all()
    else:
        template ="crud/history/history.html"
    return render(request, template, context)

def test(request):
    uds = UdsMeta.objects.all().order_by("-oid")
    a = "https://cloud.tsnigri.ru/apps/files/?dir=/01-01-%D0%A4%D0%9E%D0%9D%D0%94%D0%9E%D0%92%D0%AB%D0%95%20%D0%9C%D0%90%D0%A2%D0%95%D0%A0%D0%98%D0%90%D0%9B%D0%AB%20%D0%A6%D0%9D%D0%98%D0%93%D0%A0%D0%98/8518-%D0%91%D0%B5%D1%80%D0%B5%D0%B7%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%AE.%D0%9A.%2C1986&fileid=5896026"
    b = "http://cloud.tsnigri.ru/apps/files/?dir=/01-01-ФОНДОВЫЕ МАТЕРИАЛЫ ЦНИГРИ/8518-Березиков Ю.К.,1986"
    resp  = requests.get(a,headers={"Host":"cloud.tsnigri.ru"})
    
    # answer = []
    # for i in uds:
    #     url = str(i.path_cloud_ref)
    #     print(url, end=" ")
    #     url = url.replace("http://cloud.tsnigri.ru/", "https://cloud.tsnigri.ru/login?redirect_url=")
    #     print(url)
    #     try:
    #         a = requests.get(url, headers={"Host":"cloud.tsnigri.ru"}, timeout=5)
    #         print(a.url,  a.status_code)
    #         if a.status_code == 404:
    #             answer.append(i.oid)
    #     except :
    #         answer.append(i.oid)
    
    # print(answer)
    if request.method == "POST":
        print(request.POST)
    return redirect("/")


# class HistoryView(SingleTableMixin, FilterView):
#     table_class = HistoryTable
#     queryset = History.objects.all()
#     filterset_class = HistoryFilter
#     paginate_by = 25
#     def get_template_names(self): 
#         if self.request.htmx:
#             template_name = "crud/history/history.html"
#         else:
#             template_name = "crud/history/history.html"
#         return template_name
    
    
    
class UdsMetaHTMxTableView(SingleTableMixin, FilterView):
    table_class = UdsMetaTable
    def get_queryset(self):
        try:
            bascet = Bascet.objects.get(my_user_id = self.request.user.id).udsMeta.all()
        except:
            bascet = []
        uds_meta = UdsMeta.objects.all()
        for i in bascet:
            uds_meta = uds_meta.filter(~Q(oid = i.oid))
            
        return uds_meta.order_by("-oid")
    
    filterset_class = UdsMetaFilters
    paginate_by = 25
    login_form = LoginForm()
    create_form = UdsMetaForm()
    register_form =  RegisterForm()
    def get_table_kwargs(self):
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
        register_form = LoginForm(request.POST)
        super_user_username = ("vahrushev@tsnigri.ru", "uvarova@tsnigri.ru", "gening@tsnigri.ru", "uscharova@tsnigri.ru", "test@mail.ru")
        user = request.user
        if 'del' in request.POST:
            try:
                udsMetaObj = UdsMeta.objects.get(oid = request.POST["oid"])
                
                @decor # не работает при удалении связя слетают
                def arr():
                    return "del"
                arr(user, UdsMeta.objects.get(oid =  request.POST["oid"]))
                udsMetaObj.delete()
            except ObjectDoesNotExist:
                return redirect('/')
            return redirect('/')
        
        elif 'login' in request.POST:
            if login_form.is_valid():
                user = authenticate(username = login_form.cleaned_data["username"], password = login_form.cleaned_data["password"])
            
                if user is not None:
                    login(request, user)
                    return redirect("/")
                
        elif 'register' in request.POST:
            if register_form.is_valid():
                if register_form.cleaned_data["username"] in super_user_username:
                    try:
                        user = User(username = register_form.cleaned_data["username"], 
                                    first_name = request.POST["first_name"], last_name = request.POST["last_name"], is_superuser = True,\
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
                    return redirect("/")
                    
                    
        elif 'create' in request.POST:
            try:          
                form_data = HelperUdsMet.credte_dict_from_js_dict(request.POST)
                UdsMeta.objects.create(**form_data)
        
                @decor
                def arr():
                    return "create"
                arr(user, UdsMeta.objects.get(uniq_id =  form_data["uniq_id"])) 
                
            except IntegrityError:
                pass
            return redirect('/') 
        
        elif 'update' in request.POST:
            form_data = HelperUdsMet.credte_dict_from_js_dict(request.POST)
            try:
                UdsMeta.objects.filter(oid = form_data["oid"]).update(**form_data)  
                @decor
                def arr():
                    return "update"
                arr(user, UdsMeta.objects.get(uniq_id =  form_data["uniq_id"]))
            except ObjectDoesNotExist:
                pass
        elif 'upd_one' in request.POST:
            UdsMeta.objects.filter(oid = request.POST["oid"]).update(**{request.POST['cls']:request.POST['upd_val']})
            return redirect("/")
        
        elif 'bascet' in request.POST:
            udsMetaObj = UdsMeta.objects.get(oid = request.POST["oid"])
            user = request.user
            bascet, created  = Bascet.objects.get_or_create(my_user = user)
            udsMetaObj.bascets.add(bascet)
            
            @decor
            def arr():
                return "bascet"
            arr(user, UdsMeta.objects.get(oid =  request.POST["oid"]))
            
            return redirect('/') 
            
        return redirect("/")
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # stor_phys_dict = {} 
        buff = UdsMeta.objects.order_by("-oid").first()
        # for i in buff:
        #     stor_phys_dict.update({i.obj_orgs: stor_phys_dict.get(i.obj_orgs, 0) + 1})
        # context["stor_phys_p"] = dict(sorted(stor_phys_dict.items(), reverse=True,key=lambda item: item[1]))        
        # print(context["stor_phys_p"])
        context["form"] = self.login_form
        context["register_form"] = self.register_form
        context["create_form"] = self.create_form
        context["user"] = self.request.user
        context["common_user"] = self.request.user.groups.filter(name = "common_user").exists()
        context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
        d, m, y = (context["current_date"].split('.'))# 14.10.2022 
        old_uniq = buff.uniq_id
        old_date = buff.stor_date
        count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
        
        if context["current_date"] == old_date:
            context["uniq_id"] = f"g01s01y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g01s01y{y}m{m}d{d}n{1}e"
        return context
 
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "crud/index/index_table_partial.html"
        else:
            template_name = "crud/index/index_table_htmx.html"
        return template_name
    

def get_html(request):
    context = {}
    context["user"] = request.user
    context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
    context["userInfo"] = UserInfo.objects.get(user_id = request.user.id)
    buff = UdsMeta.objects.order_by("-oid").first()
    # buff2 = UdsMeta.objects.filter(obj_sub_group = "02RFGF").order_by("-oid").first()
    d, m, y = (context["current_date"].split('.'))# 14.10.2022 
    old_uniq = buff.uniq_id
    old_date = buff.stor_date
    count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
    if request.GET["choise"] == "01TSNIGRI":
        context["choise"] = "01TSNIGRI"
        if context["current_date"] == old_date:
            context["uniq_id"] = f"g01s01y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g01s01y{y}m{m}d{d}n{1}e"
        return render(request, "crud/form/01TSNIGRI.html", context=context)
    elif request.GET["choise"] == "02RFGF":
        context["choise"] = "02RFGF"
        if context["current_date"] == old_date:
            context["uniq_id"] = f"g01s02y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g01s02y{y}m{m}d{d}n{1}e"
        return render(request, "crud/form/02RFGF.html", context=context)
    elif request.GET["choise"] == "03TGF":
        context["choise"] = "03TGF"
        if context["current_date"] == old_date:
            context["uniq_id"] = f"g01s03y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g01s03y{y}m{m}d{d}n{1}e"
        return render(request, "crud/form/03TGF.html", context=context)
    elif request.GET["choise"] == "04OTHER_ORG":
        context["choise"] = "04OTHER_ORG"
        if context["current_date"] == old_date:
            context["uniq_id"] = f"g01s04y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g01s04y{y}m{m}d{d}n{1}e"
        return render(request, "crud/form/04OTHER_ORG.html", context=context)
    