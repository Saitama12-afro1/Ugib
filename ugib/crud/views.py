from pprint import pprint
from turtle import update

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist


from.models import UdsMeta, auto_incr_oid
from .forms import UdsMetaForm
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
    if request.method == 'POST':
       
        if 'update'  in request.POST:
            form_data = HelperUdsMet.create_dict_from_query_set_without_oid(request.POST)  
            try:
                print(form_data)
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
            form_data = HelperUdsMet.create_dict_from_query_set_without_oid(request.POST)
            # data = HelperUdsMet.create_Uds_Meta_dict(form_data, UdsMeta)
            print(form_data)
            UdsMeta.objects.create(**form_data)
            
            return redirect('/')
    allUdsMeta = UdsMeta.objects.all().order_by("-oid")
    
    
    paginator = Paginator(allUdsMeta,20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    a = UdsMeta.objects.all().order_by("oid").last()

    return render(request, "crud/index2.html",{"allUdsMeta":allUdsMeta,"page_obj":page_obj} )


def test(request):
    if request.method == 'POST':
        print(request.POST)
    
    return render(request,"crud/t.html")
    
    