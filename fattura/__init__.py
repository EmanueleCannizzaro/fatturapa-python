
__VERSION = "1.3.1"
CONF_FILE = "pyFatturaPA.conf.json"
VAT_DEFAULT = 22.0

EU_MemberStates = {
    'eu':"Europa", 
    'at':"Austria", 
    'be':"Belgio", 
    'bg':"Bulgaria", 
    'cy':"Cipro", 
    'cz':"Repubblica Ceca", 
    'de':"Germania", 
    'dk':"Danimarca", 
    'ee':"Estonia", 
    'el':"Grecia", 
    'es':"Spagna", 
    'fi':"Finlandia", 
    'fr':"Francia", 
    'hr':"Croazia", 
    'hu':"Ungheria", 
    'ie':"Irlanda", 
    'is':"Islanda", 
    'it':"Italia", 
    'li':"Liechtenstein", 
    'lt':"Lituania", 
    'lu':"Lussemburgo", 'lv':"Lettonia", 'mt':"Malta", 'nl':"Paesi Bassi", 'no':"Norvegia", 'pl':"Polonia", 'pt':"Portogallo", 'ro':"Romania", 'se':"Svezia", 
    'si':"Slovenia", 
    'sk':"Slovacchia", 
    'uk':"Regno Unito"
}
REGIONS, PROVINCES = {
	'Abruzzo'              :{'AQ':"L'Aquila", 'CH':"Chieti", 'PE':"Pescara", 'TE':"Teramo"},
	'Basilicata'           :{'MT':"Matera", 'PZ':"Potenza"},
	'Calabria'             :{'CZ':"Catanzaro", 'CS':"Cosenza", 'KR':"Crotone", 'RC':"Reggio-Calabria", 'VV':"Vibo-Valentia"},
	'Campania'             :{'AV':"Avellino", 'BN':"Benevento", 'CE':"Caserta", 'NA':"Napoli", 'SA':"Salerno"},
	'Emilia Romagna'       :{'BO':"Bologna", 'FE':"Ferrara", 'FC':"Forlì-Cesena", 'MO':"Modena", 'PR':"Parma", 'PC':"Piacenza", 'RA':"Ravenna", 'RE':"Reggio-Emilia", 'RN':"Rimini"},
	'Friuli Venezia Giulia':{'GO':"Gorizia", 'PN':"Pordenone", 'TS':"Trieste", 'UD':"Udine"},
	'Lazio'                :{'FR':"Frosinone", 'LT':"Latina", 'RI':"Rieti", 'RM':"Roma", 'VT':"Viterbo"},
	'Liguria'              :{'GE':"Genova", 'IM':"Imperia", 'SP':"La Spezia", 'SV':"Savona"},
	'Lombardia'            :{'BG':"Bergamo", 'BS':"Brescia", 'CO':"Como", 'CR':"Cremona", 'LC':"Lecco", 'LO':"Lodi", 'MN':"Mantova", 'MI':"Milano", 'MB':"Monza-Brianza", 'PV':"Pavia", 'SO':"Sondrio", 'VA':"Varese"},
	'Marche'               :{'AN':"Ancona", 'AP':"Ascoli-Piceno", 'FM':"Fermo", 'MC':"Macerata", 'PU':"Pesaro-Urbino"},
	'Molise'               :{'CB':"Campobasso", 'IS':"Isernia"},
	'Piemonte'             :{'AL':"Alessandria", 'AT':"Asti", 'BI':"Biella", 'CN':"Cuneo", 'NO':"Novara", 'TO':"Torino", 'VB':"Verbania", 'VC':"Vercelli"},
	'Puglia'               :{'BA':"Bari", 'BT':"Barletta-Andria-Trani", 'BR':"Brindisi", 'FG':"Foggia", 'LE':"Lecce", 'TA':"Taranto"},
	'Sardegna'             :{'CA':"Cagliari", 'CI':"Carbonia-Iglesias", 'NU':"Nuoro", 'OG':"Ogliastra", 'OT':"Olbia Tempio", 'OR':"Oristano", 'SS':"Sassari", 'VS':"Medio Campidano"},
	'Sicilia'              :{'AG':"Agrigento", 'CL':"Caltanissetta", 'CT':"Catania", 'EN':"Enna", 'ME':"Messina", 'PA':"Palermo", 'RG':"Ragusa", 'SR':"Siracusa", 'TP':"Trapani"},
	'Toscana'              :{'AR':"Arezzo", 'FI':"Firenze", 'GR':"Grosseto", 'LI':"Livorno", 'LU':"Lucca", 'MS':"Massa-Carrara", 'PI':"Pisa", 'PT':"Prato", 'SI':"Siena"},
	'Trentino Alto Adige'  :{'BZ':"Bolzano", 'TN':"Trento"},
	'Umbria'               :{'PG':"Perugia", 'TR':"Terni"},
	'Valle d\'Aosta'       :{'AO':"Aosta"},
	'Veneto'               :{'BL':"Belluno", 'PD':"Padova", 'RO':"Rovigo", 'TV':"Treviso", 'VE':"Venezia", 'VR':"Verona", 'VI':"Vicenza"}
}, []
FatturaPA_XMLns = {
	'xmlns:ds'			:"http://www.w3.org/2000/09/xmldsig#",
	'xmlns:p'			:"http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2",
	'xmlns:xsi'			:"http://www.w3.org/2001/XMLSchema-instance",
	'xsi:schemaLocation':"http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2/Schema_del_file_xml_FatturaPA_versione_1.2.xsd"
}
FormatoTrasmissione_t = { 'FPA12':"verso PA", 'FPR12':"verso privati"	}
CausalePagamento_t = frozenset(['A','B','C','D','E','F','G','H','I','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','L1','M1','O1','V1'])
TipoSconto_t = { 'sconto':"SC", 'maggiorazione':"MG"	}
Art73_t = frozenset(["SI"])	# documento emesso secondo modalità e temini stabiliti con DM ai sensi art. 74 DPR 633/72

# Copied from Documentazione valida a partire dal 1 ottobre 2020
# Rappresentazione tabellare del tracciato fattura ordinaria - excel
TIPO_CASSA = {
    #TipoCassa_t = {
	'TC01': "Cassa nazionale previdenza e assistenza avvocati e procuratori legali",
	'TC02': "Cassa previdenza dottori commercialisti",
	'TC03': "Cassa previdenza e assistenza geometri",
	'TC04': "Cassa nazionale previdenza e assistenza ingegneri e architetti liberi professionisti",
	'TC05': "Cassa nazionale del notariato",
	'TC06': "Cassa nazionale previdenza e assistenza ragionieri e periti commerciali",
	'TC07': "Ente nazionale assistenza agenti e rappresentanti di commercio (ENASARCO)",
	'TC08': "Ente nazionale previdenza e assistenza consulenti del lavoro (ENPACL)",
	'TC09': "Ente nazionale previdenza e assistenza medici (ENPAM)",
	'TC10': "Ente nazionale previdenza e assistenza farmacisti (ENPAF)",
	'TC11': "Ente nazionale previdenza e assistenza veterinari (ENPAV)",
	'TC12': "Ente nazionale previdenza e assistenza impiegati dell'agricoltura (ENPAIA)",
	'TC13': "Fondo previdenza impiegati imprese di spedizione e agenzie marittime",
	'TC14': "Istituto nazionale previdenza giornalisti italiani (INPGI)",
	'TC15': "Opera nazionale assistenza orfani sanitari italiani (ONAOSI)",
	'TC16': "Cassa autonoma assistenza integrativa giornalisti italiani (CASAGIT)",
	'TC17': "Ente previdenza periti industriali e periti industriali laureati (EPPI)",
	'TC18': "Ente previdenza e assistenza pluricategoriale (EPAP)",
	'TC19': "Ente nazionale previdenza e assistenza biologi (ENPAB)",
	'TC20': "Ente nazionale previdenza e assistenza professione infermieristica (ENPAPI)",
	'TC21': "Ente nazionale previdenza e assistenza psicologi (ENPAP)",
	'TC22': "INPS"
}

# see pages 1 to 25 for the PDF document
# GUIDA ALLA COMPILAZIONE DELLE FATTURE ELETTRONICHE E DELL’ESTEROMETRO
# from AdE (Agenzia Delle Entrate), version 1.6 - 2022/02/04
# https://www.agenziaentrate.gov.it/portale/documents/20143/451259/Guida_compilazione-FE_2021_07_07.pdf/e6fcdd04-a7bd-e6f2-ced4-cac04403a768
TIPO_DOCUMENTO = {
    #Documento_t = {
	'TD01': "Fattura",
	'TD02': "Acconto/anticipo su fattura",
	'TD03': "Acconto/anticipo su parcella",
	'TD04': "Nota di credito",
	'TD05': "Nota di debito",
	'TD06': "Parcella",
	'TD16': "Integrazione fattura reverse charge interno",
	'TD17': "Integrazione/autofattura per acquisto servizi da estero (ex art.17 comma 2 DPR 633/1978",
	'TD18': "Integrazione per acquisto beni intracomunitari (ex art.46 DL 331/1993)",
	'TD19': "Integrazione/autofattura per acquisto beni (ex art.17 comma 2 DPR 633/1972)",
	'TD20': "Autofattura denuncia",	#per regolarizzazione e integrazione delle fatture (art.6 comma 7 DLgs 471/1997 o art.46 comma 5 DL 331/1993)",
	'TD21': "Autofattura per splafonamento",
	'TD22': "Estrazione beni da Deposito IVA",
	'TD23': "Estrazione beni da Deposito IVA con versamento IVA",
	'TD24': "Fattura differita (art.21 comma 4 lett.a)",	#ovvero fattura differita di beni collegati a DDT o di servizi collegati a ideona documentazione di prova dell'effettuazione per le prestazioni di servizio)",
	'TD25': "Fattura differita (art.21 comma 4 terzo § lett.b)",	#triangolari interne, ossia cessione di beni effettuata dal cessionario verso un terzo per il tramite del cedente)",
	'TD26': "Cessione di beni ammortizzabili e per passaggi interni (art.36 DPR 633/1972)",
	'TD27': "Fattura per autoconsumo o per cessioni gratuite senza rivalsa",
}

# Copied from Documentazione valida a partire dal 1 ottobre 2020
# Rappresentazione tabellare del tracciato fattura ordinaria - excel
TIPO_RITENUTA = (
    #Ritenuta_t1 = {
	'RT01': "Ritenuta persone fisiche",
	'RT02': "Ritenuta persone giuridiche",
	'RT03': "Contributo INPS",
	'RT04': "Contributo ENASARCO",
	'RT05': "Contributo ENPAM",
	'RT06': "altro contributo previdenziale"
}


Ritenuta_t2 = {	'SI':"Cessione/prestazione soggetta a ritenuta"	}
SoggettoEmittente_t = {	'CC':"Cessionario / committente", 'TZ':"Terzo"	}
RegimeFiscale_t = {
	'RF01':"Regime ordinario",
	'RF02':"Regime dei contribuenti minimi (art.1 c.96-117, L.244/2007)",
	#'RF03':"Nuove iniziative produttive (art.13 L.388/0)",
	'RF04':"Agricoltura e attività connesse e pesca (artt.34 e 34bis)",
	'RF05':"Vendita sali e tabacchi (art.74 c.1)",
	'RF06':"Commercio dei fiammiferi (art.74 c.1)",
	'RF07':"Editoria (art.74 c.1)",
	'RF08':"Gestione di servizi di telefonia pubblica (art.74 c.1)",
	'RF09':"Rivendita di documenti di trasporto pubblico e di sosta (art.74 c.1)",
	'RF10':"Intrattenimenti, giochi e altre attività di cui alla tariffa allegata al DPR 640/72 (art.74 c.6)",
	'RF11':"Agenzie di viaggi e turismo (art.74ter)",
	'RF12':"Agriturismo (art.5 c.2, L.413/1991)",
	'RF13':"Vendite a domicilio (art.25bis c.6, DPR 600/1973)",
	'RF14':"Rivendita di beni usati, di oggetti	d’arte, d’antiquariato o da collezione (art.36, DL 41/1995)",
	'RF15':"Agenzie di vendite all’asta di oggetti d’arte, antiquariato o da collezione (art.40bis, DL 41/1995)",
	'RF16':"IVA per cassa P.A. (art.6 c.5)",
	'RF17':"IVA per cassa (art.32bis, DL 83/2012)",
	'RF19':"Regime forfettario (art.1 comma 54-89 L.190/2014)",
	'RF18':"altro"
}


# Copied from Documentazione valida a partire dal 1 ottobre 2020
# Rappresentazione tabellare del tracciato fattura ordinaria - excel
REGIME_FISCALE_IVA = {
    #RegimeFiscaleIVA_t = {
	"RF01": 22.0,  # Ordinario
    "RF02": 20.0,  # Contribuenti minimi (art.1, c.96-117, L. 244/07)
    "RF04": 10.0,  # Agricoltura e attività connesse e pesca (artt.34 e 34-bis, DPR 633/72)
    "RF05":  0.0,  # Vendita sali e tabacchi (art.74, c.1, DPR. 633/72)
    "RF06":  0.0,  # Commercio fiammiferi (art.74, c.1, DPR  633/72)
    "RF07":  0.0,  # Editoria (art.74, c.1, DPR  633/72)
    "RF08":  0.0,  # Gestione servizi telefonia pubblica (art.74, c.1, DPR 633/72)
    "RF09":  0.0,  # Rivendita documenti di trasporto pubblico e di sosta (art.74, c.1, DPR  633/72)
    "RF10":  0.0,  # Intrattenimenti, giochi e altre attività di cui alla tariffa allegata al DPR 640/72 (art.74, c.6, DPR 633/72)
    "RF11":  0.0,  # Agenzie viaggi e turismo (art.74-ter, DPR 633/72)
    "RF12":  0.0,  # Agriturismo (art.5, c.2, L. 413/91)
    "RF13":  0.0,  # Vendite a domicilio (art.25-bis, c.6, DPR  600/73)
    "RF14":  0.0,  # Rivendita beni usati, oggetti d’arte, d’antiquariato o da collezione (art.36, DL 41/95)
    "RF15":  0.0,  # Agenzie di vendite all’asta di oggetti d’arte, antiquariato o da collezione (art.40-bis, DL 41/95)
    "RF16":  0.0,  # IVA per cassa P.A. (art.6, c.5, DPR 633/72)
    "RF17":  0.0,  # IVA per cassa (art. 32-bis, DL 83/2012)
    "RF18":  0.0,  # Altro
    "RF19":  0.0,  # Regime forfettario (art.1, c.54-89, L. 190/2014)
}

CondizioniPagamento_t = {	'TP01':"pagamento a rate", 'TP02':"pagamento completo", 'TP03':"anticipo"	}

# Copied from Documentazione valida a partire dal 1 ottobre 2020
# Rappresentazione tabellare del tracciato fattura ordinaria - excel
MODALITA_PAGAMENTO = {}
    #ModalitaPagamento_t = {
	'MP01': "contanti",
	'MP02': "assegno",
	'MP03': "assegno circolare",
	'MP04': "contanti presso Tesoreria",
	'MP05': "bonifico",
	'MP06': "vaglia cambiario",
	'MP07': "bollettino bancario",
	'MP08': "carta di pagamento",
	'MP09': "RID",
	'MP10': "RID utenze",
	'MP11': "RID veloce",
	'MP12': "RIBA",
	'MP13': "MAV",
	'MP14': "quietanza erario",
	'MP15': "giroconto su conti di contabilità speciale",
	'MP16': "domiciliazione bancaria",
	'MP17': "domiciliazione postale",
	'MP18': "bollettino di c/c postale", 
	'MP19': "SEPA Direct Debit",
	'MP20': "SEPA Direct Debit CORE",
	'MP21': "SEPA Direct Debit B2B",
	'MP22': "Trattenuta su somme già riscosse",
	'MP23': "PagoPA",
}

EsigibilitaIVA_t = {	'D':"esibilità differita", 'I':"esigibilità immediata", 'S':"scissione dei pagamenti"	}
Natura_t = {
	'':"Standard (nessuna ulteriore natura)", 
    'N1':"Esclusa ex art.15", 
    'N4':"Esente", 
    'N5':"Regime del margine / IVA non esposta in fattura",
	'N7':"IVA assolta in altro stato UE (vendite a distanza ex art.40 commi 3 e 4 e art.41 comma 1 lett.b, DL 331/93; prestazione di servizi di telecomunicazioni, teleradiodiffusione ed elettronici ex art.7-sexies lett. f,g, DPR 633/72 e art.74-sexies, DPR 633/72)",
	'N2':"Non soggetta [...]", 
    'N3':"Non imponibile [...]", 
    'N6':"Inversione contabile (reverse charge)[...]",
}
_nature_esenti_IVA_ritenuta = frozenset([ 'N2','N3','N4' ])
RefNormativo_t = {
	'N2':{	# NON SOGGETTE
		'N2.1':"Non soggetta (artt. da 7 a 7septies DPR 633/1972)",
		'N2.2':"Non soggetta (altri casi)"	},
	'N3':{	# NON IMPONIBILI
		'N3.1':"Non imponibile (esportazione)", 
		'N3.2':"Non imponibile (cessione intracomunitaria)", 
		'N3.3':"Non imponibile (cessione verso San Marino)", 
		'N3.4':"Non imponibile (assimilata a cessione all'esportazione)", 
		'N3.5':"Non imponibile (a seguito di dichiarazione di intento)", 
		'N3.6':"Non imponibile (altra operazione che non concorre alla formazione del plafond)"	},
	'N6':{	# INVERSIONE CONTABILE ('REVERSE CHARGE')
		'N6.1':"Inversione contabile (cessione di rottami e altri materiali di recupero)", 
		'N6.2':"Inversione contabile (cessione di oro e argento puro)", 
		'N6.3':"Inversione contabile (subappalto nel settore edile)", 
		'N6.4':"Inversione contabile (cessione di fabbricati)", 
		'N6.5':"Inversione contabile (cessione di telefoni cellulari)", 
		'N6.6':"Inversione contabile (cessione di prodotti elettronici)", 
		'N6.7':"Inversione contabile (prestazioni comparto edile e settori connessi)", 
		'N6.8':"Inversione contabile (operazioni settore energetico)", 
		'N6.9':"Inversione contabile (altri casi)"	}
}

# see table at page 26 for the PDF document
# GUIDA ALLA COMPILAZIONE DELLE FATTURE ELETTRONICHE E DELL’ESTEROMETRO
# from AdE (Agenzia Delle Entrate), version 1.6 - 2022/02/04
# https://www.agenziaentrate.gov.it/portale/documents/20143/451259/Guida_compilazione-FE_2021_07_07.pdf/e6fcdd04-a7bd-e6f2-ced4-cac04403a768
# see also:
# - https://agenziaentrate.gov.it/portale/documents/20143/296703/Variazioni+alle+specifiche+tecniche+fatture+elettroniche2021-07-02.pdf  # noqa
# - https://www.agenziaentrate.gov.it/portale/web/guest/schede/comunicazioni/fatture-e-corrispettivi/faq-fe/risposte-alle-domande-piu-frequenti-categoria/compilazione-della-fattura-elettronica  # noqa
NATURA_IVA = (
    "N1",
    "N2",
    "N2.1",  # non soggette ad IVA ai sensi degli artt. da 7 a 7-septies del D.P.R. n. 633/72
    "N2.2",  # non soggette - altri casi
    "N3",
    "N3.1",  # non imponibili - esportazioni
    "N3.2",  # non imponibili - cessioni intracomunitarie
    "N3.3",  # non imponibili - cessioni verso San Marino
    "N3.4",  # non imponibili - operazioni assimilate alle cessioni all'esportazione
    "N3.5",  # non imponibili - a seguito di dichiarazioni d'intento
    "N3.6",  # non imponibili - altre operazioni
    "N4",
    "N5",
    "N6",
    "N6.1",  # inversione contabile - cessione di rottami e altri materiali di recupero
    "N6.2",  # inversione contabile – cessione di oro e argento ai sensi della
             #                        legge 7/2000 nonché di oreficeria usata ad OPO
    "N6.3",  # inversione contabile - subappalto nel settore edile
    "N6.4",  # inversione contabile - cessione di fabbricati
    "N6.5",  # inversione contabile - cessione di telefoni cellulari
    "N6.6",  # inversione contabile - cessione di prodotti elettronici
    "N6.7",  # inversione contabile - prestazioni comparto edile e settori connessi
    "N6.8",  # inversione contabile - operazioni settore energetico
    "N6.9",  # inversione contabile - altri casi
    "N7",
)

SocioUnico_t = {
    'SU':"socio unico", 
    'SM':"più soci"	
}
StatoLiquidazione_t = {
    'LS':"in liquidazione",
    'LN':"non in liquidazione"
}
TipoCessionePrestazione_t = {
    'SC':"Sconto", 
    'PR':"Premio", 
    'AB':"Abbuono", 
    'AC':"Spesa accessoria"
}
