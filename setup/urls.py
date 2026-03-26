from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import produtos_view
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'), 
    path('produtos/', views.produtos_view, name='produtos'),
    path('shopee/', views.shopee_view, name='shopee'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]