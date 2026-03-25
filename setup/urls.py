from django.contrib import admin
from django.urls import path
from core.views import produtos_view
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', produtos_view, name='produtos'), 
    path('shopee/', views.shopee_view, name='shopee'),
]