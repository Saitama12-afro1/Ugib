from datetime import datetime
from pprint import pprint
from copy import deepcopy
import csv
import re
import requests
import glob
import os
import io
import logging

import xlsxwriter
from docxtpl import DocxTemplate
from xlsxwriter.workbook import Workbook
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse, FileResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.db.models import Q, F, Count, Subquery, OuterRef
from django.db import models
from django.core.mail import send_mail
from django_tables2 import SingleTableMixin, Table
from django_filters.views import FilterView
from django.db.models.query import QuerySet
from django.db import connection, transaction



from grr.models import UdsMetaGrrAccom, UdsMetaGrrStage, UdsMetaProtocols
from .models import History, UdsMeta, Bascet, Order, UserInfo,UdsMetaApr
from .HelperUdsMeta import HelperUdsMet, HelperUdsMetApr
from .forms import LoginForm, UdsMetaForm, WordDocFilling, RegisterForm, MyChangePassword, UdsMetaAprForm
from .history import decor
from .tables import UdsMetaTable, UdsMetaAprTable
from .filters import  UdsMetaFilters, HistoryFilter, UdsMetaAprFilters
from ugib.MyHasher import MyHasher

MyHasher = MyHasher()

logger = logging.getLogger(__name__)

tables = {"01fond": UdsMeta, "apr": UdsMetaApr, "grr-stage": UdsMetaGrrStage, "grr-accom":UdsMetaGrrAccom, "02maps": UdsMeta }



@login_required(login_url="/")
@transaction.atomic
def refresh_view(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # cursor.execute("REFRESH MATERIALIZED VIEW public.mat_view_v3 WITH data")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_apr_geom_mat_view_v1  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_grr_accom_geom_mat_view  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_grr_accom_mat_view  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_grr_geom_mat_view  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_grr_geom_mat_view_test  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_grr_stage_geom_mat_view  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_grr_stage_mat_view  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_ntb_final  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_protocols_geom_mat_view_v1  WITH data;")
            # cursor.execute("REFRESH MATERIALIZED VIEW public.uds_meta_view_mat_v4  WITH data;")
            cursor.execute("select diagnostic.refresh_mat_view()")
        cur_page_link = request.POST["cur_page"]
        return redirect(request.META.get('HTTP_REFERER') + f"?page={cur_page_link}/")
            

@login_required(login_url="/")
def profile(request):
    context = {}
    user = request.user
    form = WordDocFilling()
    context["orders"] = user.orders.all()
    context["history"] = []
    try:
        context["allUdsMeta"] = Bascet.objects.get(my_user_id = user.id).udsMeta.all()#Изменить
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

        
    def generate_str_for_count(num):# функция для определения окончания слова в зависимости от числительного 
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


@login_required(login_url="/")
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



class HistoryView(FilterView):
    filterset_class = HistoryFilter
    template_name = "crud/history/history.html"
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["history"] = History.objects.all().order_by("-id")
        f = HistoryFilter(self.request.GET, queryset= context["history"])
        context["filter"] = f
        p = Paginator(f.qs, 20)
        page_number = self.request.GET.get('page')
        page_obj = p.get_page(page_number)
        context["page_obj"] = page_obj

        iniz = self.request.user.first_name.split(" ")
        iniz = iniz[0][0] + "." + iniz[1][0] + "."
        context["iniz"] = iniz
        # context["table"] = HistoryTable(context["history"])
        if not  user.is_superuser:
            return page_not_found(self.request,404)
        return context
    

@login_required(login_url="/")
def history_views(request):
    context = {}
    user = request.user
    
    context["history"] = History.objects.all().order_by("-id")
    f = HistoryFilter(request.GET, queryset= context["history"])
    context["filter"] = f
    p = Paginator(f.qs, 20)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context["page_obj"] = page_obj

    iniz = request.user.first_name.split(" ")
    iniz = iniz[0][0] + "." + iniz[1][0] + "."
    context["iniz"] = iniz
    # context["table"] = HistoryTable(context["history"])
    if not  user.is_superuser:
        return page_not_found(request,404)
    
    template ="crud/history/history.html"
    
    return render(request, template, context)

def get_uniq_id(choise, fond):
    num = {"01fond": "01", "apr": "13", "grr-stage": "14", "grr-accom":"14", "02maps": "02" }
    current_date = datetime.strftime(datetime.now(), "%d.%m.%Y")
    if choise[0].isdigit():
        number_fond = choise[:2]
    else:
        number_fond = "01"
    buff = tables[fond].objects.order_by("-oid").first()
    old_uniq = buff.uniq_id
    old_date = buff.stor_date
    count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
    d, m, y = (current_date.split('.'))
    n = num[fond]

    if current_date == old_date:
        return f"g{n}s{number_fond}y{y}m{m}d{d}n{int(count) + 1}e"
    else:
        return f"g{n}s{number_fond}y{y}m{m}d{d}n{1}e"

def test(request):
    if request.method == "POST":
        data = request.POST["stor_folder"]
        if data == "":
            return JsonResponse("0", safe=False)
        obj = tables[request.POST["choise"]].objects.filter(stor_folder__startswith= data)
        if obj:
            return JsonResponse("1", safe=False)
        return JsonResponse("0", safe=False)
        

def create_post(request):
    print(request.META.get('HTTP_REFERER'))
    user = request.user
    data_models = UdsMeta
    if data_models is UdsMeta:
            choise = '01fond'
    if data_models is UdsMetaApr:
        choise = 'apr'
    if data_models is UdsMetaGrrStage:
        choise = 'grr-stage'
    if data_models is UdsMetaGrrAccom:
        choise = 'grr-accom'
        
    if request.method == "POST":
        form_data = HelperUdsMet.credte_dict_from_js_dict(request.POST)
        try:
            cur_page_link = form_data.pop('nt_pag')
        except KeyError:
            cur_page_link = 1
            
        try:
            with transaction.atomic():
                if choise == 'apr':
                    buff: dict = deepcopy(form_data)
                    buff.pop('path_cloud_protocol')
                    buff.pop('path_local_protocol')
                    data_models.objects.create(**buff)
                    form_data['path_local'] = form_data.pop('path_local_protocol')
                    form_data['path_cloud'] = form_data.pop('path_cloud_protocol')
                    UdsMetaProtocols.objects.create(**form_data)
                else:
                    data_models.objects.create(**form_data)
                
                @decor
                def arr():
                    return "create", choise
                
                arr(user, data_models.objects.get(uniq_id =  form_data["uniq_id"])) 
                
        except IntegrityError:
            uniq_id = form_data["uniq_id"]
            uniq_id = uniq_id[:len(uniq_id) - 2] + str(int(uniq_id[len(uniq_id) - 2:len(uniq_id) - 1]) + 1) + uniq_id[len(uniq_id) - 1:]
            form_data["uniq_id"] = uniq_id
            data_models.objects.create(**form_data)
            logger.error(" create not valid key")
        except Exception as e:
            logger.error(f" create {str(e)}")
        return redirect(request.META.get('HTTP_REFERER') + f"?page={cur_page_link}")
    

class UdsMetaHTMxTableView(SingleTableMixin, FilterView): # представление для базовой страницы
    table_class = UdsMetaTable
    data_models = UdsMeta
    
    def get_queryset(self):
        # print(self.data_models.objects.all())
        try:
            bascet = Bascet.objects.get(my_user_id = self.request.user.id).udsMeta.all()
        except:
            bascet = []
        uds_meta = self.data_models.objects.all()
        logger.info(f"Load {self.data_models} page")    
        for i in bascet:
            uds_meta = uds_meta.filter(~Q(oid = i.oid))
        return uds_meta.order_by("-oid")

    filterset_class = UdsMetaFilters
    paginate_by = 25
    login_form = LoginForm()
    register_form =  RegisterForm()
    redirect_url = "/"
    
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
        super_user_username = ("vahrushev@tsnigri.ru", "uvarova@tsnigri.ru",  "test@mail.ru","chernyshov@tsnigri.ru") # пользователи с доступ к CRUD-операциям
        user = request.user
        if self.data_models is UdsMeta:
            choise = '01fond'
        if self.data_models is UdsMetaApr:
            choise = 'apr'
        if self.data_models is UdsMetaGrrStage:
            choise = 'grr-stage'
        if self.data_models is UdsMetaGrrAccom:
            choise = 'grr-accom'
        
        if 'del' in request.POST:
            try:
                cur_page_link = request.POST["current_page"]
            except KeyError:
                cur_page_link = 1
            try:
                with transaction.atomic():
                    udsMetaObj = self.data_models.objects.get(oid = request.POST["oid"])
                    @decor 
                    def arr():
                        return "del", choise
                    arr(user, self.data_models.objects.get(oid =  request.POST["oid"]))
                    with connection.cursor() as cursor:
                        if choise == 'grr-stage':
                            cursor.execute(f'DELETE FROM uds_meta_grr_stage_geom WHERE uniq_id = %s',[udsMetaObj.uniq_id])
                        elif choise == 'grr-accom':
                            cursor.execute(f'DELETE FROM uds_meta_grr_accom_geom WHERE uniq_id = %s',[udsMetaObj.uniq_id])
                            
                    udsMetaObj.delete()
                    
            except ObjectDoesNotExist:
                logger.error("When removed ObjectDoesNotExist")
            return redirect(request.META.get('HTTP_REFERER') + f"?page={cur_page_link}")
        
        elif 'exc' in request.POST:
            form_data = HelperUdsMet.create_dict_from_uds(self.data_models.objects.get(oid = request.POST['oid']))#обернуть в тру execept
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
            allUdsMeta = self.data_models.objects.all().order_by("-oid")
            with open('stockitems_misuper.csv', 'w', newline="", encoding="utf-8") as myfile:  
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",", dialect=csv.Dialect.delimiter)
                wr.writerow(HelperUdsMet._all_columns,)
                for i in allUdsMeta:
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
                    return redirect(self.redirect_url)
                try:
                    user = User.objects.get(username = login_form.cleaned_data["username"])
                    if MyHasher.check_password(login_form.cleaned_data["password"], user.password):
                        login(request, user)
                        return redirect(self.redirect_url)

                except ObjectDoesNotExist:
                    logger.error("When login ObjectDoesNotExist")
                    return redirect(self.redirect_url)
                
        elif 'register' in request.POST:
            if register_form.is_valid(password=request.POST["password"]):
                if register_form.cleaned_data["username"] in super_user_username:
                    try:
                        user = User(username = register_form.cleaned_data["username"], 
                                    first_name = request.POST["first_name"] +" "+ request.POST["sur_name"], last_name = request.POST["last_name"], \
                                    is_staff = True, is_superuser = True
                        )
                        
                        user.set_password(register_form.cleaned_data["password"])
                        user.save()
                        user_info = UserInfo(user_id = user.id, departament = request.POST["departament"], position = request.POST["position"])
                        user_info.save()
                    except ObjectDoesNotExist:
                        logger.error("When register ObjectDoesNotExist")
                else:
                    user = User(username = register_form.cleaned_data["username"], first_name = request.POST["first_name"] + " " + request.POST["sur_name"],
                                last_name =request.POST["last_name"],
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
                    return redirect(self.redirect_url)
            else:
                return redirect(self.redirect_url)#сделать доп ошибку
                    
        elif 'create' in request.POST: 
            form_data = HelperUdsMet.credte_dict_from_js_dict(request.POST)
            try:
                cur_page_link = form_data.pop('nt_pag')
            except KeyError:
                cur_page_link = 1
            try:
                with transaction.atomic():
                    form_data["uniq_id"] = get_uniq_id(request.POST["choise"],request.POST["fond"].lower())
                        
                    if choise == 'apr':
                        buff: dict = deepcopy(form_data)
                        buff.pop('path_cloud_protocol')
                        buff.pop('path_local_protocol')
                        self.data_models.objects.create(**buff)
                        form_data['path_local'] = form_data.pop('path_local_protocol')
                        form_data['path_cloud'] = form_data.pop('path_cloud_protocol')
                        UdsMetaProtocols.objects.create(**form_data)
                        
                    else:
                        self.data_models.objects.create(**form_data)
                    @decor
                    def arr():
                        return "create", choise
                    arr(user, self.data_models.objects.get(uniq_id =  form_data["uniq_id"])) 
                return redirect(request.META.get('HTTP_REFERER') + f"?page={cur_page_link}")
                
            except IntegrityError:

                uniq_id = form_data["uniq_id"]
                uniq_id = uniq_id[:len(uniq_id) - 2] + str(int(uniq_id[len(uniq_id) - 2:len(uniq_id) - 1]) + 1) + uniq_id[len(uniq_id) - 1:]
                form_data["uniq_id"] = uniq_id
                self.data_models.objects.create(**form_data)
                logger.error(" create not valid key")
                print(2222222)
                return redirect(request.META.get('HTTP_REFERER') + f"?page={cur_page_link}")
                
            except Exception as e:
                logger.error(f"When create {str(e)}")
                logger.error(request.POST)
                logger.error("------------------")
                response = HttpResponse()
                return response
                # return redirect(request.META.get('HTTP_REFERER') + f"?page={cur_page_link}")
        
        elif 'update' in request.POST:
            form_data = HelperUdsMet.credte_dict_from_js_dict(request.POST)
            try:
                cur_page_link = form_data.pop('nt_pag')
            except KeyError:
                cur_page_link = 1
            try:
                with transaction.atomic():
                    if choise == 'apr':
                        try:
                            buff =  self.data_models.objects.get(oid = request.POST["oid"])
                            UdsMetaProtocols.objects.filter(uniq_id = buff.uniq_id).update(**form_data)
                        except:
                            pass
                    self.data_models.objects.filter(oid = form_data["oid"]).update(**form_data) 
                    
                    
                    @decor
                    def arr():
                        return "update", choise

                    arr(user, self.data_models.objects.get(uniq_id =  form_data["uniq_id"]))
                    
                   
            except ObjectDoesNotExist:
                print("error")
                logger.error("When update ObjectDoesNotExist")
            if cur_page_link == '0':
                uniq_id = form_data["uniq_id"]
                return redirect(request.META.get('HTTP_REFERER') + f"?query={uniq_id}")
            
            return redirect(request.META.get('HTTP_REFERER') + f"?page={cur_page_link}")
                # return redirect(self.redirect_url)
        
        elif 'upd_one' in request.POST:
            try:
                cur_page_link = request.POST["current_page"]
            except KeyError:
                cur_page_link = 1
            try:
                with transaction.atomic():
                    if choise == 'apr':
                        try:
                            buff =  self.data_models.objects.get(oid = request.POST["oid"])
                            UdsMetaProtocols.objects.filter(uniq_id = buff.uniq_id).update(**{request.POST['cls']:request.POST['upd_val']})
                        except ObjectDoesNotExist:
                            logger.error("When upd_one ObjectDoesNotExist")
                        
                    self.data_models.objects.filter(oid = request.POST["oid"]).update(**{request.POST['cls']:request.POST['upd_val']})
                    
                    @decor
                    def arr():
                            return "update", choise
                    arr(user, self.data_models.objects.get(oid =  int(request.POST["oid"])))

            except ObjectDoesNotExist:
                logger.error("When upd_one ObjectDoesNotExist")
            if cur_page_link == '0':
                uniq_id = self.data_models.objects.get(oid = request.POST["oid"]).uniq_id
                return redirect(request.META.get('HTTP_REFERER') + f"?query={uniq_id}")
            return redirect(request.META.get('HTTP_REFERER') + f"?page={cur_page_link}")
        
        elif 'bascet' in request.POST:
            udsMetaObj = self.data_models.objects.get(oid = request.POST["oid"])
            user = request.user
            bascet, created  = Bascet.objects.get_or_create(my_user = user)
            udsMetaObj.bascets.add(bascet)
            
            @decor
            def arr():
                return "bascet", choise
            arr(user, self.data_models.objects.get(oid =  request.POST["oid"]))
            
            return redirect(self.redirect_url) 
        
        elif 'export_exel_partially' in request.POST:
            filename = 'result_query.xlsx'
            response = FileResponse(open(filename, 'rb'))
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['X-Sendfile'] = filename
            return response

    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buff = self.data_models.objects.order_by("-oid").first()
        # stor_phys_dict = {} 
        # buff_2 = self.data_models.objects.all()
        # for i in buff_2:
        #     stor_phys_dict.update({i.stor_desc: stor_phys_dict.get(i.stor_desc, 0) + 1})
        # context["stor_phys_p"] = dict(sorted(stor_phys_dict.items(), reverse=True,key=lambda item: item[1]))
        # import pprint        
        # pprint.pprint(context["stor_phys_p"])
        context["form"] = self.login_form
        context["register_form"] = self.register_form
        context["user"] = self.request.user
        context["common_user"] = self.request.user.groups.filter(name = "common_user").exists()
        context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
        context["choise"] = "01fond"
        context["super_users"] = self.request.user.username in  ("vahrushev@tsnigri.ru", "uvarova@tsnigri.ru",  "chernyshov@tsnigri.ru", 'test@mail.ru')
        d, m, y = (context["current_date"].split('.'))# 14.10.2022 
        old_uniq = buff.uniq_id
        old_date = buff.stor_date
        try:
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
        except AttributeError:
            count = 0

        if context["current_date"] == old_date:
            context["uniq_id"] = f"g01s01y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g01s01y{y}m{m}d{d}n{1}e"
        return context

    
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "crud/index/01fond/index_table_partial.html"
        else:
            template_name = "crud/index/01fond/index_table_htmx.html"
        return template_name
    

def get_html_uds(request):
    context = {}
    context["user"] = request.user
    context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
    iniz = request.user.first_name.split(" ")
    iniz = iniz[0][0] + "." + iniz[1][0] + "."#Создание инициалов из Имени и Отчества
    context["iniz"] = iniz
    context["userInfo"] = UserInfo.objects.get(user_id = request.user.id)
    if ("fond" not in request.GET):
        fond = "01FOND".lower()
    else:
        fond = request.GET["fond"].lower()
    if 'oid' in request.GET:
        context["record"] = UdsMeta.objects.get(oid = request.GET["oid"])
        return render(request, 'crud/form/update.html', context=context)
    context["choise"] = request.GET["choise"]
    choise = context["choise"]
    context["uniq_id"] = create_uniq_id(choise=choise,current_date = context["current_date"], fond = fond)
    return render(request, f"crud/form/{fond}/{choise}.html", context=context)

    
    
def get_html_apr(request):
    context = {}
    context["user"] = request.user
    context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
    iniz = request.user.first_name.split(" ")
    iniz = iniz[0][0] + "." + iniz[1][0] + "."#Создание инициалов из Имени и Отчества
    context["iniz"] = iniz
    context["userInfo"] = UserInfo.objects.get(user_id = request.user.id)
    date = context["current_date"].replace(".", "_")
    buff = UdsMetaApr.objects.order_by("-oid").first() 
    
    try:
        last_count_stor_desc =  int(buff.stor_desc[len(buff.stor_desc) - 2:]) + 1
        if last_count_stor_desc % 10 == last_count_stor_desc:
            last_count_stor_desc = "0" + str(last_count_stor_desc)
    except ValueError:
        last_count_stor_desc = ''
        
    date = date.split("_")
    date = date[2] + "_" + date[1] + "_" + date[0]
    stor_desc = context["stor_desc"] = f"{date} Протокол " 
    context["path_local_protocol"] = f"\\\pegas\\UDS\\13APR_PR\\01_PROTOCOLS\\"
    stor_desc = stor_desc.replace(" ", "%20")
    context["path_cloud_protocol"] = f"http://cloud.tsnigri.ru/apps/files/?dir=/13-01-ПРОТОКОЛЫ%20АПРОБАЦИИ%20ПР/"
    # buff2 = UdsMeta.objects.filter(obj_sub_group = "02RFGF").order_by("-oid").first()
    if 'oid' in request.GET:
        context["record"] = UdsMetaApr.objects.get(oid = request.GET["oid"])
        return render(request, 'crud/form/update_apr.html', context=context)
    if "APR" == request.GET["choise"]:
        context["choise"] = "apr"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "crud/form/apr/13APR.html", context=context)



def create_uniq_id(choise:str,current_date:datetime, fond = "") ->str: # Функция создает уникальный идентификатор
        buff = UdsMeta.objects.order_by("-oid").first()
        old_uniq = buff.uniq_id
        old_date = buff.stor_date
        count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
        name_fond = choise[0] + choise[1]
        d, m, y = (current_date.split('.'))# 14.10.2022 
        print(fond, choise)
        if choise == "apr":
            buff = UdsMetaApr.objects.order_by("-oid").first()
            old_uniq = buff.uniq_id
            old_date = buff.stor_date
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
            if current_date == old_date:
                return f"g13s01y{y}m{m}d{d}n{int(count) + 1}e"
            else:
                return f"g13s01y{y}m{m}d{d}n{1}e"
        if fond == "02maps":
            buff = UdsMeta.objects.filter(uniq_id__istartswith=f'g02s{name_fond}').order_by("-oid").first()
            if buff != None:
                old_uniq = buff.uniq_id
                old_date = buff.stor_date
                count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]   
            else:
                count = 1
            if current_date == old_date:
                return f"g02s{name_fond}y{y}m{m}d{d}n{int(count) + 1}e"
            else:
                return f"g02s{name_fond}y{y}m{m}d{d}n1e"
        if choise == "grr-stage":
            buff = UdsMetaGrrStage.objects.order_by("-oid").first()
            old_uniq = buff.uniq_id
            old_date = buff.stor_date
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
            if current_date == old_date:
                return f"g14s01y{y}m{m}d{d}n{int(count) + 1}e"
            else:
                return f"g14s01y{y}m{m}d{d}n{1}e"
        if choise == "grr-accom":
            buff = UdsMetaGrrAccom.objects.order_by("-oid").first()
            old_uniq = buff.uniq_id
            old_date = buff.stor_date
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]   
            if current_date == old_date:
                return f"g14s01y{y}m{m}d{d}n{int(count) + 1}e"
            else:
                return f"g14s01y{y}m{m}d{d}n{1}e"
        if choise == "02MAPS":
            buff = UdsMeta.objects.filter(uniq_id__istartswith='g02s04').order_by("-oid").first()
            old_uniq = buff.uniq_id
            old_date = buff.stor_date
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]   
            if current_date == old_date:
                return f"g02s04y{y}m{m}d{d}n{int(count) + 1}e"
            else:
                return f"g02s04y{y}m{m}d{d}n1e"
        
        if current_date == old_date:
            return f"g01s{name_fond}y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             return f"g01s{name_fond}y{y}m{m}d{d}n{1}e"
       

def password_change(request):
    form = MyChangePassword()
    all_mails = [x.username for x in User.objects.all()]
    if request.method == "POST":
        form = MyChangePassword(request.POST)
        if form.is_valid():
            form.test_pas()
            form.test_mail(all_mails)
            password = form.cleaned_data["password"]
            user = User.objects.get(username = form.cleaned_data["mail"])
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("/")
    context = {}
    context["form"] = form
    return render(request, "crud/password_change.html" ,context=context )
   
# queryset = UdsMetaApr.objects.annotate(test = Subquery(UdsMetaProtocols.objects.filter(
#                                                             uniq_id = OuterRef('uniq_id')).values("path_local")
#                                                        , output_field = models.TextField()
#                                                     ))
# table = UdsMetaAprTable(queryset)
# print(", ".join(map(str, table.rows[0])))
# h = 2
# for item in table.as_values():
#     print(item)
#     h += 1
#     if h == 4: break
   
class UdsMetaAprHTMxTableView(UdsMetaHTMxTableView,SingleTableMixin, FilterView):
    queryset = UdsMetaApr.objects.annotate(path_cloud_protocols = Subquery(UdsMetaProtocols.objects.filter(
                                                            uniq_id = OuterRef('uniq_id')).values("path_local")
                                                       , output_field = models.TextField()
                                                    ))
    table_class = UdsMetaAprTable
    data_models = UdsMetaApr
    redirect_url = "/apr/"


    filterset_class = UdsMetaAprFilters
    
    paginate_by = 25
    login_form = LoginForm()
    register_form =  RegisterForm()
            
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # stor_phys_dict = {} 
        # buff = UdsMetaApr.objects.order_by("-oid")
        # for i in buff:
        #     stor_phys_dict.update({i.spat_num_grid: stor_phys_dict.get(i.spat_num_grid, 0) + 1})
        # context["stor_phys_p"] = dict(sorted(stor_phys_dict.items(), reverse=True,key=lambda item: item[1]))        
        # pprint(context["stor_phys_p"])
        
        context["choise"] = "apr"
        
        return context

    
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "crud/index/apr/index_table_apr_partial.html"
        else:
            template_name = "crud/index/apr/index_table_apr_htmx.html"
        return template_name