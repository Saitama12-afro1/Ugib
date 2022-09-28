from pprint import pprint
from turtle import update
import csv


from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User

from.models import UdsMeta
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
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(HelperUdsMet._all_columns)
                wr.writerow(list(form_data.values()))
                
            with open('stockitems_misuper.csv', encoding="cp1251") as myfile:
                response = HttpResponse(myfile, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=stockitems_misuper.csv'
                return response
        elif 'login'  in request.POST:
            # current_page = request.GET.get('page')
            user = authenticate(username = request.POST["mail"], password = request.POST["password"])
            
            if user is not None:
                login(request, user)
                return redirect("/")
            # return redirect(f'/?page={current_page}')
    
    context["allUdsMeta"] = allUdsMeta
    context["page_obj"] = page_obj
    context["user"] = user
    return render(request, "crud/index2.html",context=context)


def profile(request):
    if request.method == 'POST':
        pass
    return render(request,"crud/profile.html")

def logout(request):
    django_logout(request)
    return redirect("/")
    