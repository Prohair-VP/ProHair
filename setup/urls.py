from django.contrib import admin
from django.urls import path
from core.views import produtos_view # <-- Atualizamos o import para a nossa nova função!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', produtos_view, name='produtos'), 
]