from django.db.models import Count
from django.db.models import F
from .models import *

def catlist(request):
	catlist = Item.objects.values('item_cat__nombre','item_cat__id').annotate(qitems = Count('item_cat')).order_by('item_cat__id')
	return {'catlist':catlist}

def nowr(request):
	nowr = Consumo.objects.filter(fecha_fin__isnull=True).order_by('con_itm__item_cat__id','-fecha_inicio')
	return {'nowr':nowr}

def autores(request):
	lautores = RelItemPersona.objects.filter(credit='author',item__item_cat__id=1).values('persona__nombre','persona__id').annotate(qlibros = Count('persona__nombre')).order_by('-qlibros','persona__nombre')
	return {'autores':lautores}

def item_tags(request):
	from django.db.models.functions import Length
	item_tags = ItemTag.objects.values('tag').annotate(qitems = Count('tag')).annotate(text_len=Length('tag')).filter(text_len__gt=4).order_by('-qitems','tag')[0:50]


	return {'item_tags':item_tags}
