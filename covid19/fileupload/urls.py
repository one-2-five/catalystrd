from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
#from . views import model_form_upload


urlpatterns = [
    path('', views.xray_list, name='xray_list'),
    path('upload/', views.model_form_upload, name='model_form_upload'),
    path('trainmodel/<int:id>/', views.trainmodel, name='trainmodel'),
    path('delete/<int:id>/', views.xray_delete, name='xray_delete'),
    path('update/<int:id>/', views.xray_update, name='xray_update'),

]