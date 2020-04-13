from django.urls import path

from . import views

urlpatterns = [
    path('upload/image/', views.upload_image),
    path('upload/get_qiniu_token', views.get_qiniu_token_view)
]
