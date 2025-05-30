from django.urls import path

from . import views

urlpatterns = [


    path('', views.store, name='store'),

    path('product/<slug:slug>', views.product_info, name='product-info'),

    path('search/<slug:slug>', views.list_category, name='list-category'),

    path('search/', views.search_products, name='search-results'),

    path('ajax-search/', views.ajax_search, name='ajax-search'),


]