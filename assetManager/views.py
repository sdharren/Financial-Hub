from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.forms import SignUpForm


def home(request):
    plaid_wrapper = SandboxWrapper()
    plaid_wrapper.create_public_token()
    plaid_wrapper.exchange_public_token(plaid_wrapper.create_public_token())
    accounts_informations = plaid_wrapper.get_accounts()
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

# add @login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_page')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

# add @login_required
def connect_investments(request):
    if request.method == 'GET':
        plaid_wrapper = DevelopmentWrapper()
        plaid_wrapper.create_link_token()
        link_token = plaid_wrapper.get_link_token()
        return render(request, 'connect_investments.html', {'link_token': link_token})
    else:
        plaid_wrapper = DevelopmentWrapper()
        public_token = request.POST['public_token']
        plaid_wrapper.exchange_public_token(public_token)
        print(plaid_wrapper.get_access_token())

