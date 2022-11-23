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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.db.models import Q
from django.core.mail import send_mail
from django_tables2 import SingleTableMixin, Table
from django_filters.views import FilterView
from django.db.models.query import QuerySet

from grr.models import UdsMetaGrrAccom, UdsMetaGrrStage
from .models import History, UdsMeta, Bascet, Order, UserInfo,UdsMetaApr
from .HelperUdsMeta import HelperUdsMet, HelperUdsMetApr
from .forms import LoginForm, UdsMetaForm, WordDocFilling, RegisterForm, MyChangePassword, UdsMetaAprForm
from .history import decor
from .tables import UdsMetaTable, UdsMetaAprTable
from .filters import  UdsMetaFilters, HistoryFilter, UdsMetaAprFilters



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

@login_required(login_url="/")
def history_views(request):
    context = {}
    user = request.user
    user_info = UserInfo.objects.get(user_id = user.id)
    context["history"] = History.objects.all().order_by("-id")
    p = Paginator(context["history"], 20)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context["page_obj"] = page_obj
    f = HistoryFilter(request.GET, queryset= context["history"])
    context["filter"] = f
    iniz = request.user.first_name.split(" ")
    iniz = iniz[0][0] + "." + iniz[1][0] + "."
    context["iniz"] = iniz
    # context["table"] = HistoryTable(context["history"])
    if user.username not in ("vahrushev@tsnigri.ru", "uvarova@tsnigri.ru", "test@mail.ru"):
        return page_not_found(request,404)
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
        super_user_username = ("vahrushev@tsnigri.ru", "uvarova@tsnigri.ru", "gening@tsnigri.ru", "uscharova@tsnigri.ru", "test@mail.ru", "mukhina@tsnigri.ru", "t1@mail.ru") # пользователи с доступ к CRUD-операциям
        user = request.user
        if 'del' in request.POST:
            try:
                udsMetaObj = self.data_models.objects.get(oid = request.POST["oid"])
                @decor 
                def arr():
                    return "del"
                arr(user, self.data_models.objects.get(oid =  request.POST["oid"]))
                udsMetaObj.delete()
            except ObjectDoesNotExist:
                return redirect(self.redirect_url)
            return redirect(self.redirect_url)
        
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
                    return redirect(self.redirect_url)
            else:
                return redirect(self.redirect_url)#сделать доп ошибку
                    
                    
        elif 'create' in request.POST:
            try:          
                form_data = HelperUdsMet.credte_dict_from_js_dict(request.POST)
                self.data_models.objects.create(**form_data)
        
                @decor
                def arr():
                    return "create"
                arr(user, self.data_models.objects.get(uniq_id =  form_data["uniq_id"])) 
                
            except IntegrityError:
                pass
            return redirect(self.redirect_url) 
        
        elif 'update' in request.POST:
            form_data = HelperUdsMet.credte_dict_from_js_dict(request.POST)
            try:
                self.data_models.objects.filter(oid = form_data["oid"]).update(**form_data)  
                @decor
                def arr():
                    return "update"
                arr(user, self.data_models.objects.get(uniq_id =  form_data["uniq_id"]))
            except ObjectDoesNotExist:
                return redirect(self.redirect_url)
        
        elif 'upd_one' in request.POST:
            try:
                self.data_models.objects.filter(oid = request.POST["oid"]).update(**{request.POST['cls']:request.POST['upd_val']})
                @decor
                def arr():
                        return "update"
                arr(user, self.data_models.objects.get(oid =  int(request.POST["oid"])))
                return redirect(self.redirect_url)
            except ObjectDoesNotExist:
                return redirect(self.redirect_url)
        
        elif 'bascet' in request.POST:
            udsMetaObj = self.data_models.objects.get(oid = request.POST["oid"])
            user = request.user
            bascet, created  = Bascet.objects.get_or_create(my_user = user)
            udsMetaObj.bascets.add(bascet)
            
            @decor
            def arr():
                return "bascet"
            arr(user, self.data_models.objects.get(oid =  request.POST["oid"]))
            
            return redirect(self.redirect_url) 
            
        return redirect(self.redirect_url)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # stor_phys_dict = {} 
        buff = self.data_models.objects.order_by("-oid").first()
        # for i in buff:
        #     stor_phys_dict.update({i.obj_orgs: stor_phys_dict.get(i.obj_orgs, 0) + 1})
        # context["stor_phys_p"] = dict(sorted(stor_phys_dict.items(), reverse=True,key=lambda item: item[1]))        
        # print(context["stor_phys_p"])
        context["form"] = self.login_form
        context["register_form"] = self.register_form
        context["user"] = self.request.user
        context["common_user"] = self.request.user.groups.filter(name = "common_user").exists()
        context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
        context["choise"] = "01FOUND"
        d, m, y = (context["current_date"].split('.'))# 14.10.2022 
        old_uniq = buff.uniq_id
        old_date = buff.stor_date
        try:
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
        except AttributeError:
            pass

        if context["current_date"] == old_date:
            context["uniq_id"] = f"g01s01y{y}m{m}d{d}n{int(count) + 1}e"
        else:
             context["uniq_id"] = f"g01s01y{y}m{m}d{d}n{1}e"
        return context

    
    def get_template_names(self): 
        if self.request.htmx:
            template_name = "crud/index/01found/index_table_partial.html"
        else:
            template_name = "crud/index/01found/index_table_htmx.html"
        return template_name
    

def get_html_uds(request):
    context = {}
    context["user"] = request.user
    context["current_date"] =  datetime.strftime(datetime.now(), "%d.%m.%Y")
    iniz = request.user.first_name.split(" ")
    iniz = iniz[0][0] + "." + iniz[1][0] + "."#Создание инициалов из Имени и Отчества
    context["iniz"] = iniz
    context["userInfo"] = UserInfo.objects.get(user_id = request.user.id)
  
    # buff2 = UdsMeta.objects.filter(obj_sub_group = "02RFGF").order_by("-oid").first()
    if 'oid' in request.GET:
        context["record"] = UdsMeta.objects.get(oid = request.GET["oid"])
        return render(request, 'crud/form/update.html', context=context)
    if request.GET["choise"] == "01TSNIGRI":
        context["choise"] = "01TSNIGRI"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "crud/form/01found/01TSNIGRI.html", context=context)
    if request.GET["choise"] == "02RFGF":
        context["choise"] = "02RFGF"
        context["uniq_id"] = create_uniq_id(choise= context["choise"],current_date = context["current_date"] )
        return render(request, "crud/form/01found/02RFGF.html", context=context)
    if request.GET["choise"] == "03TGF":
        context["choise"] = "03TGF"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "crud/form/01found/03TGF.html", context=context)
    if request.GET["choise"] == "04OTHER_ORG":
        context["choise"] = "04OTHER_ORG"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "crud/form/01found/04OTHER_ORG.html", context=context)
    
    
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
    last_count_stor_desc =  int(buff.stor_desc[len(buff.stor_desc) - 2:]) + 1
    if last_count_stor_desc % 10 == last_count_stor_desc:
        last_count_stor_desc = "0" + str(last_count_stor_desc)
    context["stor_desc"] = f"{date} Протокол {last_count_stor_desc}" 
    # buff2 = UdsMeta.objects.filter(obj_sub_group = "02RFGF").order_by("-oid").first()
    if 'oid' in request.GET:
        context["record"] = UdsMetaApr.objects.get(oid = request.GET["oid"])
        return render(request, 'crud/form/update.html', context=context)
    if "APR" == request.GET["choise"]:
        context["choise"] = "apr"
        context["uniq_id"] = create_uniq_id(choise=context["choise"],current_date = context["current_date"] )
        return render(request, "crud/form/apr/13APR.html", context=context)



def create_uniq_id(choise:str,current_date:datetime) ->str: # Функция создает уникальный идентификатор
        buff = UdsMeta.objects.order_by("-oid").first()
        old_uniq = buff.uniq_id
        old_date = buff.stor_date
        count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
        name_fond = choise[0] + choise[1]
        d, m, y = (current_date.split('.'))# 14.10.2022 
        if choise == "apr":
            buff = UdsMetaApr.objects.order_by("-oid").first()
            old_uniq = buff.uniq_id
            old_date = buff.stor_date
            count = re.search(r"n[0-9]+", old_uniq ).group(0)[1:]
            if current_date == old_date:
                return f"g13s01y{y}m{m}d{d}n{int(count) + 1}e"
            else:
                return f"g13s01y{y}m{m}d{d}n{1}e"
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
            request.user.set_password(password)
            request.user.save()
            return redirect("/")
    context = {}
    context["form"] = form
    return render(request, "crud/password_change.html" ,context=context )
   
   
class UdsMetaAprHTMxTableView(UdsMetaHTMxTableView,SingleTableMixin, FilterView): # представление для базовой страницы
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