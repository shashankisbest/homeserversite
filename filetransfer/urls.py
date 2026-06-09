from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "filetransfer_home"),
    path("upload/", views.upload, name = "filetransfer_upload"),
    path('download/', views.download, name='download'),
    path('download/<str:root_name>/', views.download, name='download_root'),
    path('download/<str:root_name>/<path:subpath>/', views.download, name='download_browse'),
    path('toggle_selection/', views.toggle_selection, name='toggle_selection'),
    path('cart/', views.cart, name='cart'),
    
    
    
]