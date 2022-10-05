from datetime import datetime
from pprint import pprint
import csv
import requests

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

from.models import History, UdsMeta, Bascet, Order
from .HelperUdsMeta import HelperUdsMet
from .forms import LoginForm, WordDocFilling
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
    a = "https://cloud.tsnigri.ru/login?redirect_url=/apps/files/?dir%3D/01-04-%25D0%25A4%25D0%259E%25D0%259D%25D0%2594%25D0%259E%25D0%2592%25D0%25AB%25D0%2595%2520%25D0%259C%25D0%2590%25D0%25A2%25D0%2595%25D0%25A0%25D0%2598%25D0%2590%25D0%259B%25D0%25AB%2520%25D0%25A1%25D0%25A2%25D0%259E%25D0%25A0%25D0%259E%25D0%259D%25D0%259D%25D0%2598%25D0%25A5%2520%25D0%259E%25D0%25A0%25D0%2593%25D0%2590%25D0%259D%25D0%2598%25D0%2597%25D0%2590%25D0%25A6%25D0%2598%25D0%2599/6266-%25D0%259E%25D0%25BB%25D1%258C%25D1%2585%25D0%25BE%25D0%25B2%25D1%2581%25D0%25BA%25D0%25B8%25D0%25B9%2520%25D0%2590.%25D0%2598.,1963"
    resp  = requests.get(a)
    print(resp.request.headers, resp.status_code)
    
    answer = []
    for i in uds:
        url = str(i.path_cloud_ref)
        url = url.replace("http://cloud.tsnigri.ru/", "https://cloud.tsnigri.ru/login?redirect_url=")

        try:
            a = requests.get(url, headers={"Host":"cloud.tsnigri.ru"}, timeout=5)
            if a.status_code == 404:
                answer.append(i.oid)
        except :
            answer.append(i.oid)
    
    print(answer)
    return render(request, "crud/test.html")


class UdsMetaHTMxTableView(SingleTableMixin, FilterView):
    table_class = UdsMetaTable
    queryset = UdsMeta.objects.all().order_by("-oid")
    filterset_class = UdsMetaFilters
    paginate_by = 25
    def post(self, request,*args, **kwargs):
        if request.method == "POST":
            print("arrrrr")
            print(request.POST)
            return HttpResponseRedirect("/table")

    def get_template_names(self): 
        
        if self.request.htmx:
            print(1111111111)
            template_name = "crud/index/index_table_htmx.html"
          
        else:
            print(2222222)
            template_name = "crud/index/index_table_htmx.html"
        return template_name
    
    
