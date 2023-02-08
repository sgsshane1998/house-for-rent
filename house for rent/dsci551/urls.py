from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name = 'homepage'),
    path('search/', views.search, name = 'search'),
    path('detail/<int:IDs>', views.detail, name = 'detail')
]
