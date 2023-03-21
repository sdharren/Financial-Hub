from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('', views.getRoutes),
    path('firstname/', views.getFirstName),
    path('token/', MyTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('signup/', views.SignupView.as_view(), name = "signup"),
    path('investment_categories/', views.investment_categories, name='investment_categories'),
    path('investment_category_names/', views.investment_category_names),
    path('investment_category_breakdown/', views.investment_category_breakdown, name='investment_category_breakdown'),
    path('stock_history/', views.stock_history, name='stock_history'),
    path('supported_investments/', views.supported_investments),
    path('exchange_public_token/', views.exchange_public_token, name='exchange_public_token'),
    path('link_token/', views.link_token, name='link_token'),
    path('cache_assets/', views.cache_assets),
    path('sector_spending/', views.sector_spending, name='sector_spending'),
    path('company_spending/', views.company_spending, name='company_spending'),
    path('yearly_graphs/', views.yearlyGraph, name='yearlyGraph'),
    path('monthly_graphs/', views.monthlyGraph, name='monthlyGraph'),
    path('weekly_graphs/', views.weeklyGraph, name='weeklyGraph'),
    path('sandbox_investments/', views.sandbox_investments, name='sandbox_investments'),
    path('get_balances_data/', views.get_balances_data, name='get_balances_data'),
    path('select_account/', views.select_account, name='select_account'),
    path('select_bank_account/', views.select_bank_account, name='select_bank_account'),
    path('set_bank_access_token/', views.set_bank_access_token, name='set_bank_access_token'),
    path('currency_data/', views.get_currency_data, name='currency_data'),
    path('recent_transactions/', views.recent_transactions, name='recent_transactions'),
]
