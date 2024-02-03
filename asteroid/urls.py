from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('plantilla/', views.plantilla, name='plantilla'),
	path('', views.homepage, name='homepage'),
	path('archive/<p>', views.archive, name='archive'),
	path('c/<cat>/<p>', views.category, name='category'),
	path('q/<cat>/<p>', views.catqueue, name='catqueue'),
	path('search/', views.search, name='search'),
	path('additem', views.additem, name='additem'),
	path('item/<iid>', views.item, name='item'),
	path('edititem/<iid>', views.edititem, name='edititem'),
	path('startitem/<iid>', views.startitem, name='startitem'),
	path('tableitem/<iid>', views.tableitem, name='tableitem'),
	path('addmedia/<iid>', views.addMedia, name='addMedia'),
	path('finance/', views.finance, name='finance'),
	path('financemob/', views.finance2, name='finance2'),
	path('savetrx/', views.saveTrx, name='savetrx'),
	path('savepmt/', views.savePmt, name='savepmt'),
	path('addcoleccion/', views.addColeccion, name='addcoleccion'),
	path('coleccion/<id>', views.coleccion, name='coleccion'),
	path('cocovers/<id>/<s>', views.cocovers, name='cocovers'),
	path('additmcol/<it>/<co>', views.additmcol, name='additmcol'),
	
	path('autor/<au>', views.autor, name='autor'),
	path('view-month/<y>/<m>', views.viewmonth, name='viewmonth'),
	path('quemar/<itm>', views.quemar, name='quemar'),
	
	path('addjournalentry/', views.addJournalEntry, name='addJournalEntry'),
	path('edit-itt/<tid>', views.editTable, name='edit-itt'),
	path('year-hist/<y>/<c>', views.yearHist, name='yearHist'),
	path('add-ittmedia/', views.addIttMedia, name='addIttMedia'),
	path('add-ittmedia/', views.addIttMedia, name='addIttMedia'),

	path('publish/<col_id>', views.forKindle, name='kindlePublish'),
	
	path('viewtag/<t>', views.viewtag, name='itag'),


	path('add-notes/<item_id>', views.addNotes, name='addnotes'),
	path('edit-notes/<note_id>', views.editNotes, name='editnotes'),
	path('addbudget/',views.addBudgetReg,name='addBudget'),


    path('diradb/', views.plantilla2, name='plantilla2'),
	path('add-persona/', views.addPersona, name='add-persona'),
	path('view-ppl/<t>/<p>', views.viewPersonas, name='view-ppl'),
	path('view-persona/<p>', views.viewPersona, name='view-persona'),
	path('edit-persona/<p>', views.editPersona, name='edit-persona'),
	path('add-media-persona/', views.addPersonaMedia, name='add-media-persona'),
	path('view-pg/<p>/<n>', views.viewPersonaGallery, name='view-pg'),
	path('view-g/<g>/<p>', views.viewGrupo, name='view-g'),
	path('viewr/', views.viewr, name='viewr'),
	path('relacionarPG/<p>/<g>',views.relacionarPG,name='relacionarPG'),
	path('movie-import/<movie_id>/',views.moviedbImport,name='moviedbImport'),
	path('togetmovie/',views.togetmovie,name='togetmovie'),
	path('startNC/',views.startNoteConsumo,name='startNoteConsumo'),
	path('finishNC/',views.finishNoteConsumo,name='finishNoteConsumo'),
	path('add-item-credits/',views.addItemCredits,name='addItemCredits'),

	path('update-progress/',views.updateProgress,name='updateProgress'),
	path('add-grupo/',views.addGrupo,name='addGrupo'),
	
	path('save-persona-dt/',views.savePersonaDT,name='savePersonaDT'),
	path('viewmatches/<sta>/', views.viewMatches, name='viewmatches'),
	path('viewmatch/<pid>/', views.viewMatch, name='viewmatch'),
	path('editmatch/<pid>/', views.editPartido, name='editmatch'),
	path('closematch/<pid>/', views.closeMatch, name='closematch'),
	path('viewliga/<sta>/<lig>', views.viewLiga, name='viewliga'),
	path('addcontract/<pid>', views.addContract, name='addcontract'),
	path('regpenround/<pid>', views.regPenRound, name='regpenround'),
	path('team/<t>', views.sccteam, name='sccteam'),
	path('addsecleg/', views.addsecleg, name='addsecleg'),
	path('jugadores/', views.jugadores, name='jugadores'),
	path('jugador/<jid>', views.jugador, name='jugador'),
	path('addpartidocomm/',views.addpartidocomm,name="addpartidocomm"),
	path('addplayerv2/', views.addPlayerv2, name='addplayerv2'),
	path('add-soccer-team/',views.addSoccerTeam,name='addSoccerTeam'),
	path('view-contrato/<c>',views.editContrato,name='editContrato'),
	path('edit-bio/<c>',views.editBiographics,name='editBio'),
	path('view-table/<liga>',views.viewTable,name='viewTable'),
	path('addmatch/<lid>/', views.addPartido, name='addmatch'),
	path('edit-comm/<commid>/', views.editComm, name='editComm'),
	path('wikis/', views.wikipages, name='wikis'),
	path('wiki/<wid>', views.wikipage, name='wiki'),
	path('addwikichild/<parent_id>', views.addwikichild, name='addwikichild'),
	path('wikichild/<child_id>', views.wikichild, name='wikichild'),
	path('editwikichild/<child_id>', views.editwikichild, name='editwikichild'),
	path('add-wcm/', views.addwcm, name='addwcm'),

]