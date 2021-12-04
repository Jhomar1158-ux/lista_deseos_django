from django.urls import path
from app1 import views

urlpatterns=[
    path('', views.index),
    path('registro', views.registro),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('item/new', views.addNewItem),
    path('item/create', views.createItem),
    path('item/<int:id>/', views.itemDetails),
    path('item/<int:id>/quit', views.quitItem),
    path('item/<int:id>/destroy', views.deleteItem)
]