from django.shortcuts import render
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper


def connect_investments(request):
    if request.method == 'GET':
        investments = Investments()
        link_token = investments.create_link_token()
        return render(request, 'connect_investments.html', {'link_token': link_token})
    else:
        investments = Investments()
        public_token = request.POST['public_token']
        print(investments.get_access_token(public_token))

