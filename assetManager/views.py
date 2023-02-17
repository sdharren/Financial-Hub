from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.forms import SignUpForm, LogInForm
from assetManager.investments.stocks import StocksGetter
import json

#from assetManager.bankcards.debit_card import DebitCard

def transaction_reports():
    plaid_wrapper = SandboxWrapper()
    debit_card = DebitCard(plaid_wrapper)
    debit_card.get_transactions()



def home(request):
    plaid_wrapper = SandboxWrapper()
    public_token = plaid_wrapper.create_public_token()
    plaid_wrapper.exchange_public_token(public_token)
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

# add @login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                # home page for now CHANGE LATER
                return redirect('home_page')
        messages.add_message(request, messages.ERROR, 'The credentials provided are incorrect.')
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

# add @login_required
def connect_investments(request):
    if request.method == 'GET':
        # here we will have arguments that denote what products the user has chosen
        products_chosen = ['investments']
        # for now i've hardcoded them
        plaid_wrapper = DevelopmentWrapper()
        plaid_wrapper.create_link_token(products_chosen)
        link_token = plaid_wrapper.get_link_token()
        return render(request, 'connect_investments.html', {'link_token': link_token})
    else:
        plaid_wrapper = DevelopmentWrapper()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        public_token = body['public_token']
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(request.user)
        return redirect('home_page')