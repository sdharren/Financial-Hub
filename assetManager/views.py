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

def reformatJson(Json):
    new_json = []
    for item in Json:
        dic = {}
        dic[item['official_name']]=item['balances']['available']
        if(item['balances']['available']!=None):
            new_json.append(dic)
    return new_json


def link_sandbox_investments(request):
    user = request.user
    wrapper = SandboxWrapper()
    public_token = wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments'])
    wrapper.exchange_public_token(public_token)
    wrapper.save_access_token(user, ['investments'])

