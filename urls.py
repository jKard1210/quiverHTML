from django.urls import path
from . import views


app_name = "altData"

urlpatterns = [
	path('', views.index,name="index"),
	path("logout/", views.logout_request, name="logout"),
	path('dashboard/',views.dashboard, name='dashboard'),
	path('login/', views.login_request, name="login"),
	path('register/', views.register_user, name="register"),
	path('dashboard/<ticker>/', views.ticker_view, name="tickerView")
]
