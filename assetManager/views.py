from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.forms import SignUpForm, LogInForm
from assetManager.investments.stocks import StocksGetter
import json
from django.core.cache import cache
from dateutil.tz import tzlocal
import datetime
from django.http import JsonResponse
from assetManager.investments.reactstuff import NumberShow
from assetManager.transactionInsight.bank_graph_data import BankGraphData
#remove after testing purposes are finished
from assetManager.models import User
from assetManager.assets.debit_card import DebitCard
from django.contrib.auth.decorators import login_required

def home(request):
    plaid_wrapper = SandboxWrapper()
    public_token = plaid_wrapper.create_public_token()
    plaid_wrapper.exchange_public_token(public_token)
    accounts_informations = plaid_wrapper.get_accounts(plaid_wrapper.ACCESS_TOKEN)
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
                #setup method
                # home page for now CHANGE LATER
                return redirect('home_page')
        messages.add_message(request, messages.ERROR, 'The credentials provided are incorrect.')
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

# NOTE: this method is not needed - real one in api/views, leave for now for manual testing
def setup_asset_data(request):
    user = request.user
    wrapper = SandboxWrapper() # for now
    stock_getter = StocksGetter(wrapper)
    stock_getter.query_investments(user)
    cache.set('investments' + user.email, stock_getter.investments)

# add @login_required
def connect_investments(request):
    if request.method == 'GET':
        # here we will have arguments that denote what products the user has chosen
        products_chosen = ['transactions']
        # for now i've hardcoded them
        plaid_wrapper = DevelopmentWrapper()
        plaid_wrapper.create_link_token(products_chosen)
        link_token = plaid_wrapper.get_link_token()
        # attach products_chosen to session so they can be used in POST request
        request.session['products_chosen'] = products_chosen
        return render(request, 'connect_investments.html', {'link_token': link_token})
    else:
        plaid_wrapper = DevelopmentWrapper()
        #plaid_wrapper.products_requested = ['transactions']
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        public_token = body['public_token']

        plaid_wrapper.exchange_public_token(public_token)

        products_chosen = request.session.get('products_chosen', None)
        # if POST request recieved before GET
        if products_chosen is None:
            return redirect('connect_investments')
        plaid_wrapper.save_access_token(request.user, products_chosen)
        del request.session['products_chosen']
        return redirect('home_page')

def number_view(request):
    data = {'number': NumberShow.getNumber()}
    return HttpResponse(json.dumps(data), content_type='application/json')

def link_sandbox_investments(request):
    user = request.user
    wrapper = SandboxWrapper()
    public_token = wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments'])
    wrapper.exchange_public_token(public_token)
    wrapper.save_access_token(user, ['investments'])

