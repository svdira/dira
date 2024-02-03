from django.shortcuts import render, redirect
from django import template
from .models import *
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q
import os
import datetime
import shutil


def prueba(request):
	return render(request,'base0.html',{})

def addPetal(request):
	if request.method == 'POST':

		for img in request.FILES.getlist("imagen"):
			newP = Petal.objects.create(imagen=img,ptags=request.POST.get("ptags"))
			newP.save()

			ltags = request.POST.get("ptags","").split(",")

			for t in ltags:
				bt = Tags.objects.create(petal=newP,tag=t)
				bt.save()

		return render(request,'add-petal.html',{})
	else:
		return render(request,'add-petal.html',{})

def randPetal(request):
	pks = Petal.objects.all().values_list('pk', flat=True)
	random_pk = choice(pks)
	random_obj = Petal.objects.get(pk=random_pk)

	ptags = Tags.objects.exclude(tag='base').filter(petal__id=random_obj.id)

	taglist = Tags.objects.exclude(tag='base').values('tag').annotate(qitems = Count('tag')).order_by('-qitems')

	emb_img = "<img src='{}' style='width:100%; border:1px solid grey; float:left;'>".format(random_obj.imagen.url)


	return render(request,'random.html',{'rpic':random_obj,'nowtags':ptags,'ntags':taglist,'emb':emb_img})

def tag(request,t,p):
	ntag = Tags.objects.filter(tag=t).count()
	pics = Tags.objects.filter(tag=t)[int(p)]

	if int(p) == (ntag-1):
		next_p = 0
	else:
		next_p = int(p)+1

	tag = t

	ptags = Tags.objects.filter(petal__id=pics.petal.id)

	taglist = Tags.objects.values('tag').annotate(qitems = Count('tag')).order_by('-qitems')

	emb_img = "<img src='{}' style='width:100%; border:1px solid grey; float:left;'>".format(pics.petal.imagen.url)
	return render(request,'tag.html',{'rpic':pics,'nowtags':ptags,'ntags':taglist,'tag':tag,'next_p':next_p,'emb':emb_img})

def addnewtag(request):
	if request.method == 'POST':

		pid = request.POST.get("picid","0")

		pic = Petal.objects.get(pk=int(pid))

		ltags = request.POST.get("ptags","").split(",")

		for t in ltags:
			bt = Tags.objects.create(petal=pic,tag=t)
			bt.save()


	return redirect('/garden/')



def fjImport(request,img):
	import random
	r = []
	fdir ='D:/django/svdira/media/jk'
	for root, dirs, files in os.walk(fdir):
		for name in files:
			filepath = root + os.sep + name
			if filepath.endswith(".jpg") or filepath.endswith(".png"):
				r.append(os.path.join(root, name))

	ppics = len(r)
	if int(img)==0:
		img = random.randint(0, ppics-1)
	netx = random.randint(0, ppics-1)

	original_path = r[int(img)].replace("/","\\")

	fpath = "/media/" + r[int(img)].replace("D:/django/svdira/media/","").replace("\\","/")
	return render(request,'imgImport.html',{'imgs':fpath,'nextp':netx,'og':original_path})

def deleteImg(request):
	if request.method=="POST":
		oldPath = request.POST.get("fileRemove")

		newPath = "D:/django/svdira/media/descartes/{}.jpg".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

		os.rename(oldPath, newPath)

	return redirect("/garden/imgImport/0")

def saveImg(request):
	if request.method=="POST":
		oldPath = request.POST.get("oldPath")

		newPath = "D:/django/svdira/media/flowers/{}.jpg".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

		os.rename(oldPath, newPath)

	return redirect("/garden/imgImport/0")

def movePetal(request):
	import random
	r = []
	folder = 'D:/django/svdira/media/selected'
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

	fdir ='D:/django/svdira/media/selection'
	ddir ='D:/django/svdira/media/selected'
	for root, dirs, files in os.walk(fdir):
		for name in files:
			filepath = root + os.sep + name
			if filepath.endswith(".jpg") or filepath.endswith(".png"):
				r.append(os.path.join(name))
	ppics = len(r)
	img = random.randint(0, ppics-1)
	original_path = fdir+'/'+r[int(img)]
	final_path = ddir+'/'+r[int(img)]

	shutil.move(original_path, final_path)



	return redirect('/garden/add-petal')

def startNoteConsumo(request):
	obj_nota = Notas.objects.get(pk=request.POST.get("nota_id"))

	NoteMedia.objects.create()
