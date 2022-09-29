from pprint import pprint
import csv
from re import A
from docxtpl import DocxTemplate

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User

from.models import UdsMeta, Bascet, Order, Statistic
from .HelperUdsMeta import HelperUdsMet

# def index(request):   
#     if request.method == "POST":
#         udsMetaForm = UdsMetaForm(request.POST)
#         if udsMetaForm.is_valid():
#             print(1111)
    
#     udsMetaForm = UdsMetaForm(initial={"stor_folder":"sasas"})
#     print(udsMetaForm.get_context())
#     udsAllValues = UdsMeta.objects.all()
#     masAllUdsValuesForms = []
#     for i in udsAllValues:
#         masAllUdsValuesForms.append(UdsMetaForm(initial=i.__dict__))
#     return render(request, "crud/index.html",{"masAllUdsValuesForms":masAllUdsValuesForms[0:10]})

def index(request):
    context = {}
    user = request.user
    allUdsMeta = UdsMeta.objects.all().order_by("-oid")
    paginator = Paginator(allUdsMeta,20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        if 'update'  in request.POST:
            form_data = HelperUdsMet.create_dict_from_query_set_without_oid(request.POST)  
            try:
                UdsMeta.objects.filter(oid = request.POST["oid"]).update(**form_data)
            except ObjectDoesNotExist:
                pass
            return redirect("/")
        
        elif 'del' in request.POST:
            form_data = HelperUdsMet.create_dict_from_query_set(request.POST)
            try:
                udsMetaObj = UdsMeta.objects.get(oid = form_data["oid"])
                udsMetaObj.delete()
            except ObjectDoesNotExist:
                return redirect('/')
            return redirect('/')
        
        elif 'create' in request.POST:
            try:          
                form_data = HelperUdsMet.create_dict_from_query_set_without_oid(request.POST)
                UdsMeta.objects.create(**form_data)
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
            user = authenticate(username = request.POST["mail"], password = request.POST["password"])
            
            if user is not None:
                login(request, user)
                return redirect("/")
            
        elif 'bascet' in request.POST:
            udsMetaObj = UdsMeta.objects.get(oid = request.POST["oid"])
            user = request.user
            bascet, created  = Bascet.objects.get_or_create(my_user = user)
    
            udsMetaObj.bascets.add(bascet)
            return redirect('/')

    if user.is_active:
        context["allUdsMeta"] = Bascet.objects.filter(my_user_id = user.id).first().udsMeta.all()
    else:
        context["allUdsMeta"] = allUdsMeta
    context["page_obj"] = page_obj
    context["user"] = user
    
    return render(request, "crud/index2.html",context=context)


def profile(request):
    context = {}
    user = request.user
    allUdsMeta = Bascet.objects.filter(my_user_id = user.id).first().udsMeta.all().order_by("-oid")
    if request.method == 'POST':
        if "create_order" in request.POST:
            doc = DocxTemplate("crud/source/blank.docx")
            cont = {'position':'netest', 'departament':'test', 'username':'test', 'task':'test'}
            doc.render(cont)
            doc.save("crud/source/final_blank.docx")
    context["count_elements_in_bascet"] = len(allUdsMeta)
    return render(request,"crud/profile.html", context= context)

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
    
    context["allUdsMeta"] = allUdsMeta
    context["page_obj"] = page_obj
    if request.method == 'POST':
        if "del" in request.POST:
            bascet = Bascet.objects.get(my_user_id = user.id)
            bascet.udsMeta.remove(UdsMeta.objects.get(oid = request.POST["oid"]))
    return render(request, "crud/bascet.html", context=context)


