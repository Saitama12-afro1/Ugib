from datetime import datetime
from pprint import pprint
import csv
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
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.decorators.csrf import csrf_exempt


from.models import History, UdsMeta, Bascet, Order
from .HelperUdsMeta import HelperUdsMet
from .forms import LoginForm, UdsMetaForm, WordDocFilling
from .history import decor
from .tables import UdsMetaTable
from .filters import  UdsMetaFilters


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
    print(11212121)
    return render(request,'crud/errors/404.html', {'path': request.path}, status = 404 )



def history_views(request):
    context = {}
    user = request.user
    context["history"] = History.objects.all()
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
    print(resp.request.headers, resp.status_code)
    
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
    return redirect("/table")

class UdsMetaHTMxTableView(SingleTableMixin, FilterView):
    table_class = UdsMetaTable
    queryset = UdsMeta.objects.all().order_by("-oid")
    filterset_class = UdsMetaFilters
    paginate_by = 25
    form = LoginForm()
    create_form = UdsMetaForm()

    def post(self, request,*args, **kwargs):
        login_form = LoginForm(request.POST)
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
                return redirect('/table')
            return redirect('/table')
        elif 'login' in request.POST:
            if login_form.is_valid():
                user = authenticate(username = login_form.cleaned_data["username"], password = login_form.cleaned_data["password"])
            
                if user is not None:
                    login(request, user)
                    return redirect("/table")
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
        elif 'update' in request.POST:
            pass
            
        return redirect("/table")
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["create_form"] = self.create_form
        context["user"] = self.request.user
        return context
    
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "crud/index/index_table_partial.html"
        else:
            template_name = "crud/index/index_table_htmx.html"
        return template_name
    
