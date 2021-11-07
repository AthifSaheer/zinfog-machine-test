from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.admin_login, name='login'),
    # path('register/', views.register, name="register"),
    path('logout/', views.admin_logout, name='logout'),
]
