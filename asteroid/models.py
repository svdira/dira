from django.db import models
from datetime import datetime
from system.storage import ImageStorage
from django.db import models
from django.utils import timezone
import os
from uuid import uuid4
from django.db.models import Q, Avg, Count, Min, Sum
from random import choice

def path_and_name(instance, filename):
    upload_to = 'wiki_media'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Categoria(models.Model):
	nombre = models.CharField(max_length=120)
	desc = models.CharField(max_length=512)

	def __str__(self):
		return self.nombre


class Item(models.Model):
	item_cat = models.ForeignKey(Categoria,on_delete=models.CASCADE)
	titulo = models.CharField(max_length=512)
	contenido = models.TextField()
	fecha = models.DateField()

	@property
	def mainPic(self):
		npics = WikiMedia.objects.filter(med_itm__id=self.id,imgtype=1).count()

		if npics == 0:
			return None
		else:
			pks = WikiMedia.objects.filter(med_itm__id=self.id,imgtype=1).values_list('pk', flat=True)
			random_pk = choice(pks)
			ppic = WikiMedia.objects.get(pk=random_pk)
			return ppic.imagen.url

	@property
	def mainLand(self):
		npics = WikiMedia.objects.filter(med_itm__id=self.id,imgtype=2).count()

		if npics == 0:
			return None
		else:
			pks = WikiMedia.objects.filter(med_itm__id=self.id,imgtype=2).values_list('pk', flat=True)
			random_pk = choice(pks)
			ppic = WikiMedia.objects.get(pk=random_pk)
			return ppic.imagen.url

	@property
	def short_desc(self):
		return self.contenido[0:700]

	@property
	def card_desc(self):
		return self.contenido[0:200]

	@property
	def ncon(self):
		nq = Consumo.objects.filter(con_itm__id=self.id,fecha_fin__isnull=False).count()
		return nq

	@property
	def notes(self):
		notas = Notes.objects.filter(item_note__id=self.id)
		return notas

	@property
	def pubyear(self):
		q = ItemTable.objects.filter(tbl_itm__id=self.id,campo__in=['pub year','premiere']).count()

		if q == 0:
			pubyear = 0
		else:
			anhos = ItemTable.objects.filter(tbl_itm__id=self.id,campo__in=['pub year','premiere'])
			for an in anhos:
				pubyear = int(an.datos)

		return pubyear

	@property
	def author(self):
		q = RelItemPersona.objects.filter(item__id=self.id,credit='author').count()

		if q == 0:
			pubyear = 0
		else:
			anhos = RelItemPersona.objects.filter(item__id=self.id,credit='author')
			for an in anhos:
				pubyear = an.persona.nombre

		return pubyear

	@property
	def lastr(self):
		nq = Consumo.objects.filter(con_itm__id=self.id,fecha_fin__isnull=False).count()
		if nq == 0:
			return '1970-12-31'
		else:
			lcon = Consumo.objects.filter(con_itm__id=self.id,fecha_fin__isnull=False).latest('fecha_fin')
		return "{}".format(lcon.fecha_fin)


	@property
	def lastmod(self):
		nq = WikiChild.objects.filter(parent__id=self.id).count()
		if nq == 0:
			return "1999-12-31"
		else:
			lcon = WikiChild.objects.filter(parent__id=self.id).latest('fechaM')
		return "{}".format(lcon.fechaM)

	def __str__(self):
		return self.titulo



class ItemTag(models.Model):
	item_t = models.ForeignKey(Item,on_delete=models.CASCADE)
	tag = models.CharField(max_length=75)

	def __str__(self):
		return self.tag

class ItemTable(models.Model):
	tbl_itm = models.ForeignKey(Item,on_delete=models.CASCADE)
	campo = models.CharField(max_length=128)
	datos = models.TextField()

	def __str__(self):
		return self.tbl_itm.titulo+'-'+self.campo


	@property
	def mainPic(self):
		npics = ItemTableMedia.objects.filter(itm_tbl__id=self.id,imgtype=1).count()

		if npics == 0:
			return None
		else:
			pks = ItemTableMedia.objects.filter(itm_tbl__id=self.id,imgtype=1).values_list('pk', flat=True)
			random_pk = choice(pks)
			ppic = ItemTableMedia.objects.get(pk=random_pk)
			return ppic.imagen.url

class Consumo(models.Model):
	con_itm = models.ForeignKey(Item,on_delete=models.CASCADE)
	unidades = models.CharField(max_length=60)
	cantidad = models.IntegerField()
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField(null=True)
	season = models.IntegerField(default=0)
	lan = models.CharField(max_length=2,default="ND")
	formato = models.CharField(max_length=128,default="ND")
	mutiplicador = models.IntegerField(default=1)

	def __str__(self):
		return self.con_itm.titulo

	@property
	def progreso(self):
	    ultimoProgreso = ConsumoHist.objects.filter(consumo__id = self.id).latest('id')
	    if ultimoProgreso:
	        avance = {'progreso':ultimoProgreso.progreso,'por_av':round(100*round(ultimoProgreso.progreso*1.0/self.cantidad,2),1)}
	    else:
	        avance = {'progreso':0,'por_av':0.0}
	    return avance

class WikiMedia(models.Model):
	med_itm = models.ForeignKey(Item,on_delete=models.CASCADE)
	imgtype = models.IntegerField()
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)
	mtags = models.CharField(max_length=512)

	def __str__(self):
		return self.med_itm.titulo

class Coleccion(models.Model):
	nombre = models.CharField(max_length=256)
	info = models.CharField(max_length=512)
	cfecha = models.DateField(default="2022-09-14")

	def __str__(self):
		return self.nombre

	@property
	def qitems(self):
		qi = ColItem.objects.filter(col__id=self.id).count()
		return qi

class ColItem(models.Model):
	itm = models.ForeignKey(Item, on_delete = models.CASCADE)
	col = models.ForeignKey(Coleccion, on_delete = models.CASCADE)

	def __str__(self):
		return self.col.nombre+'--'+self.itm.titulo

class Cuenta(models.Model):
	nombre = models.CharField(max_length=150)
	tipo = models.IntegerField()

	def __str__(self):
		return self.nombre

class TrxTyp(models.Model):
	desc = models.CharField(max_length=200)
	codigo = models.IntegerField()

	def __str__(self):
		return self.desc

class Trx(models.Model):
	fecha = models.DateField()
	debito = models.ForeignKey(Cuenta, on_delete = models.CASCADE)
	credito = models.ForeignKey(TrxTyp, on_delete = models.CASCADE)
	monto = models.DecimalField(max_digits=16,decimal_places=2,default=0.00)
	desc = models.CharField(max_length=200)

	def __str__(self):
		return self.credito.desc +'--'+ str(self.fecha)


class Budget(models.Model):
	cuenta = models.ForeignKey(TrxTyp,on_delete=models.CASCADE)
	anho = models.IntegerField()
	mes = models.IntegerField()
	mbudget = models.DecimalField(max_digits=16,decimal_places=2,default=0.00)

	def __str__(self):
		return str(self.anho)+'-'+str(self.mes)+':'+self.cuenta.desc




class ItemTableMedia(models.Model):
	itm_tbl = models.ForeignKey(ItemTable,on_delete=models.CASCADE)
	imgtype = models.IntegerField()
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)
	mtags = models.CharField(max_length=512)

	def __str__(self):
		return self.itm_tbl.campo


class Notes(models.Model):
    item_note = models.ForeignKey(Item,on_delete = models.CASCADE)
    titulo = models.CharField(max_length=256)
    texto = models.TextField()

    def __str__(self):
        return str(self.titulo)

    @property
    def InPogress(self):
        r_notes = NoteMedia.objects.filter(nota__id=self.id).count()
        if r_notes > 0:
            p_notes = NoteMedia.objects.filter(nota__id=self.id)
            for i in p_notes:
                obj_consumo = i
            return obj_consumo
        else:
            return None


class Persona(models.Model):
	nombre = models.CharField(max_length=512)
	biographics = models.TextField()
	tipo = models.CharField(max_length=32)
	last_update = models.DateTimeField(auto_now_add=True)

	def mainPic(self):
		npics = PersonaMedia.objects.filter(persona__id=self.id,imgtype=1).count()

		if npics == 0:
			return False
		else:
			pks = PersonaMedia.objects.filter(persona__id=self.id,imgtype=1).values_list('pk', flat=True)
			random_pk = choice(pks)
			ppic = PersonaMedia.objects.get(pk=random_pk)
			return ppic.imagen.url

	def __str__(self):
		return self.nombre

class PersonaMedia(models.Model):
	persona = models.ForeignKey(Persona,on_delete=models.CASCADE)
	imgtype = models.IntegerField()
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)

	def __str__(self):
		return self.persona.nombre


class Grupo(models.Model):
	titulo = models.CharField(max_length=256)
	desc = models.TextField(default='TBD')
	tipo = models.CharField(max_length=200,default='no-asignado')

	def __str__(self):
		return self.titulo

	def npers(self):
		conteo = RelGrupoPersona.objects.filter(grupo__id=self.id).count()
		return conteo


class RelGrupoPersona(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

	def __str__(self):
		return self.persona.nombre+' in '+self.grupo.titulo

class NoteMedia(models.Model):
	nota = models.ForeignKey(Notes, on_delete=models.CASCADE)
	cover_pic = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)
	start_date = models.DateField()
	finish_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.nota.item_note.titulo+'-'+self.nota.titulo

	@property
	def estatus(self):
		if self.finish_date is None:
			return 0
		else:
			return 1

class RelItemPersona(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	credit = models.CharField(max_length=256)

	def __str__(self):
		return self.item.titulo+'-'+self.persona.nombre

class ConsumoHist(models.Model):
    consumo = models.ForeignKey(Consumo, on_delete=models.CASCADE)
    r_fecha = models.DateField()
    progreso = models.IntegerField()
    anterior = models.IntegerField(default=0)
    nowcon = models.IntegerField(default=0)

    def __str__(self):
        return self.consumo.con_itm.titulo

class attFecha(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	campo = models.CharField(max_length=255)
	valor = models.DateField()

	def __str__(self):
		return self.persona.nombre+'-'+self.campo

class attEntero(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	campo = models.CharField(max_length=255)
	valor = models.IntegerField()

	def __str__(self):
		return self.persona.nombre+'-'+self.campo

class attCadena(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	campo = models.CharField(max_length=255)
	valor = models.TextField()

	def __str__(self):
		return self.persona.nombre+'-'+self.campo


class attDecimal(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	campo = models.CharField(max_length=255)
	valor = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

	def __str__(self):
		return self.persona.nombre+'-'+self.campo

class PartidoFutbol(models.Model):
	equipo_local = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='local_t')
	equipo_visit = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='local_v')
	goles_local = models.IntegerField(default=0)
	goles_visit = models.IntegerField(default=0)
	terminado = models.IntegerField(default=0)
	liga = models.CharField(max_length=255)
	fecha = models.DateField()

	def __str__(self):
		return self.equipo_local.titulo+'-'+self.equipo_visit.titulo

class Goal(models.Model):
	partido = models.ForeignKey(PartidoFutbol,on_delete = models.CASCADE)
	equipo = models.ForeignKey(Grupo,on_delete=models.CASCADE)
	jugador = models.ForeignKey(Persona,on_delete=models.CASCADE)
	asignado = models.IntegerField()
	minuto = models.IntegerField()
	adicional =models.IntegerField()
	penal = models.IntegerField()

	def __str__(self):
		return 'partido_'+str(self.partido.id)+'_'+self.jugador.nombre+'-'+str(self.minuto)

class PersonaDT(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	strDT = models.TextField()

	def __str__(self):
		return self.persona.nombre


class Equipo(models.Model):
	nombre = models.CharField(max_length=128)
	pais = models.CharField(max_length=128)
	logo = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)

	def __str__(self):
		return self.nombre

class Jugador(models.Model):
	nombre = models.CharField(max_length=128)
	pais = models.CharField(max_length=128)
	biographics = models.TextField(default="This section needs to be expanded.")

	def __str__(self):
		return self.nombre

class Contrato(models.Model):
	jug = models.ForeignKey(Jugador, on_delete = models.CASCADE)
	equ = models.ForeignKey(Equipo, on_delete = models.CASCADE)
	active = models.BooleanField(default=True)
	position = models.CharField(default="Not Specified", max_length=256)
	number = models.IntegerField(default = 0)

	def __str__(self):
		return self.jug.nombre+'-'+self.equ.nombre

class Liga(models.Model):
	nombre = models.CharField(max_length=120)

	def __str__(self):
		return self.nombre


class Partido(models.Model):
	fecha = models.DateField()
	liga = models.ForeignKey(Liga, on_delete = models.CASCADE)
	local = models.ForeignKey(Equipo, on_delete = models.CASCADE,related_name="elocal")
	visita = models.ForeignKey(Equipo, on_delete = models.CASCADE,related_name="evisita")
	terminado = models.BooleanField(default=False, blank=True,null=True)
	fase = models.CharField(max_length=120)

	def __str__(self):
		return self.local.nombre+' v '+self.visita.nombre

	@property
	def marcador(self):
		nlocal = Goles.objects.filter(partido__id=self.id,asignado=1,penales=False).count()
		nvisita = Goles.objects.filter(partido__id=self.id,asignado=2,penales=False).count()

		plocal = Goles.objects.filter(partido__id=self.id,asignado=1,penales=True).count()
		pvisita = Goles.objects.filter(partido__id=self.id,asignado=2,penales=True).count()

		if (plocal+pvisita)==0:
			score = "{} - {}".format(nlocal,nvisita)
		else:
			score = "{} ({})-({}) {}".format(nlocal,plocal,pvisita,nvisita)

		return score

	@property
	def comms(self):
		comentarios = PartidoComment.objects.filter(comm_partido__id=self.id)
		txt_comms = ""
		if comentarios:
			for c in comentarios:
				txt_comms = txt_comms +' '+ c.comm

			return txt_comms
		else:
			return None




class Goles(models.Model):
	partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
	asignado = models.IntegerField()
	contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
	minuto = models.IntegerField()
	adicional = models.IntegerField()
	penal = models.BooleanField()
	penales = models.BooleanField()
	og = models.BooleanField(default=False)

	def __str__(self):
		return self.contrato.jug.nombre

	@property
	def descriptor(self):

		if self.adicional>0:
			add = "+"+str(self.adicional)
		else:
			add = ""

		if self.penal:
			p = " pen"
		else:
			p = ""

		if self.og:
			fog = " og"
		else:
			fog =""

		desc = self.contrato.jug.nombre+" "+str(self.minuto)+"'"+add+p+fog

		return desc

class Penales(models.Model):
	partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
	asignado = models.IntegerField()
	contrato = models.ForeignKey(Contrato,on_delete=models.CASCADE)
	anotado = models.BooleanField()

	def __str__(self):
		return str(self.id)

	@property
	def icon(self):
		if self.anotado == True:
			symbol = "&#9989;"
		else:
			symbol = "&#10060;"

		return symbol

class PartidoComment(models.Model):
	comm_partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
	comm = models.TextField()
	minuto  = models.IntegerField(default=0)
	tipo = models.IntegerField(default=0)

	def __str__(self):
		return str(self.id)

class LigaTeams(models.Model):
    ligaRel = models.ForeignKey(Liga,on_delete = models.CASCADE)
    equipoRel = models.ForeignKey(Equipo,on_delete = models.CASCADE)
    flagActivo = models.BooleanField(default=True)

    def __str__(self):
        return self.ligaRel.nombre+'-'+self.equipoRel.nombre

class WikiChild(models.Model):
	parent = models.ForeignKey(Item,on_delete=models.CASCADE)
	titulo = models.CharField(max_length=256)
	bio = models.TextField()
	tabla = models.TextField(default='blank')
	fechaM = models.DateField()

	@property
	def mainPic(self):
		npics = WCMedia.objects.filter(wikichild__id=self.id).count()

		if npics == 0:
			return None
		else:
			pks = WCMedia.objects.filter(wikichild__id=self.id).values_list('pk', flat=True)
			random_pk = choice(pks)
			ppic = WCMedia.objects.get(pk=random_pk)
			return ppic.imagen.url
	
	def __str__(self):
		return self.titulo

class WCMedia(models.Model):
	wikichild = models.ForeignKey(WikiChild,on_delete=models.CASCADE)
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)

	def __str__(self):
		return self.wikichild.titulo


