from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "filetransfer_home"),

    
    path('download/', views.download, name='download'),
    path('download/<str:root_name>/', views.download, name='download_root'),
    path('download/<str:root_name>/<path:subpath>/', views.download, name='download_browse'),
    path('toggle_selection/', views.toggle_selection, name='toggle_selection'),
    path('cart/', views.cart, name='cart'),
    path('download_zip/', views.download_zip, name='download_zip'),





    path("upload/", views.upload, name = "upload"),
    path('upload/<str:root_name>/', views.upload, name='upload_root'),
    path('upload/<str:root_name>/<path:subpath>/', views.upload, name='upload_browse'),

    
    
    
]