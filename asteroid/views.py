from django.shortcuts import render, redirect
from django import template
from .models import *
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q, Max
from django.db.models import FloatField
from django.db.models import F
from django.db.models.functions import Round
from django.db.models.functions import Cast
import math

def plantilla(request):

    return render(request,'base.html',{})

def homepage(request):
    import math
    from datetime import datetime
    fec_hoy = datetime.today().strftime('%Y-%m-%d')
    nlist = 15
    npics = Item.objects.filter(item_cat__id__in=[7,8,9]).count()
    npages = math.ceil(npics/nlist)

    matches = Partido.objects.filter(terminado=False,fecha__lte=fec_hoy).order_by('-fecha')[0:2]

    articles = Item.objects.filter(item_cat__id__in=[7,8,9]).order_by('-fecha','-id')[0:nlist]
    listas = Coleccion.objects.all().exclude(nombre__contains='Magazine').order_by('-cfecha')
    return render(request,'homepage.html',{'articles':articles,'listas':listas,'npages':range(npages),'partidos':matches})

def search(request):
    keyword = request.POST.get("kw","")
    if keyword == "":
        keyword = "kafbdajfbakdjaf"

    articles = Item.objects.filter(Q(titulo__contains=keyword) | Q(contenido__contains=keyword)).order_by('item_cat__id')
    return render(request,'search.html',{'articles':articles})



def archive(request,p):
    import math

    nlist = 15
    npics = Item.objects.filter(item_cat__id__in=[7,8,9]).count()
    npages = math.ceil(npics/nlist)

    li = int(p)*nlist
    ls = (1+int(p))*nlist

    articles = Item.objects.filter(item_cat__id__in=[7,8,9]).order_by('-id')[li:ls]
    return render(request,'archive.html',{'articles':articles,'npages':range(npages),'page':int(p)})

def category(request,cat,p):
    import math

    if int(cat) in [1,2,3,4,5,14,15,17,18,19,21,22]:
        nlist = 25
        npics = Consumo.objects.filter(con_itm__item_cat__id=int(cat),fecha_fin__isnull=False).count()
        npages = math.ceil(npics/nlist)
        li = int(p)*nlist
        ls = (1+int(p))*nlist
        articles = Consumo.objects.filter(con_itm__item_cat__id=int(cat),fecha_fin__isnull=False).order_by('-fecha_fin','-id')[li:ls]
    else:
        nlist = 12
        npics = Item.objects.filter(item_cat__id=int(cat)).count()
        npages = math.ceil(npics/nlist)
        li = int(p)*nlist
        ls = (1+int(p))*nlist
        articles = Item.objects.filter(item_cat__id=int(cat)).order_by('-fecha','-id')[li:ls]


    ocat = Categoria.objects.get(pk=int(cat))

    cortes = Consumo.objects.filter(con_itm__item_cat__id=int(cat),fecha_fin__isnull=False).values('fecha_fin__year').annotate(qitems=Count('id')).order_by('-fecha_fin__year')

    return render(request,'category.html',{'articles':articles,'npages':range(npages),'page':int(p),'cat':cat,'ocat':ocat,'nitms':npics,'cortes':cortes})


def catqueue(request,cat,p):
    import math

    if int(cat) in [1,2,3,4,5,14,15,17,18,19,21,22]:
        nlist = 12
        npics = Item.objects.filter(item_cat__id=int(cat),consumo__con_itm__isnull=True).count()
        npages = math.ceil(npics/nlist)
        li = int(p)*nlist
        ls = (1+int(p))*nlist
        articles = sorted(Item.objects.filter(item_cat__id=int(cat),consumo__con_itm__isnull=True).order_by('titulo'), key=lambda t: t.pubyear)[li:ls]
    else:
        nlist = 12
        npics = Item.objects.filter(item_cat__id=int(cat)).count()
        npages = math.ceil(npics/nlist)
        li = int(p)*nlist
        ls = (1+int(p))*nlist
        articles = Item.objects.filter(item_cat__id=int(cat)).order_by('-fecha')[li:ls]


    ocat = Categoria.objects.get(pk=int(cat))


    return render(request,'catqueue.html',{'articles':articles,'npages':range(npages),'page':int(p),'cat':cat,'ocat':ocat,'nitms':npics})



def additem(request):
    cats = Categoria.objects.all()
    if request.method=='POST':
        cat_id = request.POST.get("categoria")
        objCategoria = Categoria.objects.get(pk=int(cat_id))
        post_titulo = request.POST.get("titulo")
        post_contenido = request.POST.get("contenido")
        hoy = datetime.now()
        post_fecha = request.POST.get("fecha")

        newItem = Item.objects.create(item_cat=objCategoria,titulo=post_titulo,contenido=post_contenido,fecha=post_fecha)
        newItem.save()


        if request.POST.get("itmtags",""):
            ltags = request.POST.get("itmtags","").split(",")
            if ltags[0].strip()=='book':
                new_itt = ItemTable.objects.create(tbl_itm=newItem,campo='pub year',datos=ltags[2].strip())
                new_itt.save()
                thisPersona = Persona.objects.get(pk=int(ltags[1].strip()))
                new_rel = RelItemPersona.objects.create(item=newItem, persona=thisPersona,credit='author')
                new_rel.save()
                contador = 1
                for t in ltags:
                    if contador > 3:
                        bt = ItemTag.objects.create(item_t=newItem,tag=t.strip())
                        bt.save()
                    contador = contador + 1
            elif ltags[0].strip()=='movie':
                new_itt = ItemTable.objects.create(tbl_itm=newItem,campo='pub year',datos=ltags[1].strip())
                new_itt.save()
            else:
                for t in ltags:
                    bt = ItemTag.objects.create(item_t=newItem,tag=t.strip())
                    bt.save()


        if request.FILES.get("cover"):

            newMedia = WikiMedia.objects.create(med_itm = newItem,imgtype=1,imagen=request.FILES.get("cover"),mtags='cover')
            newMedia.save()

        if newItem.item_cat.id == 16:
            return redirect('/wiki/'+str(newItem.id))
        else:
            return redirect('/item/'+str(newItem.id))
    else:
        return render(request,'add-item.html',{'cats':cats})


def addJournalEntry(request):
    if request.method == 'POST':
        objCategoria = Categoria.objects.get(pk=7)
        post_contenido = request.POST.get("contenido")
        post_fecha = request.POST.get("fecha")
        fecha_titulo =  datetime.strptime(post_fecha, '%Y-%m-%d').strftime('%b %-d, %Y')

        newItem = Item.objects.create(item_cat=objCategoria,titulo=fecha_titulo,contenido=post_contenido,fecha=post_fecha)
        newItem.save()
        return redirect('/item/'+str(newItem.id))
    else:
        return render(request,'add-journey-entry.html',{})

def item(request,iid):
    thisItem = Item.objects.get(pk=iid)
    ncon = Consumo.objects.filter(con_itm__id=iid,fecha_fin__isnull=True).count()
    notas = Notes.objects.filter(item_note__id=int(iid))

    if ncon > 0:
        consumo = Consumo.objects.filter(con_itm__id=iid,fecha_fin__isnull=True).latest('id')
    else:
        consumo = None

    tabla = ItemTable.objects.filter(tbl_itm__id=iid).order_by('campo')
    listas = ColItem.objects.filter(itm__id=iid)
    consumos = Consumo.objects.filter(con_itm__id=iid,fecha_fin__isnull=False)
    itags = ItemTag.objects.filter(item_t=iid)[0:12]

    creditos = RelItemPersona.objects.filter(item__id = thisItem.id)

    personas_id = []

    for c in creditos:
        personas_id.append(c.persona.id)

    creditos_it = RelItemPersona.objects.filter(persona__id__in = personas_id).values('item__id').annotate(qitems = Count('item_id'))

    items_id = []

    for i in creditos_it:
        items_id.append(i["item__id"])

    more_creditos = sorted(Item.objects.filter(id__in = items_id).exclude(id=thisItem.id), key=lambda t: t.pubyear)



    for i in itags:
        i.tag = i.tag.strip()

    if request.method=='POST':
        fecha = request.POST.get("fecha_fin")
        Consumo.objects.filter(con_itm__id=iid,fecha_fin__isnull=True).update(fecha_fin=fecha)
        consumo = None
        return render(request,'item.html',{'thisItem':thisItem,'consumo':consumo,'consumos':consumos,'tabla':tabla,'listas':listas,'itags':itags,'notas':notas,'creditos':creditos,'more_creditos':more_creditos})
    else:
        return render(request,'item.html',{'thisItem':thisItem,'consumo':consumo,'consumos':consumos,'tabla':tabla,'listas':listas,'itags':itags,'notas':notas,'creditos':creditos,'more_creditos':more_creditos,'items_id':items_id})

def edititem(request,iid):
    thisItem = Item.objects.get(pk=iid)
    cats = Categoria.objects.all()
    rel_media = WikiMedia.objects.filter(med_itm__id=int(iid))

    if request.method=='POST':
        cat_id = request.POST.get("categoria")
        objCategoria = Categoria.objects.get(pk=int(cat_id))
        post_titulo = request.POST.get("titulo")
        post_contenido = request.POST.get("contenido")

        Item.objects.filter(id=iid).update(item_cat=objCategoria,titulo=post_titulo,contenido=post_contenido)

        if request.POST.get("itmtags",""):
            ltags = request.POST.get("itmtags","").split(",")
            if ltags !='':
                for t in ltags:
                    bt = ItemTag.objects.create(item_t=thisItem,tag=t.strip())
                    bt.save()


        return redirect('/item/'+str(iid))
    else:
        return render(request,'edit-item.html',{'thisItem':thisItem,'cats':cats,'rel_media':rel_media})

def startitem(request,iid):
    thisItem = Item.objects.get(pk=iid)

    if thisItem.item_cat.id in [1,17,18,21,22]:
        units = 'pages'
    elif thisItem.item_cat.id == 2:
        units = 'minutes'
    elif thisItem.item_cat.id in [3,5,19]:
        units = 'episodes'
    else:
        units = 'check please'

    if request.method == 'POST':
        if thisItem.item_cat.id == 2:
            newC = Consumo.objects.create(con_itm=thisItem,unidades=request.POST.get("unidades"),cantidad=request.POST.get("cantidad"),fecha_inicio=request.POST.get("fecha_inicio"),fecha_fin=request.POST.get("fecha_inicio"),season=int(request.POST.get("season")), formato=request.POST.get("formato"), lan=request.POST.get("lan"), mutiplicador=int(request.POST.get("multiplicador")))
        else:
            newC = Consumo.objects.create(con_itm=thisItem,unidades=request.POST.get("unidades"),cantidad=request.POST.get("cantidad"),fecha_inicio=request.POST.get("fecha_inicio"),season=int(request.POST.get("season")), formato=request.POST.get("formato"), lan=request.POST.get("lan"), mutiplicador=int(request.POST.get("multiplicador")))
        newC.save()
        return redirect('/item/'+str(iid))
    else:
        return render(request,'start-item.html',{'thisItem':thisItem,'units':units})


def tableitem(request,iid):
    thisItem = Item.objects.get(pk=iid)

    if request.method == 'POST':
        lineas = request.POST.get("datalines","").split(";")

        for l in lineas:
            campos = l.split(":")
            newC = ItemTable.objects.create(tbl_itm=thisItem,campo=campos[0].strip(),datos=campos[1].strip())
            newC.save()
        return redirect('/item/'+str(iid))
    else:

        return render(request,'table-item.html',{'thisItem':thisItem})

def addMedia(request,iid):
    thisItem = Item.objects.get(pk=iid)
    if request.method == 'POST':
        ix = request.FILES.get("imagen")
        newWM = WikiMedia.objects.create(med_itm=thisItem,imagen=ix,imgtype=request.POST.get("imgtype"),mtags=request.POST.get("mtags"))
        newWM.save()
        return redirect('/item/'+str(iid))
    else:
        return render(request,'add-media.html',{'thisItem':thisItem})

def finance(request):
    cuentas = Cuenta.objects.all().order_by('nombre')
    tiposT = TrxTyp.objects.all().order_by('desc')

    transacciones = Trx.objects.all().order_by('-fecha','-id')
    saldos = Trx.objects.raw("select * from c_balance order by cid")

    cortes = Trx.objects.values('fecha__year','fecha__month').annotate(qitems = Count('id')).order_by('-fecha__year','-fecha__month')

    acc_saldo = 0
    for s in saldos:
        acc_saldo = acc_saldo + s.balance_final

    return render(request,'finance2.html',{'cuentas':cuentas,'tiposT':tiposT,'trxs':transacciones,'saldos':saldos,'fbal':acc_saldo,'cortes':cortes})


def saveTrx(request):

    if request.method == "POST":
        ttrx = request.POST.get("tipotrx")
        cuenta = request.POST.get("cuenta")
        monto = request.POST.get("monto")
        fecha = request.POST.get("fecha")
        desc = request.POST.get("detalle")

        c = Cuenta.objects.get(pk=cuenta)
        t = TrxTyp.objects.get(pk=ttrx)

        nt = Trx.objects.create(fecha = fecha, debito = c, credito=t, monto = monto,desc=desc)


        nt.save()

        return redirect('/finance/')
    else:
        return redirect('/finance/')

def savePmt(request):

    if request.method == "POST":
        origen = request.POST.get("origen")
        destino = request.POST.get("destino")
        monto = request.POST.get("monto")
        fecha = request.POST.get("fecha")
        desc = request.POST.get("detalle")

        o = Cuenta.objects.get(pk=origen)
        d = Cuenta.objects.get(pk=destino)

        i = TrxTyp.objects.get(pk=17)
        t = TrxTyp.objects.get(pk=15)

        nt = Trx.objects.create(fecha = fecha, debito = o, credito=t, monto = monto,desc=desc)
        nt.save()

        nt2 = Trx.objects.create(fecha = fecha, debito = d, credito=i, monto = monto,desc=desc)
        nt2.save()

        return redirect('/finance/')
    else:
        return redirect('/finance/')

def addColeccion(request):
    if request.method == 'POST':
        newC = Coleccion.objects.create(nombre=request.POST.get("nombre"),info=request.POST.get("info"),cfecha=request.POST.get("cfecha"))
        newC.save()
        return redirect('/coleccion/{}'.format(newC.id))
    else:
        return render(request,'add-list.html',{})

def coleccion(request,id):
    col = Coleccion.objects.get(pk=id)
    colitms = ColItem.objects.filter(col__id=id).order_by('id')
    listas = Coleccion.objects.all().order_by('-id')

    nb = 0
    rb = 0

    for c in colitms:
        nb = nb+1
        if datetime.strptime(c.itm.lastr,"%Y-%m-%d").date() > col.cfecha:
            rb = rb + 1

    if nb == 0:
        por_r=0
    else:
        por_r = round(100*rb/nb,1)

    if request.method == 'POST':
        kw = request.POST.get("keyw","dfbafiaorbeabga")
        articles = Item.objects.filter(Q(titulo__contains=kw) | Q(contenido__contains=kw)).order_by('item_cat__id')
        return render(request,'list.html',{'col':col,'sr':articles,'ci':colitms,'listas':listas})
    else:
        return redirect('/cocovers/{}/a'.format(col.id))

def cocovers(request,id,s):
    col = Coleccion.objects.get(pk=id)
    if s == "d":
        colitms = ColItem.objects.filter(col__id=id).order_by('-id')
    elif s=="b":
        colitms =sorted(ColItem.objects.filter(col__id=id),key=lambda t: t.itm.pubyear)
    else:
        colitms = sorted(ColItem.objects.filter(col__id=id).order_by('id'), key=lambda t:t.itm.lastr)

    listas = Coleccion.objects.all().order_by('-cfecha')

    nb = 0
    rb = 0

    for c in colitms:
        nb = nb+1
        if datetime.strptime(c.itm.lastr,"%Y-%m-%d").date() > col.cfecha:
            rb = rb + 1

    if nb == 0:
        por_r=0
    else:
        por_r = round(100*rb/nb,1)

    if request.method == 'POST':
        kw = request.POST.get("keyw","dfbafiaorbeabga")
        articles = Item.objects.filter(Q(titulo__contains=kw) | Q(contenido__contains=kw)).order_by('item_cat__id')
        return render(request,'cocovers.html',{'col':col,'sr':articles,'ci':colitms,'listas':listas,'rb':rb,'nb':nb,'por_r':por_r})
    else:
        return render(request,'cocovers.html',{'col':col,'ci':colitms,'listas':listas,'rb':rb,'nb':nb,'por_r':por_r})

def additmcol(request,it,co):
    col = Coleccion.objects.get(pk=co)
    itm = Item.objects.get(pk=it)

    newCI = ColItem.objects.create(itm=itm,col=col)
    newCI.save()
    return redirect('/cocovers/'+str(col.id)+'/d')


def autor(request,au):


    books = sorted(ItemTable.objects.filter(campo='author',datos=au), key=lambda t: t.tbl_itm.pubyear)

    nb=0
    rb=0

    for b in books:
        nb = nb + 1
        if b.tbl_itm.ncon > 0:
            rb = rb + 1

    por_r = round(100*rb/nb,1)

    return render(request,'authors.html',{'books':books,'au':au,'rb':rb,'nb':nb,'por_r':por_r})


def viewmonth(request,y,m):
    trx = Trx.objects.filter(fecha__year=y,fecha__month=m, credito__codigo=1).order_by('-fecha','-id')
    categories = TrxTyp.objects.all().order_by('desc')
    budexec = Trx.objects.raw("""select
                                    *,
                                    case when mbudget==0 then actual else actual-mbudget end bvar,
                                    case when mbudget==0 then 100 else 100*(actual-mbudget)/mbudget end pvar

                            from
                                fin_control
                            where
                                mes={} and anho={} and (mbudget>0 or actual>0)
                            order by mbudget desc""".format(m,y))
    tot_act = 0
    tot_bud = 0
    for t in budexec:
        tot_act = tot_act+t.actual
        tot_bud = tot_bud+t.mbudget

    if tot_bud == 0:
        perf = 0
    else:
        perf = 100.0*tot_act/tot_bud

    if perf <= 95.0:
        colp = "green"
    elif perf <= 101.5:
        colp = "orange"
    else:
        colp = "red"

    cortes = Trx.objects.values('fecha__year','fecha__month').annotate(qitems = Count('id')).order_by('-fecha__year','-fecha__month')

    return render(request,'view-month.html',{'trxs':trx,'be':budexec,'anho':y,'mes':m,'actual':tot_act, 'budget':tot_bud,'perf':perf,'colp':colp,'cortes':cortes,'categ':categories})

def quemar(request,itm):
    thisItem = Item.objects.get(pk=itm)
    newC = Consumo.objects.create(con_itm=thisItem,unidades="quemado",cantidad=0,fecha_inicio="2023-12-31",fecha_fin="2023-12-31")
    newC.save()

    return redirect('/item/{}'.format(itm))


def editTable(request,tid):
    itt = ItemTable.objects.get(pk=int(tid))

    if request.method == 'POST':
        itt.campo = request.POST.get("campo",itt.campo)
        itt.datos = request.POST.get("datos",itt.datos)

        itt.save()

        return redirect('/item/{}'.format(itt.tbl_itm.id))
    else:
        return render(request,'edit-itt.html',{'itt':itt})

def yearHist(request,y,c):
    yearConsumos = Consumo.objects.filter(con_itm__item_cat__id=int(c),fecha_fin__year=int(y)).order_by('fecha_fin','id')
    categoria = Categoria.objects.get(pk=int(c))
    ncons = yearConsumos.count()

    cortes = Consumo.objects.filter(con_itm__item_cat__id=int(c),fecha_fin__isnull=False).values('fecha_fin__year').annotate(qitems=Count('id')).order_by('-fecha_fin__year')


    return render(request,'year-hist.html',{'consumos':yearConsumos,'anho':int(y),'categoria':categoria,'ncons':ncons,'cortes':cortes,'cat':int(c)})

def addIttMedia(request):
    itt_id = request.POST.get("itt_id")
    itt = ItemTable.objects.get(pk=int(itt_id))

    ix = request.FILES.get("imagen")
    newWM = ItemTableMedia.objects.create(itm_tbl=itt,imagen=ix,imgtype=1,mtags=request.POST.get("mtags"))
    newWM.save()
    return redirect('/item/'+str(itt.tbl_itm.id))


def forKindle(request,col_id):

    col = Coleccion.objects.get(pk=col_id)
    colitms = ColItem.objects.filter(col__id=col_id).order_by('id')

    return render(request,'printable.html',{'col':col,'colitms':colitms})



def viewtag(request,t):
    nowtag=t
    alltags = ItemTag.objects.filter(tag=nowtag)
    return render(request,'itag.html',{'alltags':alltags,'nowtag':nowtag})



def addNotes(request,item_id):
    itmN = Item.objects.get(pk=int(item_id))
    if request.method == 'POST':
        newN = Notes.objects.create(item_note=itmN,titulo=request.POST.get("titulo"),texto=request.POST.get("texto"))
        return redirect('/item/{}'.format(int(item_id)))
    else:
        return render(request,'add-notes.html',{'thisItem':itmN,'item_id':item_id})

def editNotes(request,note_id):
    nota = Notes.objects.get(pk=int(note_id))
    if request.method == 'POST':
        Notes.objects.filter(id=int(note_id)).update(titulo=request.POST.get("titulo"),texto=request.POST.get("texto"))

        return redirect('/item/{}'.format(int(nota.item_note.id)))
    else:
        return render(request,'edit-notes.html',{'nota':nota,'note_id':note_id})

def addBudgetReg(request):
    input_anho = int(request.POST.get('y'))
    input_mes = int(request.POST.get('m'))
    input_mbudget = float(request.POST.get('mbudget'))
    input_cuenta = TrxTyp.objects.get(pk=int(request.POST.get("cuenta")))
    Budget.objects.create(cuenta=input_cuenta,anho=input_anho,mes=input_mes,mbudget=input_mbudget)
    return redirect('/view-month/{}/{}'.format(input_anho,input_mes))

def finance2(request):
    cuentas = Cuenta.objects.all().order_by('nombre')
    tiposT = TrxTyp.objects.all().order_by('desc')

    transacciones = Trx.objects.all().order_by('-fecha','-id')
    saldos = Trx.objects.raw("select * from c_balance order by cid")

    cortes = Trx.objects.values('fecha__year','fecha__month').annotate(qitems = Count('id')).order_by('-fecha__year','-fecha__month')

    acc_saldo = 0
    for s in saldos:
        acc_saldo = acc_saldo + s.balance_final

    return render(request,'finance.html',{'cuentas':cuentas,'tiposT':tiposT,'trxs':transacciones,'saldos':saldos,'fbal':acc_saldo,'cortes':cortes})


def plantilla2(request):
    ptitle = "Home"

    grupos = Grupo.objects.all().order_by('titulo')

    if request.method == 'POST':

        if request.POST.get("search_term","")=="":
            results = None
        else:
            keyword = request.POST.get("search_term","")
            results = Persona.objects.filter(Q(nombre__contains=keyword) | Q(biographics__contains=keyword)).order_by('id')
            return render(request,'menu.html',{'ptitle':ptitle,'grupos':grupos,'results':results})
    else:
        return render(request,'menu.html',{'ptitle':ptitle,'grupos':grupos,'results':None})

def addPersona(request):
    ptitle = "Add Persona"
    grupos = Grupo.objects.all().order_by('titulo')

    if request.method=="POST":
        newP = Persona.objects.create(nombre=request.POST.get("nombre"),biographics=request.POST.get("bio"), tipo =request.POST.get("tipo"))
        newP.save()

        if request.FILES.get("ppic"):
            PersonaMedia.objects.create(persona = newP, imgtype=1,imagen=request.FILES.get("ppic"))

        if request.POST.get("grupo") != '0':
            thisG = Grupo.objects.get(pk=int(request.POST.get("grupo")))

            newR = RelGrupoPersona.objects.create(grupo=thisG,persona=newP)
            newR.save()

        return redirect('/view-persona/{}'.format(newP.id))

    else:
        return render(request,'add-persona.html',{'ptitle':ptitle,'grupos':grupos})

def viewPersonas(request,t,p):

    nlist = 20
    npics = Persona.objects.filter(tipo=t).count()
    npages = math.ceil(npics/nlist)
    li = int(p)*nlist
    ls = (1+int(p))*nlist
    articles = Persona.objects.filter(tipo=t).order_by('nombre')[li:ls]

    ptitle = "View Personas"
    return render(request,'view-ppl.html',{'ptitle':ptitle,'ppl':articles,'npages': range(npages),'thispage':int(p), 'cat':t})


def viewPersona(request,p):
    thisPerson = Persona.objects.get(pk=int(p))
    n_datos = PersonaDT.objects.filter(persona__id=int(p)).count()

    if n_datos > 0:
        datos = PersonaDT.objects.filter(persona__id=int(p))[0]
        html_t = "<table id='customers'><tr><th colspan='2' style='text-align:center;'>"+thisPerson.nombre+"</th></tr>"

        dtD = datos.strDT.split(";")

        for r in dtD:
            html_t = html_t+"<tr>"
            vals = r.split(":")
            for v in vals:
                html_t = html_t+"<td>"+v.strip()+"</td>"
            html_t = html_t+"</tr>"

        html_t = html_t    + "</table>"
    else:
        html_t    = None


    nowItems = sorted(RelItemPersona.objects.filter(persona__id=thisPerson.id),  key=lambda t: t.item.pubyear)
    n_items = RelItemPersona.objects.filter(persona__id=thisPerson.id).count()
    conteo_r = 0

    for n in nowItems:
        if n.item.ncon > 0:
            conteo_r = conteo_r + 1


    ptitle = thisPerson.nombre
    return render(request,'view-persona2.html',{'ptitle':ptitle,'ppl':thisPerson,'nowItems':nowItems,'dt':html_t,'conteo_r':conteo_r,'n_items':n_items    })

def editPersona(request,p):
    thisPerson = Persona.objects.get(pk=int(p))
    nd = datos = PersonaDT.objects.filter(persona__id=int(p)).count()
    if nd > 0:
        datos = PersonaDT.objects.filter(persona__id=int(p))[0]
    else:
        datos = None

    if request.method == 'POST':
        Persona.objects.filter(id=int(p)).update(nombre=request.POST.get("nombre"),biographics=request.POST.get("bio"), last_update=datetime.now())
        return redirect('/view-persona/{}'.format(p))

    else:
        ptitle = 'Edit: '+thisPerson.nombre
        return render(request,'edit-persona.html',{'ptitle':ptitle,'ppl':thisPerson,'datos':datos})

def addPersonaMedia(request):
    thisP = Persona.objects.get(pk=int(request.POST.get("p")))

    for img in request.FILES.getlist("imagen"):
        newP = PersonaMedia.objects.create(persona=thisP,imgtype=request.POST.get("imgtype"),imagen=img)
        newP.save()

    return redirect('/view-persona/{}'.format(thisP.id))

def viewPersonaGallery(request,p,n):
    conteo = PersonaMedia.objects.filter(persona__id=int(p)).count()

    if conteo > 0:
        thisPic = PersonaMedia.objects.filter(persona__id=int(p))[int(n)]

        if int(n) == (conteo-1):
            next_p = 0
        else:
            next_p = int(n)+1

        return render(request,'view-pg.html',{'thisPic':thisPic,'next_p':str(next_p)})
    else:
        return redirect('/view-persona/{}'.format(p))

def viewGrupo(request,g,p):

    thisG = Grupo.objects.get(pk=int(g))

    nlist = 100
    npics = RelGrupoPersona.objects.filter(grupo__id=int(g)).count()
    npages = math.ceil(npics/nlist)

    li = 0 if int(p)==0 else (int(p)*nlist)
    ls = (1+int(p))*nlist
    articles = RelGrupoPersona.objects.filter(grupo__id=int(g)).order_by('persona__nombre')[li:ls]
    ptitle = "View Grupo: "+thisG.titulo

    if request.method == 'POST':

        if request.POST.get("search_term","")=="":
            results = None
        else:
            keyword = request.POST.get("search_term","")
            results = Persona.objects.filter(Q(nombre__contains=keyword) | Q(biographics__contains=keyword)).order_by('id')
            return render(request,'grupo.html',{'ptitle':ptitle,'thisG':thisG,'ppl':articles,'npages': range(npages),'thispage':int(p), 'cat':g,'results':results})
    else:
        return render(request,'grupo.html',{'ptitle':ptitle,'thisG':thisG,'ppl':articles,'npages': range(npages),'thispage':int(p), 'cat':g,'results':None})

def viewr(request):
    pks = PersonaMedia.objects.filter(persona__tipo='directorio',imgtype=2).values_list('pk', flat=True)
    random_pk = choice(pks)
    random_obj = PersonaMedia.objects.get(pk=random_pk)

    return render(request,'viewr.html',{'thisPic':random_obj})

def relacionarPG(request,p,g):
    sel_persona = Persona.objects.get(pk=int(p))
    sel_grupo = Grupo.objects.get(pk=int(g))

    newRGP = RelGrupoPersona.objects.create(persona=sel_persona,grupo=sel_grupo)

    newRGP.save()

    return redirect('/view-g/{}/0'.format(sel_grupo.id))

def moviedbImport(request,movie_id):
    import requests
    import json
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NmM4MjVlMDFiY2RiMWQ1NWQ4YjRmYzNiNDQ0ODFhZiIsInN1YiI6IjYwMWM1NmFkNzMxNGExMDAzZGZjMzhiOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vnpzsejhhlKDqssAg1dHiMH64Ja4_bP2UPcJFgHrW3k"
    }

    response = requests.get(url, headers=headers)
    movie_dict = json.loads(response.text)

    str_titulo = movie_dict['original_title']
    str_overview = movie_dict['overview']
    str_premiere = movie_dict['release_date']
    str_poster = "https://image.tmdb.org/t/p/w200{}".format(movie_dict['poster_path'])

    url = "https://api.themoviedb.org/3/movie/{}/credits?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NmM4MjVlMDFiY2RiMWQ1NWQ4YjRmYzNiNDQ0ODFhZiIsInN1YiI6IjYwMWM1NmFkNzMxNGExMDAzZGZjMzhiOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vnpzsejhhlKDqssAg1dHiMH64Ja4_bP2UPcJFgHrW3k"
    }

    response = requests.get(url, headers=headers)
    movie_dict = json.loads(response.text)

    int_c = 0
    for c in movie_dict['crew']:
        if c['job']=='Director':
            int_c = int_c + 1
            if int_c == 1:
                str_director = c['original_name']
    str_cast = ""
    for c in movie_dict['cast']:
        str_cast = str_cast+c['original_name']+","

    str_cast = str_cast[:-1]

    str_tags = str_director+","+str_premiere[0:4]+","+str_cast

    if request.method=='POST':
        cat_id = request.POST.get("categoria")
        objCategoria = Categoria.objects.get(pk=int(cat_id))
        post_titulo = request.POST.get("titulo")
        post_contenido = request.POST.get("contenido")
        hoy = datetime.now()
        post_fecha = request.POST.get("fecha")

        newItem = Item.objects.create(item_cat=objCategoria,titulo=post_titulo,contenido=post_contenido,fecha=post_fecha)
        newItem.save()


        if request.POST.get("itmtags",""):
            ltags = request.POST.get("itmtags","").split(",")
            contador_n = 1
            for t in ltags:
                bt = ItemTag.objects.create(item_t=newItem,tag=t.strip())
                bt.save()
                if newItem.item_cat.id == 1 and contador_n==1:
                      ItemTable.objects.create(tbl_itm=newItem,campo='author',datos=t.strip())
                elif newItem.item_cat.id==1 and contador_n==2:
                      ItemTable.objects.create(tbl_itm=newItem,campo='pub year',datos=t.strip())
                elif newItem.item_cat.id==2 and contador_n==1:
                      ItemTable.objects.create(tbl_itm=newItem,campo='director',datos=t.strip())
                elif newItem.item_cat.id==2 and contador_n==2:
                      ItemTable.objects.create(tbl_itm=newItem,campo='premiere',datos=t.strip())
                contador_n = contador_n + 1

        if request.FILES.get("cover"):

            newMedia = WikiMedia.objects.create(med_itm = newItem,imgtype=1,imagen=request.FILES.get("cover"),mtags='cover')
            newMedia.save()
        return redirect('/item/'+str(newItem.id))
    else:
        return render(request,'get-movie.html',{'str_tags':str_tags,'str_titulo':str_titulo,'str_overview':str_overview,'str_premiere':str_premiere,'str_poster':str_poster,'str_director':str_director,'str_cast':str_cast})

def togetmovie(request):
    if request.method == 'POST':
        movie_id = request.POST.get("movie_id")
        return redirect('/movie-import/{}'.format(movie_id))

def startNoteConsumo(request):
    obj_nota = Notes.objects.get(pk=int(request.POST.get("note_id")))
    imagen = request.FILES.get("cover_pic")
    newN = NoteMedia.objects.create(nota=obj_nota,cover_pic=imagen,start_date=request.POST.get("start_date"))
    newN.save()
    return redirect('/item/{}'.format(obj_nota.item_note.id))

def finishNoteConsumo(request):
    noteM = NoteMedia.objects.get(pk=request.POST.get("nmid"))
    NoteMedia.objects.filter(pk=noteM.id).update(start_date=request.POST.get("start_date"),finish_date=request.POST.get("finish_date"))
    return    redirect('/item/{}'.format(noteM.nota.item_note.id))

def addItemCredits(request):
    per_ids = request.POST.get("per_ids","").split(",")
    credito = request.POST.get("credit","")
    itm = Item.objects.get(pk=int(request.POST.get("iid")))



    for ic in per_ids:
        person = Persona.objects.get(pk=int(ic.strip()))
        newRTP = RelItemPersona.objects.create(item=itm,persona=person,credit=credito)
        newRTP.save()

    return redirect('/item/{}'.format(itm.id))

def updateProgress(request):
    thisconsumo = Consumo.objects.get(pk=int(request.POST.get("con_id")))
    nultimoCon = ConsumoHist.objects.filter(consumo__id=thisconsumo.id).count()
    if nultimoCon > 0:
        ultimoCon = ConsumoHist.objects.filter(consumo__id=thisconsumo.id).latest('id')
    else:
        ultimoCon = None
    if ultimoCon:
        antP = ultimoCon.progreso
        nowP = int(request.POST.get("progreso")) - antP
    else:
        antP = 0
        nowP = int(request.POST.get("progreso"))

    if int(request.POST.get("progreso")) > antP and int(request.POST.get("progreso")) <= thisconsumo.cantidad:
        newConHist = ConsumoHist.objects.create(consumo=thisconsumo,r_fecha = request.POST.get("r_fecha"), progreso = int(request.POST.get("progreso")), anterior = antP, nowcon = nowP)
        newConHist.save()
    if thisconsumo.cantidad == int(request.POST.get("progreso")):
        Consumo.objects.filter(id=thisconsumo.id,fecha_fin__isnull=True).update(fecha_fin=request.POST.get("r_fecha"))

    return redirect('/')

def addGrupo(request):
    if request.method=='POST':
        newG = Grupo.objects.create(titulo=request.POST.get("titulo"),desc=request.POST.get("desc"),tipo=request.POST.get("tipo"))
        newG.save()
    return render(request,'add-grupo.html',{})


def savePersonaDT(request):
    p_id = int(request.POST.get("pid"))
    input_data = request.POST.get("pDT")
    person = Persona.objects.get(pk=p_id)
    n_datos = PersonaDT.objects.filter(persona__id=p_id).count()

    if n_datos == 0:
        newD = PersonaDT.objects.create(persona=person,strDT=input_data)
        newD.save()
    else:
        thisPDT = PersonaDT.objects.filter(persona__id=p_id).update(strDT=input_data)


    return redirect('/view-persona/{}'.format(p_id))



def addPartido(request,lid):
    liga = Liga.objects.get(pk=lid)
    equipos = LigaTeams.objects.filter(ligaRel__id=liga.id,flagActivo=True).order_by('equipoRel__nombre')
    last_matches = Partido.objects.all().order_by('-id')[0:10]
    ligas = Liga.objects.all().order_by('-id')

    if request.method == 'POST':
        id_el = request.POST.get("local")
        id_ev = request.POST.get("visit")
        fecha = request.POST.get("fecha")
        fase = request.POST.get("fase")

        el = Equipo.objects.get(pk=int(id_el))
        ev = Equipo.objects.get(pk=int(id_ev))

        newM = Partido.objects.create(fecha=fecha,liga=liga,local=el,visita=ev,terminado=False,fase=fase)
        newM.save()
        last_mr = Partido.objects.latest('id')

        return render(request,'add-partido.html',{'liga':liga,'equipos':equipos,'last_m':last_mr,'lm':last_matches,'ligas':ligas})
    else:
        last_mr = Partido.objects.latest('id')
        return render(request,'add-partido.html',{'liga':liga,'equipos':equipos,'last_m':last_mr,'lm':last_matches,'ligas':ligas})


def viewMatches(request,sta):
    match_stat = sta

    ligas = Liga.objects.all().order_by('-id')
    equipos = Equipo.objects.all().order_by('nombre')

    if sta == "1":
        titulo = "Coming Fixtures"
        ot = "Finished"
        iot = "/viewmatches/2"
        matches = Partido.objects.filter(terminado=False,fecha__gte='2022-12-25').order_by('fecha')[0:50]
    elif sta=="2":
        titulo = "Finished Fixtures"
        ot = "Coming"
        iot = "/viewmatches/1"
        matches = Partido.objects.filter(terminado=True).order_by('-fecha')[0:50]

    return render(request,'view-matches.html',{'matches':matches,'ligas':ligas,'ptitulo':titulo,'ot':ot,'iot':iot,'equipos':equipos})


def viewLiga(request,sta,lig):
    match_stat = sta

    ligas = Liga.objects.all().order_by('-id')
    liga = Liga.objects.get(pk=lig)

    if sta == "1":
        titulo = "Coming Fixtures"
        ot = "Finished"
        iot = "/viewliga/2/"+str(lig)
        matches = Partido.objects.filter(terminado=False,liga__id=int(lig)).order_by('fecha')[0:30]
        nmatches = Partido.objects.filter(terminado=False,liga__id=int(lig)).order_by('fecha').count()
    elif sta=="2":
        titulo = "Finished Fixtures"
        ot = "Coming"
        iot = "/viewliga/1/"+str(lig)
        matches = Partido.objects.filter(terminado=True,liga__id=int(lig)).order_by('-fecha')

    if sta=="1" and nmatches==0:
        return redirect("/viewliga/2/{}".format(liga.id))
    else:
        return render(request,'view-liga.html',{'matches':matches,'ligas':ligas,'ptitulo':titulo,'ot':ot,'iot':iot,'lig':liga})

def viewMatch(request,pid):

    listado = ["Goal Keeper","Defender","Midfielder","Forward","Not Specified"]

    ligas = Liga.objects.all().order_by('-id')



    partido = Partido.objects.get(pk=pid)
    comentarios = PartidoComment.objects.filter(comm_partido__id=partido.id).order_by('-minuto','-id')
    lig = partido.liga.id
    matches = Partido.objects.filter(terminado=False,liga__id=lig,fecha__gte=partido.fecha).exclude(id=pid).order_by('fecha','id')[0:20]

    jugadores_local = Contrato.objects.filter(equ__id=partido.local.id,active=True).order_by('jug__nombre')
    jugadores_visit = Contrato.objects.filter(equ__id=partido.visita.id,active=True).order_by('jug__nombre')

    lgoles = Goles.objects.filter(partido__id=pid,asignado=1,penales=False).order_by('minuto','adicional')
    vgoles = Goles.objects.filter(partido__id=pid,asignado=2,penales=False).order_by('minuto','adicional')

    lpens = Penales.objects.filter(partido__id=pid,asignado=1).order_by('id')
    vpens = Penales.objects.filter(partido__id=pid,asignado=2).order_by('id')

    if request.method == 'POST':

        cid = request.POST.get("contrato")
        minuto = request.POST.get("minuto")
        adicional = request.POST.get("adicional")
        ct = Contrato.objects.get(pk=cid)
        asig = request.POST.get("asignado")

        if request.POST.get("penal","0")=="0":
            pn = False
        else:
            pn = True

        if request.POST.get("autogol","0")=="0":
            og = False
        else:
            if asig=="1":
                asig="2"
            else:
                asig="1"

            og = True

        newG = Goles.objects.create(partido=partido,asignado=asig,contrato=ct,minuto=minuto,adicional=adicional,penal=pn,penales=False,og=og)
        newG.save()

        return render(request,'partido.html',{'matches':matches,'partido':partido,'jlocal':jugadores_local,'jvisit':jugadores_visit,'lgoles':lgoles,'vgoles':vgoles,'lpens':lpens,'vpens':vpens,'ligas':ligas,'listado':listado,'comentarios':comentarios})

    else:
        return render(request,'partido.html',{'matches':matches,'partido':partido,'jlocal':jugadores_local,'jvisit':jugadores_visit,'lgoles':lgoles,'vgoles':vgoles,'lpens':lpens,'vpens':vpens,'ligas':ligas,'listado':listado,'comentarios':comentarios})

def closeMatch(request,pid):
    partido = Partido.objects.get(pk=pid)
    partido.terminado = True
    partido.save()
    return redirect("/viewmatch/{}".format(pid))

def addContract(request,pid):

    eid = request.POST.get("asignado")

    equipo = Equipo.objects.get(pk=int(eid))

    nombre = request.POST.get("nombre")
    pais = request.POST.get("pais")
    position = request.POST.get("position")
    number = request.POST.get("number")

    newJugador = Jugador.objects.create(nombre=nombre,pais=pais, biographics="This section nees to be expanded.")
    newJugador.save()

    newC = Contrato.objects.create(jug=newJugador,equ=equipo,active=True, position=position,number = number)
    newC.save()

    return redirect('/viewmatch/{}'.format(pid))


def regPenRound(request,pid):
    partido = Partido.objects.get(pk=pid)

    asignado = request.POST.get("asignado")
    contrato_id = request.POST.get("contrato")
    contrato = Contrato.objects.get(pk=contrato_id)

    if request.POST.get("anotado","0")=="0":
        anotado = False
    else:
        anotado = True

    newP = Penales.objects.create(partido=partido,asignado=asignado,contrato=contrato,anotado=anotado)
    newP.save()

    if anotado == True:
        newG = Goles.objects.create(partido=partido,asignado=asignado,contrato=contrato,minuto=121,adicional=0,penal=False,penales=True,og=False)
        newG.save()

    return redirect('/viewmatch/{}'.format(pid))



def sccteam(request,t):
    import datetime
    thisEquipo = Equipo.objects.get(pk=t)
    ligas = Liga.objects.all().order_by('-id')
    matches = Partido.objects.filter(Q(visita__id=int(t)) | Q(local__id=int(t))).exclude(terminado=False).order_by('-fecha')[0:10]
    contratos = Contrato.objects.filter(equ__id=int(t),active=True).order_by('number')
    fec_hoy = datetime.date.today()
    thisY = fec_hoy.strftime("%Y")
    antY = int(thisY)-1
    goal_table = Goles.objects.raw("select 1 as id, jugador,jugador_id, sum(case when anho='{}' then goles else 0 end) goles, sum(case when anho='{}' then goles else 0 end) goles_ant from futbol_scoreres where equipo_id={} group by jugador,jugador_id order by sum(case when anho='{}' then goles else 0 end) desc".format(int(thisY),antY,thisEquipo.id,int(thisY)))
    listado = ["Goal Keeper","Defender","Midfielder","Forward","Not Specified"]
    listado2 = []
    for l in listado:
        conteo = Contrato.objects.filter(equ__id=int(t),active=True,position=l).count()
        if conteo > 0:
            listado2.append(l)
    return render(request,'sccteam.html',{'matches':matches,'ligas':ligas,'thisEquipo':thisEquipo,'contratos':contratos,'listado':listado2,'goal_table':goal_table,'thisY':thisY})


def addsecleg(request):

    match = request.POST.get("partido","")
    fecha = request.POST.get("fecha","")

    old_match = Partido.objects.get(pk=int(match))

    newP = Partido.objects.create(fecha=fecha,liga=old_match.liga,local=old_match.visita,visita=old_match.local,terminado=False,fase=old_match.fase)
    newP.save()
    return redirect('/viewmatch/{}'.format(newP.id))


def jugadores(request):

    jugadores = Jugador.objects.all().order_by('-id')

    if request.method == 'POST':
        pnombre = request.POST.get("nombre","")
        ppais = request.POST.get("pais","")

        newJ = Jugador.objects.create(nombre=pnombre,pais=ppais, biographics = "This section needs to be expanded.")
        newJ.save()

        return redirect('/jugador/{}'.format(newJ.id))
    else:
        return render(request,'players.html',{'jugadores':jugadores})

def jugador(request,jid):
    jug = Jugador.objects.get(pk=int(jid))
    contratos = Contrato.objects.filter(jug__id=int(jid)).order_by('-id')
    equipos = Equipo.objects.all().order_by('nombre')
    goal_table = Goles.objects.raw("select 1 as id, liga,liga_id,equipo, sum(goles) goles, sum(cast(penales as int)) penales, sum(goles_contra) goles_contra from futbol_scoreres where jugador_id={} group by liga,liga_id,equipo order by liga_id desc".format(jug.id))
    listado = ["Goal Keeper","Defender","Midfielder","Forward","Not Specified"]

    if request.method == 'POST' and request.POST.get("team","0") != "0":
        equ_id = request.POST.get("team","0")

        equipon = Equipo.objects.get(pk=int(equ_id))

        position = request.POST.get("position")
        number = request.POST.get("number")


        newC = Contrato.objects.create(jug=jug,equ=equipon,position=position,number = number)
        newC.save()

        return render(request,'player.html',{'jug':jug,'contratos':contratos,'equipos':equipos})
    elif request.method == 'POST' and request.POST.get("team","0") == "0":
        pnombre = request.POST.get("nombre","")
        ppais = request.POST.get("pais","")

        newJ = Jugador.objects.create(nombre=pnombre,pais=ppais)
        newJ.save()

        equ_id = request.POST.get("team2","0")

        equipon = Equipo.objects.get(pk=int(equ_id))

        position = request.POST.get("position")
        number = request.POST.get("number")

        newC = Contrato.objects.create(jug=newJ,equ=equipon,position=position,number = number)
        newC.save()

        return redirect('/jugador/{}'.format(newJ.id))
    else:
        return render(request,'player.html',{'jug':jug,'contratos':contratos,'equipos':equipos,'listado':listado,'goal_table':goal_table})

def addpartidocomm(request):
    partido = request.POST.get("partido","0")
    comm = request.POST.get("comm","")
    minuto = request.POST.get("minuto","0")
    obj_partido = Partido.objects.get(pk=int(partido))

    newC = PartidoComment.objects.create(comm_partido=obj_partido,comm=comm,minuto=int(minuto),tipo=1)
    #1: Comentarios
    #2: Goal
    newC.save()

    return redirect('/viewmatch/{}'.format(partido))


def addPlayerv2(request):
    pnombre = request.POST.get("nombre","")
    ppais = request.POST.get("pais","")
    partido = request.POST.get("partido","0")

    prev_conteo = Jugador.objects.filter(nombre=pnombre).count()

    if prev_conteo == 0:
        newJ = Jugador.objects.create(nombre=pnombre,pais=ppais)
        newJ.save()
        equ_id = request.POST.get("equipo","0")
        equipon = Equipo.objects.get(pk=int(equ_id))
        position = request.POST.get("position")
        number = request.POST.get("number")
        newC = Contrato.objects.create(jug=newJ,equ=equipon,position=position,number = number)
        newC.save()
        return redirect('/viewmatch/{}'.format(int(partido)))
    else:
        return redirect('/jugadores/')


def addSoccerTeam(request):
    if request.method == 'POST':
        newT = Equipo.objects.create(nombre=request.POST.get("nombre"),pais=request.POST.get("pais"),logo=request.FILES.get("logo"))
        newT.save()

        return render(request,'add-soccer-team.html',{})
    else:
        return render(request,'add-soccer-team.html',{})



def editPartido(request,pid):
    thisMatch = Partido.objects.get(pk=int(pid))
    equipos = LigaTeams.objects.filter(ligaRel__id=thisMatch.liga.id,flagActivo=True).order_by('equipoRel__nombre')
    thisliga = Liga.objects.get(pk=thisMatch.liga.id)

    if request.method == 'POST':
        id_el = request.POST.get("local")
        id_ev = request.POST.get("visit")
        fecha = request.POST.get("fecha")
        fase = request.POST.get("fase")

        el = Equipo.objects.get(pk=int(id_el))
        ev = Equipo.objects.get(pk=int(id_ev))

        Partido.objects.filter(id=thisMatch.id).update(fecha=fecha,liga=thisliga,local=el,visita=ev,terminado=False,fase=fase)
        return redirect('/viewmatch/{}'.format(thisMatch.id))
    else:
        return render(request,'edit-partido.html',{'thisMatch':thisMatch,'equipos':equipos})

def editContrato(request,c):
    thisC = Contrato.objects.get(pk=int(c))
    thisP = Jugador.objects.get(pk=thisC.jug.id)
    listado = ["Goal Keeper","Defender","Midfielder","Forward","Not Specified"]
    ngoles = Goles.objects.filter(contrato__id=thisC.id).count()

    og=0
    classGoles = None
    pn=0
    reg = 0

    if ngoles > 0:
        og = 0
        pn = 0
        reg = 0
        goles = Goles.objects.filter(contrato__id=thisC.id)
        classGoles = Goles.objects.filter(contrato__id=thisC.id,og=False).values('partido__liga__nombre').annotate(qgoles=Count('id'),maxfecha=Max('partido__fecha')).order_by('-maxfecha')
        for g in goles:
            if g.og == True:
                og = og + 1
            elif g.penal == True or g.penales == True:
                pn = pn + 1
            elif g.og == False and  g.penal== False and g.penales == False:
                reg = reg + 1



    if request.method == 'POST':
        Jugador.objects.filter(id=thisP.id).update(nombre=request.POST.get("nombre"),pais = request.POST.get("pais"))

        if request.POST.get("active"):
            checkb = True
        else:
            checkb = False


        Contrato.objects.filter(id=thisC.id).update(position= request.POST.get("position"),number= request.POST.get("number"),active=checkb)
        return redirect('/team/{}'.format(thisC.equ.id))
    else:
        return render(request,'edit-contrato.html',{'thisC':thisC,'listado':listado,'ngoles':(ngoles-og),'classGoles':classGoles,'pn':pn,'og':og,'reg':reg})

def editBiographics(request,c):
    thisC = Contrato.objects.get(pk=int(c))
    thisP = Jugador.objects.get(pk=thisC.jug.id)
    listado = ["Goal Keeper","Defender","Midfielder","Forward","Not Specified"]

    if request.method == 'POST':
        Jugador.objects.filter(id=thisP.id).update(biographics=request.POST.get("biographics"))
        return redirect('/view-contrato/{}'.format(thisC.id))
    else:
        return render(request,'edit-pbio.html',{'thisC':thisC,'listado':listado})



def viewTable(request,liga):
    tp = Liga.objects.raw("select 1 as id, * from position_tables where ligaid={} order by ptos desc, dg desc".format(liga))
    tp2 = Liga.objects.raw("select 1 as id, * from fase_grups where ligaid={} order by fase, ptos desc, dg desc".format(liga))
    tg = Goles.objects.raw("select 1 as id, * from liga_goleadores where liga={} order by goles desc, penales desc".format(liga))

    matches = Partido.objects.filter(terminado=True,liga__id=int(liga)).exclude(fase__contains='Group').order_by('-fecha')

    liga = Liga.objects.get(pk=int(liga))
    ligas = Liga.objects.all().order_by('-id')
    if 'Champions' in liga.nombre:
        tipo = 'grupos'
    else:
        tipo = 'liga'


    return render(request,'viewtable.html',{'tp':tp,'thisLiga':liga,'ligas':ligas,'tablagoles':tg, 'tp2':tp2,'tipo':tipo,'partidos':matches})

def editComm(request,commid):
    comentario = PartidoComment.objects.get(pk=int(commid))
    if request.method == 'POST':
        PartidoComment.objects.filter(id=int(commid)).update(comm=request.POST.get("comm"))
        return redirect('/viewmatch/{}'.format(comentario.partido.id))
    else:
        return render(request,'edit-comm.html',{'comentario':comentario})

def wikipages(request):
    wikis = sorted(Item.objects.filter(item_cat__id=16),key=lambda t: t.lastmod, reverse=True)
    return render(request,'wikis.html',{'wikis':wikis})

def wikipage(request, wid):
    wiki = Item.objects.get(pk=wid)
    children = WikiChild.objects.filter(parent__id = int(wid))
    return render(request,'wiki.html',{'wiki':wiki,'children':children})

def addwikichild(request,parent_id):
    wp = Item.objects.get(pk=parent_id)

    if request.method == 'POST':
        newWC = WikiChild.objects.create(parent = wp, titulo = request.POST.get("titulo"), bio = request.POST.get("bio"), tabla='', fechaM = datetime.today().strftime('%Y-%m-%d'))
        newWC.save()

        return redirect('/wikichild/'+str(newWC.id))
    else:
        return render(request,'add-wikichild.html',{'wp':wp})

def wikichild(request,child_id):
    wc = WikiChild.objects.get(pk=child_id)
    brothers = WikiChild.objects.filter(parent__id=wc.parent.id).exclude(id=int(child_id)).order_by('titulo')
    return render(request,'wikichild.html',{'wc':wc,'brothers':brothers})

def editwikichild(request,child_id):
    wc = WikiChild.objects.get(pk=child_id)
    brothers = WikiChild.objects.filter(parent__id=wc.parent.id).exclude(id=wc.id)

    if request.method == 'POST':
        WikiChild.objects.filter(id=wc.id).update(titulo = request.POST.get("titulo"), bio= request.POST.get("bio"), tabla= request.POST.get("tabla"),  fechaM = datetime.today().strftime('%Y-%m-%d'))
        return redirect('/wikichild/'+str(child_id))
    else:
        return render(request,'edit-wikichild.html',{'wc':wc,'brothers':brothers})

def addwcm(request):
    thisP = WikiChild.objects.get(pk=int(request.POST.get("wchild")))

    for img in request.FILES.getlist("imagen"):
        newP = WCMedia.objects.create(wikichild=thisP,imagen=img)
        newP.save()

    return redirect('/wikichild/{}'.format(thisP.id))

def addmlbgame(request):
    mlbteams = mlbTeam.objects.all().order_by('nombre')

    if request.method=='POST':

        local_t = mlbTeam.objects.get(pk=int(request.POST.get('local')))
        visit_t = mlbTeam.objects.get(pk=int(request.POST.get('visit')))

        lr = int(request.POST.get('score').split(":")[0])
        vr = int(request.POST.get('score').split(":")[1])

        newG = mlbGame.objects.create(fecha=request.POST.get('fecha'),local=local_t,visit=visit_t,local_runs=lr,visit_runa=vr,comentarios=request.POST.get('comments'))

    return render(request,'addmlbgame.html',{'mlbteams':mlbteams})



def mlbpage(request):
    partidos = mlbGame.objects.all().order_by('-fecha')
    wins = 0
    ng = 0
    str_racha = ''
    for p in partidos:
        ng = ng + 1
        if p.local.id == 1 and p.local_runs >  p.visit_runa:
            wins = wins + 1
            if ng <= 7:
                str_racha = str_racha + '&#9989;'
        elif p.visit.id == 1 and p.local_runs <  p.visit_runa:
            wins = wins + 1
            if ng<=7:
                str_racha = str_racha + '&#9989;'
        else:
            if ng<=7:
                str_racha = str_racha + '&#10060;'
    loss = ng - wins
    prct = 1.0*wins/ng

    return render(request,'mlbpage.html',{'partidos':partidos,'wins':wins,'ng':ng,'prct':prct,'loss':loss,'racha':str_racha})


def viewsquad(request,par_id,equ_id):
    check_squad = matchSquad.objects.filter(equipo__id=int(equ_id),partido__id=int(par_id)).count()

    this_equipo = Equipo.objects.get(pk=int(equ_id))
    this_partido = Partido.objects.get(pk=int(par_id))

    if check_squad == 0:
        new_S = matchSquad.objects.create(equipo=this_equipo,partido=this_partido)
        new_S.save()
        sc_id = new_S.id
        plantilla = squadPlayers.objects.filter(squad__id=new_S.id)
    else:
        this_squad =  matchSquad.objects.filter(equipo__id=int(equ_id),partido__id=int(par_id)).latest('id')
        sc_id = this_squad.id
        plantilla = squadPlayers.objects.filter(squad__id=this_squad.id)

    contratos = Contrato.objects.filter(equ__id=int(equ_id))

    listado = ["Goal Keeper","Defender","Midfielder","Forward","Not Specified"]
    
    porteros = []
    defensas = []
    medicampos = []
    delateros = []
    not_spec = []

    for p in plantilla:
        if p.jugador.position == "Goal Keeper":
            porteros.append(p)
        elif p.jugador.position == "Defender":
            defensas.append(p)
        elif p.jugador.position == "Midfielder":
            medicampos.append(p)
        elif p.jugador.position == "Forward":
            delateros.append(p)
        elif p.jugador.position == "Not Specified":
            not_spec.append(p)


    return render(request,'squad.html',{'plantilla':plantilla,
                                        'contratos':contratos,
                                        'partido':this_partido,
                                        'equipo':this_equipo,
                                        'porteros':porteros,
                                        'defensas':defensas,
                                        'medicampos':medicampos,
                                        'delateros':delateros,
                                        'not_spec':not_spec,
                                        'sc_id':sc_id})

def updateSquad(request):

    plantilla = matchSquad.objects.get(pk=int(request.POST.get("squad_id")))
    contrato = Contrato.objects.get(pk=int(request.POST.get("contrato")))
    tipo = request.POST.get("tipo")

    newLP = squadPlayers.objects.create(squad=plantilla,jugador=contrato,tipo=tipo)


    return redirect('/squad/{}/{}'.format(plantilla.partido.id,plantilla.equipo.id))