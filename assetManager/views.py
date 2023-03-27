from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.investments.stocks import StocksGetter
import json
from django.core.cache import cache
from dateutil.tz import tzlocal
import datetime
from django.http import JsonResponse
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

# NOTE: this method is not needed - real one in api/views, leave for now for manual testing
def setup_asset_data(request):
    user = request.user
    wrapper = SandboxWrapper() # for now
    stock_getter = StocksGetter(wrapper)
    stock_getter.query_investments(user)
    cache.set('investments' + user.email, stock_getter.investments)


def link_sandbox_investments(request):
    user = request.user
    wrapper = SandboxWrapper()
    public_token = wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments'])
    wrapper.exchange_public_token(public_token)
    wrapper.save_access_token(user, ['investments'])

