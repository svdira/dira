from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
	path('prueba/', views.prueba, name='prueba'),
	path('add-petal/', views.addPetal, name='addpetal'),
	path('tag/<t>/<p>', views.tag, name='tag'),
	path('', views.randPetal, name='randpetal'),
	path('addnewtag', views.addnewtag, name='addnewtag'),
	path('imgImport/<img>', views.fjImport, name='imgImport'),
	path('removeFile/', views.deleteImg, name='removeFile'),
	path('saveImg/', views.saveImg, name='saveImg'),	
	path('movePetal/', views.movePetal, name='moveImg'),	
	]