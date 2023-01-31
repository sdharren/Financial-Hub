from django.shortcuts import render
<<<<<<< HEAD
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from django.http import HttpResponse


def home(request):
    accounts_informations = get_accounts()
    json_data = reformatJson(accounts_informations)
    return render(request,'home.html',{"json_data":json_data})

def reformatJson(Json):
    new_json = []
    for item in Json:
        dic = {}
        dic[item['official_name']]=item['balances']['available']
        if(item['balances']['available']!=None):
            new_json.append(dic)
    return new_json

def connect_investments(request):
    if request.method == 'GET':
        investments = Investments()
        link_token = investments.create_link_token()
        return render(request, 'connect_investments.html', {'link_token': link_token})
    else:
        investments = Investments()
        public_token = request.POST['public_token']
        print(investments.get_access_token(public_token))

