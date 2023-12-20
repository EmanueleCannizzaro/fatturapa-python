#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##########################################################
#  FatturaPA-python 1.3.1                                #
#--------------------------------------------------------#
#   Quick generation of FatturaPA eInvoice XML files !   #
#--------------------------------------------------------#
#    GNU (GPL) 2019-2021 Walter Arrighetti               #
#    coding by: Ing. Walter Arrighetti, PhC, CISSP CCSP  #
#  < https://github.com/walter-arrighetti/pyFatturaPA >  #
#                                                        #
##########################################################
import datetime
import os.path
import json
import sys
import re


def check_config():
	try:	
    	os.path.exists(CONF_FILE)
	except:	
    	return create_config()
	return True

def enter_org_data():
	answer = XML_input("P.IVA individuale? Sì/[N]o ")
	if answer and answer.lower()[0]=='s':	orgname = tuple([XML_input("Nome:  "), XML_input(str("Cognome:  "))])
	else:	orgname = XML_input("Ragione sociale:  ")
	addr = {	'country':"", 'zip':"", 'addr':None, 'prov':None, 'muni':None	}
	while len(addr['country'])!=2:
		addr['country'] = XML_input("Sigla a 2 caratteri della nazione (premi [Invio] per Italia):  ").upper()
		if not addr['country']:	addr['country'] = "IT"
	if addr['country']=="IT":
		while not (len(addr['zip'])==5 and addr['zip'].isnumeric()):
			addr['zip'] = XML_input("CAP (5 cifre):  ").upper()
		while not addr['prov']:
			prov = XML_input("Provincia (sigla a 2 cifre):  ").upper()
			if prov in PROVINCES:	addr['prov'] = prov
		while not addr['muni']:
			comune = XML_input("Comune (nome completo):  ")
			if comune:	addr['muni'] = comune
	else:
		while not addr['zip']:
			addr['zip'] = XML_input("Zip code:  ").upper()
		print("ATTENZIONE!: Questa fattura andrà dichiarata nell'\"Esterometro\".\n")
	while not addr['addr']:
		addr['addr'] = XML_input("Indirizzo (via/piazza/..., *senza* numero civico):  ")
	addr['#'] = XML_input("Numero civico (se applicabile):  ")
	for key in ['prov','#']:
		if not addr[key]:	del addr[key]
	VATnum = None
	if addr['country']=="IT":
		while not VATnum:
			VATc, VATnum = "IT", XML_input("Numero di Partita IVA:  ")
	elif addr['country'].lower() in EU_MemberStates.keys():
		VATc = addr['country']
		while not VATnum:
			VATnum = XML_input("Numero VAT o TIN (obbligatorio in Comunità Europea):  ")
	else:
		VATc, VATnum = addr['country'], XML_input("Numero VAT o TIN (facoltativo al di fuori della CE):  ")
		if not VATnum:
			VATc, VATnum = "OO", "99999999999"
	CF = None
	while VATc=="IT" and CF==None:
		CF = XML_input("Codice Fiscale (se applicabile):  ")
		if CF=="":	break
		elif CF and CFre.match(CF) or (10<len(CF)<17 and CF.isalnum()):	break
		CF = None
	email = None
	while email==None:
		email = XML_input("Indirizzo email (obbligatoriamente PEC se in Italia):  ")
		if email=="" or emailre.match(email):	break
		else:	email = None
	if addr['country']=="IT":
		if email:
			Id = "0000000"
			print("Indirizzo PEC specificato: identificativo unico impostato a '0000000'.")
		else:
			if addr['country']=="IT":	Id = None
			while not Id:	Id = XML_input("Identificativo Unico (se applicabile):  ").upper()
	else:	Id = "XXXXXXX"
	if not Id:	Id = None
	while True:
		iban = XML_input("Inserire codice IBAN ove effettuare prioritariamente i pagamenti ([Invio] per saltare): ").strip()
		if not iban:	break
		if IBANre.match(iban.strip()):
			iban = iban.upper().replace(' ','').replace('-','')
			break
	retdict = {	'name':orgname, 'VAT#':(VATc,VATnum), 'CF':CF, 'Id':Id, 'addr':addr, 'email':email, 'IBAN':iban }
	for key in ['CF','email','IBAN']:
		if not retdict[key]:	del retdict[key]
	return retdict


def parse_config():
	try:	clients = json.load(open(CONF_FILE,"r"))
	except:	return False, False
	if "USER" not in clients.keys():	return False, False
	USER = clients["USER"]
	del clients["USER"]
	for org in clients.keys():
		if type(org)!=type(u'') or len(org)!=3 or not org.isalnum():	return False, False
	return (USER, clients)


def pretty_dict_print(dictname, D):
	return json.dumps({dictname:D}, indent='\t')


def write_config(user, clients, append):
	if append:	mod = 'a'
	else:	mod = 'w'
	try:	conf = open(CONF_FILE,mod)
	except:
		print(" * ERROR!: Unable to create/modify database \"%s\"."%os.path.abspath(CONF_GILE))
		sys.exit(-8)
	clients["USER"] = user
	conf.write(json.dumps(clients, indent='\t'))
	conf.close()



def add_company():
	if not os.path.exists(CONF_FILE):
		print("ERROR!: Il file di configurazione di pyFatturaPA (%s) non è stato trovato. L'utente va prima inizializzato."%CONF_FILE)
		sys.exit(-2)
	user, clients = parse_config()
	if not user:	return False
	orgname = ""
	while len(orgname)!=3 or not orgname.isalnum() or orgname in clients.keys():
		orgname = XML_input("Sigla di 3 caratteri alfanumerici per la nuova organizzazione:  ").upper()
	new_client = enter_org_data()
	clients[orgname] = new_client
	write_config(user, clients, append=False)


def create_config():
	print("Inizializzazione del database: inserimento dati dell'UTENTE.")
	user = enter_org_data()
	answ = None
	user['RegimeFiscale'] = _enum_selection(RegimeFiscale_t, "regime fiscale (ex DPR 633/1972)", 'RF01')
	while not answ:
		answ = XML_input("L'utente (in qualità di cedente/prestatore) è soggetto a ritenuta? [S]ì/No ")
		if (not answ) or answ[0].lower()=="s":
			answ = "Sì"
			user['ritenuta'] = {'aliquota':None, 'causale':None}
			if type(user['name'])==type(""):	user['ritenuta']['tipo'] = 'RT02'
			else:	user['ritenuta']['tipo'] = 'RT01'
			while not user['ritenuta']['aliquota'] or user['ritenuta']['aliquota']<0 or user['ritenuta']['aliquota']>100:
				aliq = XML_input("Inserire %% aliquota della ritenuta (e.g. \"%.2f\"):  "%VAT_DEFAULT)
				if aliq.isnumeric():	user['ritenuta']['aliquota'] = eval(aliq)
				else:	user['ritenuta']['aliquota'] = VAT_DEFAULT
			while not user['ritenuta']['causale'] or user['ritenuta']['causale'] not in CausalePagamento_t:
				user['ritenuta']['causale'] = XML_input("Inserire sigla della causale di pagamento ('A...Z' ovvero 'L|M|O|V1':  ").upper()
		elif answ and answ[0].lower()=="n":
			answ = None;	break
		else: answ = None;	continue
	answ = None
	while not answ:
		answ = XML_input("Si è iscritti ad una cassa previdenziale? [S]ì/No ")
		if (not answ) or answ[0].lower()=="s":
			answ = "Sì"
			user['cassa'] = {
				'tipo':_enum_selection(TipoCassa_t, "cassa di appartenenza", 'TC22'),
				'aliquota':eval(XML_input("Indicare l'aliquota contributo cassa:  ")),
				'IVA':VAT_DEFAULT	# Questa linea verrà sostiuita da un lookup automatico sul RegimeFiscaleIVA_t in base al valore di user['RegimeFiscale']
			}
		elif answ and answ[0].lower()=="n":
			del user['cassa']
			answ = None;	break
		else: answ = None;	continue
	iban = None
	write_config(user, {}, append=False)


def FatturaPA_write(filename, lines, debug_len=False):
	payload_len, file_len = 0, 0
	with open(filename,'w') as f:
		import os
		print("Creazione del file FatturaPA \"%s\"....."%filename)
		for line in lines:
			payload_len += len(line) + len(os.linesep)
			file_len += f.write(line+'\n')
	if debug_len:
		print("File length:  precomp_payload=%d\tI/O=%d"%(payload_len,file_len))
	sys.exit(0)


def FatturaPA_assemble(user, client, data):
	global FatturaPA_XMLns
	_FatturaElettronica_XMLroot = '<p:FatturaElettronica versione="%s"'%data['FormatoTrasmissione']
	for key in sorted(FatturaPA_XMLns.keys()):
		_FatturaElettronica_XMLroot += ' %s="%s"'%(key,FatturaPA_XMLns[key])
	_FatturaElettronica_XMLroot += '>'
	#####	FATTURA ELETTRONICA HEADER
	F = [
		'<?xml version="1.0" encoding="UTF-8" ?>',
		_FatturaElettronica_XMLroot,
		'\t<FatturaElettronicaHeader>',
		'\t\t<DatiTrasmissione>',
		'\t\t\t<IdTrasmittente>',
		'\t\t\t\t<IdPaese>%s</IdPaese>'%user['VAT#'][0],
		'\t\t\t\t<IdCodice>%s</IdCodice>'%user['CF'],
		'\t\t\t</IdTrasmittente>',
		'\t\t\t<ProgressivoInvio>%s</ProgressivoInvio>'%data['ProgressivoInvio'],
		'\t\t\t<FormatoTrasmissione>%s</FormatoTrasmissione>'%data['FormatoTrasmissione'],
		'\t\t\t<CodiceDestinatario>%s</CodiceDestinatario>'%client['Id']
	]
	if ('email' in client.keys()) and client['Id']=="0000000":	F.append('\t\t\t<PECDestinatario>%s</PECDestinatario>'%client['email'])
	F.extend([
		'\t\t</DatiTrasmissione>',
		'\t\t<CedentePrestatore>',
		'\t\t\t<DatiAnagrafici>',
		'\t\t\t\t<IdFiscaleIVA>',
		'\t\t\t\t\t<IdPaese>%s</IdPaese>'%user['VAT#'][0],
		'\t\t\t\t\t<IdCodice>%s</IdCodice>'%user['VAT#'][1],
		'\t\t\t\t</IdFiscaleIVA>'])
	if 'CF' in user.keys():	F.append('\t\t\t\t<CodiceFiscale>%s</CodiceFiscale>'%user['CF'])
	F.append('\t\t\t\t<Anagrafica>')
	if type(user['name'])==type(""):	F.append('\t\t\t\t\t<Denominazione>%s</Denominazione>'%user['name'])
	else:	F.extend(['\t\t\t\t\t<Nome>%s</Nome>'%user['name'][0],'\t\t\t\t\t<Cognome>%s</Cognome>'%user['name'][1]])
	F.extend([
		'\t\t\t\t</Anagrafica>',
		'\t\t\t\t<RegimeFiscale>%s</RegimeFiscale>'%user['RegimeFiscale'],
		'\t\t\t</DatiAnagrafici>',
		'\t\t\t<Sede>',
		'\t\t\t\t<Indirizzo>%s</Indirizzo>'%user['addr']['addr']])
	if '#' in user['addr'].keys():	F.append('\t\t\t\t<NumeroCivico>%s</NumeroCivico>'%user['addr']['#'])
	if 'zip' in user['addr']:	F.append('\t\t\t\t<CAP>%s</CAP>'%user['addr']['zip'])
	if 'muni' in user['addr']:	F.append('\t\t\t\t<Comune>%s</Comune>'%user['addr']['muni'])
	if 'prov' in user['addr']:	F.append('\t\t\t\t<Provincia>%s</Provincia>'%user['addr']['prov'])
	F.extend([
		'\t\t\t\t<Nazione>%s</Nazione>'%user['addr']['country'],
		'\t\t\t</Sede>',
		'\t\t</CedentePrestatore>',
		'\t\t<CessionarioCommittente>',
		'\t\t\t<DatiAnagrafici>'])
	if 'VAT#' in client.keys():	F.extend([
		'\t\t\t\t<IdFiscaleIVA>',
		'\t\t\t\t\t<IdPaese>%s</IdPaese>'%client['VAT#'][0],
		'\t\t\t\t\t<IdCodice>%s</IdCodice>'%client['VAT#'][1],
		'\t\t\t\t</IdFiscaleIVA>'])
	if 'CF' in client.keys():	F.append('\t\t\t\t<CodiceFiscale>%s</CodiceFiscale>'%client['CF'])
	F.append('\t\t\t\t<Anagrafica>')
	if type(client['name'])==type(""):	F.append('\t\t\t\t\t<Denominazione>%s</Denominazione>'%client['name'])
	else:	F.extend(['\t\t\t\t\t<Nome>%s</Nome>'%client['name'][0],'\t\t\t\t\t<Cognome>%s</Cognome>'%client['name'][1]])
	F.extend([
		'\t\t\t\t</Anagrafica>',
		'\t\t\t</DatiAnagrafici>',
		'\t\t\t<Sede>',
		'\t\t\t\t<Indirizzo>%s</Indirizzo>'%client['addr']['addr']])
	if '#' in client['addr'].keys():	F.append('\t\t\t\t<NumeroCivico>%s</NumeroCivico>'%client['addr']['#'])
	if 'zip' in client['addr']:	F.append('\t\t\t\t<CAP>%s</CAP>'%client['addr']['zip'])
	if 'muni' in client['addr']:	F.append('\t\t\t\t<Comune>%s</Comune>'%client['addr']['muni'])
	if 'prov' in client['addr']:	F.append('\t\t\t\t<Provincia>%s</Provincia>'%client['addr']['prov'])
	F.extend([
		'\t\t\t\t<Nazione>%s</Nazione>'%client['addr']['country'],
		'\t\t\t</Sede>',
		'\t\t</CessionarioCommittente>',
		'\t</FatturaElettronicaHeader>'])
	#####	FATTURA ELETTRONICA BODY
	F.extend([
		'\t<FatturaElettronicaBody>',
		'\t\t<DatiGenerali>',
		'\t\t\t<DatiGeneraliDocumento>',
		'\t\t\t\t<TipoDocumento>%s</TipoDocumento>'%data['TipoDocumento'],
		'\t\t\t\t<Divisa>%s</Divisa>'%data['Divisa'],
		'\t\t\t\t<Data>%s</Data>'%data['Data'].strftime("%Y-%m-%d"),
		'\t\t\t\t<Numero>%s</Numero>'%data['num']])
	if 'ritenuta' in user.keys() and 'ritenuta' in user.keys():
		F.extend([
			'\t\t\t\t<DatiRitenuta>',
			'\t\t\t\t\t<TipoRitenuta>%s</TipoRitenuta>'%user['ritenuta']['tipo'],
			'\t\t\t\t\t<ImportoRitenuta>%.02f</ImportoRitenuta>'%abs(data['ritenuta']['importo']),
			'\t\t\t\t\t<AliquotaRitenuta>%.02f</AliquotaRitenuta>'%user['ritenuta']['aliquota'],
			'\t\t\t\t\t<CausalePagamento>%s</CausalePagamento>'%user['ritenuta']['causale'],
			'\t\t\t\t</DatiRitenuta>'])
	if 'cassa' in user.keys() and 'cassa' in user.keys():
		F.extend([
			'\t\t\t\t<DatiCassaPrevidenziale>',
			'\t\t\t\t\t<TipoCassa>%s</TipoCassa>'%user['cassa']['tipo'],
			'\t\t\t\t\t<AlCassa>%.02f</AlCassa>'%user['cassa']['aliquota'],
			'\t\t\t\t\t<ImportoContributoCassa>%.02f</ImportoContributoCassa>'%data['cassa']['importo'],
			'\t\t\t\t\t<ImponibileCassa>%.02f</ImponibileCassa>'%data['cassa']['imponibile'],
			'\t\t\t\t\t<AliquotaIVA>%.02f</AliquotaIVA>'%user['cassa']['IVA']])
		if 'natura' in data.keys():	F.append('\t\t\t\t\t<Natura>%s</Natura>'%data['natura'][0])
		F.append('\t\t\t\t</DatiCassaPrevidenziale>')
	if 'causale' in data.keys():
		for k in range(0,len(data['causale']),200):
			F.append('\t\t\t\t<Causale>%s</Causale>'%data['causale'][200*k:200*(k+1)])
	F.append('\t\t\t</DatiGeneraliDocumento>')
	if 'ref' in data.keys():
		if 'Id' in data['ref'].keys():
			F.append('\t\t\t<DatiOrdineAcquisto>')
			if '##' in data['ref'].keys():
				for l in sorted(data['ref']['##']):
					F.append('\t\t\t\t<RiferimentoNumeroLinea>%d</RiferimentoNumeroLinea>'%l)
			F.append('\t\t\t\t<IdDocumento>%s</IdDocumento>'%data['ref']['Id']),
			F.append('\t\t\t</DatiOrdineAcquisto>')
		for reftype in ['Contratto','Convenzione','Ricezione','FattureCollegate']:
			if reftype in data['ref'].keys():
				F.append('\t\t\t\t<Dati%s>%s</Dati%s>'%(reftype,data['ref'][reftype],reftype))
	F.extend([
		'\t\t</DatiGenerali>',
		'\t\t<DatiBeniServizi>'])
	lines = sorted([data['#'][l]['linea'] for l in range(len(data['#']))])
	for l in lines:
		line = data['#'][l-1];
		F.append('\t\t\t<DettaglioLinee>')
		F.append('\t\t\t\t<NumeroLinea>%d</NumeroLinea>'%l)
		if 'descr' in line.keys():	F.append('\t\t\t\t<Descrizione>%s</Descrizione>'%line['descr'][:1000])
		if 'period' in line.keys():	F.extend([
			'\t\t\t\t<DataInizioPeriodo>%s</DataInzioPeriodo>'%line['period'][0].strftime("%Y-%m-%d"),
			'\t\t\t\t<DataFinePeriodo>%s</DataFinePeriodo>'%line['period'][1].strftime("%Y-%m-%d")])
		if 'Qty' in line.keys():
			F.append('\t\t\t\t<Quantita>%.02f</Quantita>'%line['Qty'])
			if 'unit' in line.keys():	F.append('\t\t\t\t<UnitaMisura>%s</UnitaMisura>'%line['unit'])
		F.extend([
			'\t\t\t\t<PrezzoUnitario>%.02f</PrezzoUnitario>'%line['price'],
			'\t\t\t\t<PrezzoTotale>%.02f</PrezzoTotale>'%line['total'],
			'\t\t\t\t<AliquotaIVA>%.02f</AliquotaIVA>'%data['total']['aliquota']
			])
		if 'ritenuta' in user.keys():
			if 'natura' in data.keys():
				for exent in _nature_esenti_IVA_ritenuta:
					if data['natura'][0].startswith(exent):	pass
			else:	F.append('\t\t\t\t<Ritenuta>%s</Ritenuta>'%'SI')
		if 'natura' in data.keys():	F.append('\t\t\t\t<Natura>%s</Natura>'%data['natura'][0])
		F.append('\t\t\t</DettaglioLinee>')
	F.extend([
		'\t\t\t<DatiRiepilogo>',
		'\t\t\t\t<AliquotaIVA>%.02f</AliquotaIVA>'%data['total']['aliquota']])
	if 'natura' in data.keys():
		F.append('\t\t\t\t<Natura>%s</Natura>'%data['natura'][0])
	F.extend([
		'\t\t\t\t<ImponibileImporto>%.02f</ImponibileImporto>'%data['total']['imponibile'],
		'\t\t\t\t<Imposta>%.02f</Imposta>'%data['total']['imposta']])
	if 'natura' in data.keys():
		F.append('\t\t\t\t<RiferimentoNormativo>%s</RiferimentoNormativo>'%data['natura'][1]),
	if data['total']['aliquota'] != 0.:
		F.append('\t\t\t\t<EsigibilitaIVA>%s</EsigibilitaIVA>'%data['EsigibilitaIVA']),
	F.extend([
		'\t\t\t</DatiRiepilogo>',
		'\t\t</DatiBeniServizi>'])
	if 'pagamento' in data.keys():
		F.extend([
			'\t\t<DatiPagamento>',
			'\t\t\t<CondizioniPagamento>%s</CondizioniPagamento>'%data['pagamento']['condizioni'],
			'\t\t\t<DettaglioPagamento>',
			'\t\t\t\t<ModalitaPagamento>%s</ModalitaPagamento>'%data['pagamento']['mod']])
		if 'exp' in data['pagamento'].keys():
			if type(data['pagamento']['exp'])==type(1):
				F.extend([
					'\t\t\t\t<DataRiferimentoTerminiPagamento>%s</DataRiferimentoTerminiPagamento>'%data['Data'].strftime("%Y-%m-%d"),
					'\t\t\t\t<GiorniTerminiPagamento>%d</GiorniTerminiPagamento>'%data['pagamento']['exp']])
			elif data['pagamento']['mod'] in ['TP01']:
				F.append('\t\t\t\t<DataScadenzaPagamento>%s</DataScadenzaPagamento>'%data['pagamento']['exp'].strftime("%Y-%m-%d"))
		F.append('\t\t\t\t<ImportoPagamento>%.02f</ImportoPagamento>'%data['total']['TOTALE'])
		if 'IBAN' in data['pagamento'].keys():
			F.append('\t\t\t\t<IBAN>%s</IBAN>'%data['pagamento']['IBAN'])
		F.extend([
			'\t\t\t</DettaglioPagamento>',
			'\t\t</DatiPagamento>'])
	F.extend([
		'\t</FatturaElettronicaBody>',
		'</p:FatturaElettronica>'])
	for n in range(len(F)):	F[n] = str(F[n])
	if data['num'].isdigit() and int(data['num'])>0 and data['num'][0]!='0':
		FatturaPAid = '%04d'%int(data['num'])
	else:	FatturaPAid = data['num']
	eInvoice_name = "%s%s_%s.xml"%(user["VAT#"][0],user["VAT#"][1],FatturaPAid)
	return FatturaPA_write(eInvoice_name, F)


def _enum_selection(enumtype, enumname=None, default=None):
	if not enumname:	question = "Indicare la selezione numerica sopra elencata"
	else:	question = "Prego selezionare %s"%enumname
	keys = sorted(list(enumtype.keys()))
	print()
	for n in range(1,len(keys)+1):
		print(("  %%0%dd"%len(str(len(keys))))%n + ":\t%s"%enumtype[keys[n-1]])
		if default and keys[n-1]==default:	question += " (default: %s)"%n
	question += ":  "
	answ = None
	if (default or default=='') and default in keys:
		while True:
			answ = XML_input(question)
			if not answ:	return default
			elif answ.isnumeric() and 1<=eval(answ)<=len(keys):
				return keys[eval(answ)-1]
			else:	answ = None
	else:
		while not (answ and answ.isnumeric() and 1<=eval(answ)<=len(keys)):	answ = XML_input(question)
	return keys[eval(answ)-1]


def issue_consultancy():
	user, clients = parse_config()
	ritenuta = 'ritenuta' in user.keys()
	data = {}
	if not user:
		print(" * ERRORE!: Database senza dati personali, ovvero il file \"%s\" deve trovarsi nella stessa cartella di \"%s\"."%(CONF_FILE,sys.argv[0]))
		sys.exit(-3)
	if not clients:
		print(" * ERRORE!: Database dei clienti vuoto. Deve essere inserito almeno un cliente tramite l'argomento 'fornitore'.")
		sys.exit(-4)
	org = XML_input("Inserire la sigla identificativa (3 caratteri) del cliente nel database:  ").upper()
	if org not in clients.keys():
		print(" * ERRORE!: Cliente '%s' non trovato nel database."%org)
		sys.exit(-5)
	client = clients[org];	del clients
	data['FormatoTrasmissione'], data['TipoDocumento'], data['num'] = 'FPR12', 'TD01', ""
	data['Divisa'], data['EsigibilitaIVA'], data['pagamento'] = "EUR", 'I', {	'condizioni':'TP02', 'mod':'MP05'	}
	data['Data'] = datetime.date.today()
	aliquotaIVA = VAT_DEFAULT
	while (not data['num']) or not data['num'].strip()[0].isalnum():
		data['num'] = XML_input("Inserire il numero identificativo (progressivo) della fattura:  ")
	data['ProgressivoInvio'] = data['num']
	answ = XML_input("Indicare il numero d'Ordine facoltativo del cessionario/committente, ovvero premere [Invio]:  ")
	if answ:	data['ref'] = { 'Id':answ	}
	data['natura'] = _enum_selection(Natura_t, "le condizioni di pagamento (premere [Invio] per confermare standard)", '')
	if not data['natura']:	del data['natura']
	else:
		if data['natura'] in _nature_esenti_IVA_ritenuta:
			aliquotaIVA, ritenuta = 0, False
		if data['natura'] in RefNormativo_t.keys():
			data['natura'] = _enum_selection(RefNormativo_t[data['natura']],"riferimento normativo")
	data['total'] = {	'aliquota':aliquotaIVA, 'subtotale':0., 'imponibile':0.		}
	while True:
		delaydays = XML_input("Giorni ammessi per il pagamento dall'emissione (premere [Invio] per nessuno):  ")
		if not delaydays:	break
		elif delaydays.isdigit() and eval(delaydays)>0:
			data['pagamento']['exp'] = eval(delaydays)
			break
	if 'IBAN' in user.keys():	data['pagamento']['IBAN'] = user['IBAN']
	else:
		while True:
			iban = XML_input("Inserire codice IBAN ove effettuare il pagamento (oppure [Invio] per saltare): ").strip()
			if not iban:	break
			if IBANre.match(iban.strip()):
				data['pagamento']['IBAN'] = iban.upper().replace(' ','').replace('-','')
				break
	data['causale'] = XML_input("Causale dell'intera fattura (max. 400 caratteri):  ")[:400]
	if not data['causale']:	del data['causale']
	data['#'], l, = [], 1
	while True:
		print("\nVOCE #%d DELLA FATTURA."%l)
		while True:
			vocestr = "Prezzo unitario della voce #%d"%l
			if l > 1:	vocestr += " ([Invio] se le voci fattura sono terminate)"
			vocestr += ":  "
			pricetmp = XML_input(vocestr)
			if pricetmp and pricetmp.isnumeric():
				price = eval(pricetmp);	break
			elif not pricetmp and l>1:	break
		if not pricetmp:	l -= 1;	break
		qty, vat = None, None
		while True:
			qtytmp = XML_input("Quantità della voce #%d  [default: 1]:  "%l)
			if qtytmp and qtytmp.isnumeric():
				qty = eval(qtytmp)
				if qty <= 0:	qty = None
				break
			elif not qtytmp:	break
		if qty:
			total = price * qty
			unit = XML_input("Unità di misura della voce #%d (premere [Invio] per nessuna):  "%l)
		else:	total, unit = price, None
		data['total']['subtotale'] += total
		descr = None
		while not descr:	descr = XML_input("Descrizione della voce #%d:  "%l)[:1000]
		line = {'linea':l,	'price':price, 'total':total, 'descr':descr	}
		if qty:
			line['Qty'] = qty
			if unit:	line['unit'] = unit
		data['#'].append( line )
		del price, vat, qty, total, descr
		l += 1
	if not data['#']:
		print(" * ERROR!: Non sono state inserite voci nella fattura (è necessaria almeno una voce).")
		sys.exit(-6)
	subtotale = data['total']['subtotale']
	####	Calcolo della Rivalsa INPS
	if 'cassa' in user.keys():
		data['total']['cassa'] = subtotale * (user['cassa']['aliquota']/100)
	else:	data['total']['imposta'] = 0
	data['cassa'] = {	'importo':data['total']['cassa'], 'imponibile':subtotale, 'aliquota':user['cassa']['aliquota']	}
	subtotale += data['cassa']['importo']
	data['total']['imponibile'] = subtotale
	####	Calcolo della Ritenuta d'Acconto
	if ritenuta:
		data['total']['ritenuta'] = -1 * subtotale * (user['ritenuta']['aliquota']/100)	# = user['ritenuta']['importo']
	else:	data['total']['ritenuta'] = 0
	data['ritenuta'] = {	'importo':data['total']['ritenuta'], 'imponibile':subtotale, 'aliquota':user['ritenuta']['aliquota']	}
	subtotale += data['total']['ritenuta']
	####	Calcolo dell'Imponibile Effettivo
	data['total']['imposta'] = data['total']['imponibile'] * (data['total']['aliquota']/100)
	####	Calcolo dell'Importo Totale
	subtotale += data['total']['imposta']
	data['total']['TOTALE'] = max(0,subtotale)
	if 'pagamento' in data.keys():
		data['pagamento']['importo'] = data['total']['TOTALE']
	return FatturaPA_assemble(user, client, data)

def issue_invoice():
	user, clients = parse_config()
	ritenuta = 'ritenuta' in user.keys()
	data = {}
	if not user:
		print(" * ERRORE!: Database senza dati personali, ovvero il file \"%s\" deve trovarsi nella stessa cartella di \"%s\"."%(CONF_FILE,sys.argv[0]))
		sys.exit(-3)
	if not clients:
		print(" * ERRORE!: Database dei clienti vuoto. Deve essere inserito almeno un cliente tramite l'argomento 'fornitore'.")
		sys.exit(-4)
	org = XML_input("Inserire la sigla identificativa (3 caratteri) del cliente nel database:  ").upper()
	if org not in clients.keys():
		print(" * ERRORE!: Cliente '%s' non trovato nel database."%org)
		sys.exit(-5)
	client = clients[org];	del clients
	data['FormatoTrasmissione'] = _enum_selection(FormatoTrasmissione_t, "tipologia di fattura", 'FPR12')
	data['TipoDocumento'] = _enum_selection(Documento_t, "tipologia di documento", 'TD01')
	data['num'] = ""
	while (not data['num']) or not data['num'].strip()[0].isalnum():
		data['num'] = XML_input("Inserire il numero identificativo (progressivo) della fattura:  ")
	data['ProgressivoInvio'], data['Divisa'] = data['num'], ""
	while not (data['Divisa'] and len(data['Divisa'])==3):
		data['Divisa'] = XML_input("Inserire la divisa (3 caratteri, default: EUR):  ")
		if not data['Divisa']:	data['Divisa'] = "EUR"
	data['Data'] = None
	while True:
		datetmp = XML_input("Data fatturazione nel formato GG-MM-AAAA (per oggi premere [Invio]):  ")
		if not datetmp:
			data['Data'] = datetime.date.today()
			break
		else:
			try:
				data['Data'] = datetime.datetime.strptime(datetmp,"%d-%m-%Y")
				break
			except:	pass
	answ = XML_input("Indicare il numero d'Ordine facoltativo del cessionario/committente, ovvero premere [Invio]:  ")
	if answ:	data['ref'] = { 'Id':answ	}
	#answer = XML_input("Il vettore della fattura è il cliente [S]ì/[N]o ")
	#if answer and answer.lower()[0]=='n':
	#	print("Inserire informazioni fiscali sul Vettore")
	#	vector = enter_org_data()
	#else:	vector = client
	data['EsigibilitaIVA'] = _enum_selection(EsigibilitaIVA_t, "esigibilità dell'IVA", 'I')
	while True:
		aliquotaIVA = XML_input("Aliquota IVA (default: %d%%; indicare \"0\" se non applcabile):  "%user['cassa']['IVA'])
		if not aliquotaIVA:	aliquotaIVA = VAT_DEFAULT;	break
		elif aliquotaIVA.isnumeric():	aliquotaIVA = eval(aliquotaIVA);	break
	data['total'] = {
		'aliquota':aliquotaIVA,
		'subtotale':0.,		# imponibile lordo(?)
		'imponibile':0.	# imponibile netto(?)
		}
	answ = None
	data['pagamento'] = {
		'condizioni':_enum_selection(CondizioniPagamento_t, "condizioni di pagamento", 'TP02'),
		'mod':_enum_selection(ModalitaPagamento_t, "modalità di pagamento", 'MP05')	
		}
	data['natura'] = _enum_selection(Natura_t, "le condizioni di pagamento (premere [Invio] per confermare standard)", '')
	if not data['natura']:	del data['natura']
	else:
		if data['natura'] in _nature_esenti_IVA_ritenuta:
			aliquotaIVA, ritenuta = 0, False
		if data['natura'] in RefNormativo_t.keys():
			data['natura'] = _enum_selection(RefNormativo_t[data['natura']],"riferimento normativo")
	if data['pagamento']['condizioni'] in ['TP01']:
		exp = None
		while not exp.isinstance(datetime.date):
			try:	exp = datetime.strptime(XML_input("Indicare la scadenza della rata (formato GG-MM-AAA):  "),"%d-%m-%Y")
			except:	continue
			data['pagamento']['exp'] = datetime.datetime.strptime(exp,"%d-%m-%Y")
	elif data['pagamento']['condizioni'] in ['TP02']:
		while True:
			delaydays = XML_input("Giorni ammessi per il pagamento dall'emissione (premere [Invio] per nessuno):  ")
			if not delaydays:	break
			elif delaydays.isdigit() and eval(delaydays)>0:
				data['pagamento']['exp'] = eval(delaydays)
				break
	if data['pagamento']['mod'] in ['MP05']:
		if 'IBAN' in user.keys():
			print("Premere [Invio] per inserire automaticamente l'IBAN trovato nelle informazioni")
			print("del cedente/prestatore, inserire un IBAN alternativo, ovvero digitare \"No\".")
			while True:
				iban = XML_input("[Invio] / cod.IBAN / [N]o: ")
				if not iban:
					data['pagamento']['IBAN'] = user['IBAN']
					break
				elif IBANre.match(iban.strip()):
					data['pagamento']['IBAN'] = iban.upper().replace(' ','').replace('-','')
					break
				elif iban.upper().startswith('N'):	break
		else:
			while True:
				iban = XML_input("Inserire codice IBAN ove effettuare il pagamento (oppure [Invio] per saltare): ").strip()
				if not iban:	break
				if IBANre.match(iban.strip()):
					data['pagamento']['IBAN'] = iban.upper().replace(' ','').replace('-','')
					break
	data['causale'] = XML_input("Causale dell'intera fattura (max. 400 caratteri):  ")[:400]
	if not data['causale']:	del data['causale']
	data['#'], l, = [], 1
	while True:
		print("\nVOCE #%d DELLA FATTURA."%l)
		while True:
			vocestr = "Prezzo unitario della voce #%d"%l
			if l > 1:	vocestr += " ([Invio] se le voci fattura sono terminate)"
			vocestr += ":  "
			pricetmp = XML_input(vocestr)
			if pricetmp and pricetmp.isnumeric():
				price = eval(pricetmp);	break
			elif not pricetmp and l>1:	break
		if not pricetmp:	l -= 1;	break
		qty, vat = None, None
		while True:
			qtytmp = XML_input("Quantità della voce #%d  [default: 1]:  "%l)
			if qtytmp and qtytmp.isnumeric():
				qty = eval(qtytmp)
				if qty <= 0:	qty = None
				break
			elif not qtytmp:	break
		if qty:
			total = price * qty
			unit = XML_input("Unità di misura della voce #%d (premere [Invio] per nessuna):  "%l)
		else:	total, unit = price, None
		data['total']['subtotale'] += total
		#	while not vat:
		#		vat = XML_input("Alitquota della voce #%d  [%%, default: %d]:  "%int(DEF_VAT))
		#		if vat.isnumeric():
		#			vat = eval(vat)
		#			if vat <= 0:	vat = None
		#		elif not vat:	vat = DEF_VAT
		#		else:	vat = None
		descr = None
		while not descr:	descr = XML_input("Descrizione della voce #%d:  "%l)[:1000]
		line = {'linea':l,	'price':price, 'total':total, 'descr':descr	}
		if qty:
			line['Qty'] = qty
			if unit:	line['unit'] = unit
		if not descr:	del line['descr']
		data['#'].append( line )
		del price, vat, qty, total, descr
		l += 1
	if not data['#']:
		print(" * ERROR!: Non sono state inserite voci nella fattura (è necessaria almeno una voce).")
		sys.exit(-6)
	subtotale = data['total']['subtotale']
	####	CALCOLO DELLA RIVALSA INPS
	if 'cassa' in user.keys():
		data['total']['cassa'] = subtotale * (user['cassa']['aliquota']/100)
	else:	data['total']['imposta'] = 0
	data['cassa'] = {	'importo':data['total']['cassa'], 'imponibile':subtotale, 'aliquota':user['cassa']['aliquota']	}
	subtotale += data['cassa']['importo']
	data['total']['imponibile'] = subtotale
	####	CALCOLO DELLA RITENUTA D'ACCONTO
	if ritenuta:
		data['total']['ritenuta'] = -1 * subtotale * (user['ritenuta']['aliquota']/100)	# = user['ritenuta']['importo']
	else:	data['total']['ritenuta'] = 0
	data['ritenuta'] = {	'importo':data['total']['ritenuta'], 'imponibile':subtotale, 'aliquota':user['ritenuta']['aliquota']	}
	subtotale += data['total']['ritenuta']
	####	CALCOLO DELL'IMPONIBILE EFFETTIVO
	data['total']['imposta'] = data['total']['imponibile'] * (data['total']['aliquota']/100)
	####	CALCOLO DELL'IMPORTO TOTALE
	subtotale += data['total']['imposta']
	data['total']['TOTALE'] = max(0,subtotale)
	if 'pagamento' in data.keys():
		data['pagamento']['importo'] = data['total']['TOTALE']
	return FatturaPA_assemble(user, client, data)

def XML_input(input_text):
	from xml.sax.saxutils import escape
	return str( escape(input(input_text)).strip() )

CFre, EORIre = re.compile(r"[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]"), re.compile(r"[a-zA-Z0-9]{13,17}")
emailre = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9-._]+@[a-zA-Z0-9][a-zA-Z0-9-._]+")
IBANre, BICre = re.compile(r"[a-zA-Z]{2}[- ]?[0-9]{2}[- ]?(?:[a-zA-Z0-9][- ]?){11,30}"), re.compile(r"[A-Z]{6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3}){0,1}")

def main():
	def print_args():
		print(" Utilizzo:  %s  emetti | fornitore | inizializza"%os.path.basename(sys.argv[0]))
		print("\t\temetti       Crea fattura generica verso fornitore esistente")
		print("\t\tconsulenza       \"\"   di consulenza a fornitore (UE / extra-UE)")
		print("\t\tcommittente  Aggiunge un fornitore (UE / extra-UE) al database")
		print("\t\tinizializza  Inizializza un nuovo database con i tuoi dati")
		print('\n')
		sys.exit(9)
	print("pyFatturaPA %s - Genera rapidamente fatture elettroniche semplici in XML nel formato FatturaPA."%__VERSION)
	print("GNU (GPL) 2019 by Walter Arrighetti  <walter.arrighetti@agid.gov.it>\n")
	[PROVINCES.extend(list(prov.keys())) for prov in REGIONS.values()]
	if len(sys.argv) != 2:	
    	print_args()
	elif sys.argv[1].lower()=="consulenza":	
    	issue_consultancy()
	elif sys.argv[1].lower()=="emetti":	
    	issue_invoice()
	elif sys.argv[1].lower()=="committente":
    	add_company()
	elif sys.argv[1].lower()=="inizializza":
    	create_config()
	else:
     	print_args()
	sys.exit(0)


if __name__ == "__main__": main()
