from django.urls import path, include
from . import views

# dob select before currend day
# password 8 char, symbols

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name='logout'),

    path('update/personal/details/', views.update_personal_details, name='update_personal_details'),
    path('profile/<int:id>/', views.profile, name='profile'),
    # path('upload_image/', views.upload_image, name='upload_image'),
]
