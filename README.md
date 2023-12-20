# FatturaPA-python
Tool for quick, command-line generation of simple e-Invoice compatible with the Italian-standard, [FatturaPA](https://www.fatturapa.gov.it). This is a [developers.italia.it](https://developers.italia.it/) Community Edition, version statically forked from [github.com/walter-arrighetti/](https://github.com/walter-arrighetti)[**pyFatturaPA**](https://github.com/walter-arrighetti/pyFatturaPA).
It is a typical, lazy sunday afternoon exercise, aimed at self-generating e-invoices to private companies as an individual freelance consultant.A rudimetary command-line generator of XML e-invoices to be later electronically signed or sealed. It generates a JSON database of clients (with VAT# and full invoicing information). More and more complex invoicing scenarios will be added in future releases.

***DISCLAIMER***: The author denies any responsibilities, either explicit or implied, on possible damages and liabilities derived or implied by the use of this software tool. In particular, no assumption of validity or compatibility on the software deliverables must be assumed. Also, the software is supplied *as is* (in GNU GPL terminology).

Due to the validity of such e-invoicing standard being limited to Italian finance, the README continues in Italian.

<img src="opt/pyFatturaPA_icon.png" />

### Descrizione
Questo tool viene inizialmente impiegato per costituire un database contenente un elenco essenziale di committenti (ove sono registrate le loro informazioni fiscali quali P.IVA, indirizzo PEC, C.F., ecc.). Il database, chiamato `pyFatturaPA.conf.json`, deve trovarsi nella medesima cartella del tool, così come si consiglia di eseguirlo da tale cartella.

Sempre mediante lo stesso (cfr. sezione **Sintassi**), si possono generare singole fatture elettroniche in formato XML che rispettano lo standard [*FatturaPA* 1.3.1](https://www.fatturapa.gov.it/it/norme-e-regole/documentazione-fatturapa/). La sintassi del nome del file generato è `IT`*`numPartitaIVA`*`_`*`numFattura`*`.xml`, cioè combinando il numero di P.IVA emettente e l'identificativo univoco di quella fattura elettronica specifica.

Tali fatture elettroniche sono pronte per essere *firmate* (da parte del cedente/prestatore) ovvero *sigillate elettronicamente* (da parte dell'[Agenzia delle Entrate](https://www.agenziaentrate.gov.it)), per poi essere inviate al [*Sistema di Interscambio* dell'Agenzia delle Entrate](https://ivaservizi.agenziaentrate.gov.it/portale/) stessa e, da li, in conservazione sostitutiva.

### Sintassi
```
pyFatturaPA   consulenza | emetti | committente | inizializza
```
Il tool effettua quattro possibili operazioni:
 
`emetti` genera una singola fattura con opzioni piuttosto complete; sono infatti supportate diverse tipologie di fattura/ritenuta/nota, esigibilità, aliquota, condizioni e modalità di pagamento, *natura* della fattura (per eventuale esclusione, trasferimento, inversione contabile o esenzione dell'IVA ― inclusi i riferimenti normativi) nonché causali, quantità e unità di misura per voci multiple nella fatturazione. Sono supportate fatture elettroniche verso paesi UE ed extra UE. L'eventuale IBAN ove pagare la fatturazione (in caso di pagamenti tramite bonifico) può essere preso automaticamente dalle informazioni del cedente/prestatore (nel database), immesso manualmente, ovvero omesso.
 
 `consulenza` è una versione specializzata del precedente; crea ancor più rapidamente una singola fattura, relativa ad una prestazione senza alcuna cessazione/trasferimento di beni, da parte di un professionista soggetto ad IVA (22%), alla cassa INPS (4%) e a ritenuta d'acconto (−20%). La generazione della fattura elettronica avviene inserendo solamente i **6** campi generici (*obbligatori* se in corsivo):
  * *sigla identificativa del committente* (3 caratteri, così come indicata nel database dei committenti/cessionari),
  * *numero identificativo progressivo della fattura*,
  * numero d'ordine del committente cui la fattura fa riferimento,
  * natura delle condizioni di pagamento (p.es. esclusione/trasferimento/esenzione IVA, inversione contabile, ecc.),
  * giorni ammessi per il pagamento dall'emissione,
  * codice IBAN cui intestare il pagamento (qualora non  compreso nelle informazioni del prestatore d'opera nel database),
  * causale complessiva della fattura;

più *almeno una* voce di fatturazione, ciascuna corrispondente a distinte afferenti la medesima fattura.

 `inizializza` inizializza il database  (`pyFatturaPA.conf.json`) creandone uno vuoto e inserendovi *una tantum* le sole informazioni del cedente/prestatore, dalle quali viene anche determinato se è soggetto a vati tipi di casse o ritenute.
 
 `committente` permette di aggiungere al database dei fornitori/committenti un'ulteriore voce, che sarà poi indicizzata mediante codice a 3 cifre alfanumeriche. Non è attualmente possibile rimuovere un cessionario/committente.

***DISCLAIMER***: L'autore nega ogni responsabilità, diretta o indiretta, circa l'uso del software e dei suoi derivati. In particolare non viene fatta alcuna presunzione di validità e conformità delle evidenze informatiche prodotte con gli standard tecnici di riferimento. Inoltre, il software è fornito *così com'è*, secondo i termini della licenza utilizzata.

Script per la fattura elettronica.

Per accedere al portale è stato usato lo script con licenza gratuita fornito da Claudio Pizzillo (FeCScraper).

Il codice per il controllo del file nel portale l'ho scritto io.

Per utilizzare lo script servono i dati di accesso a fisconline o entratel,

fec_controllo.py codicefiscale pin password partitaiva


# Python A38

![full workflow](https://github.com/Truelite/python-a38/actions/workflows/py.yml/badge.svg)

Library to generate Italian Fattura Elettronica from Python.

This library implements a declarative data model similar to Django models, that
is designed to describe, validate, serialize and parse Italian Fattura
Elettronica data.

Only part of the specification is implemented, with more added as needs will
arise. You are welcome to implement the missing pieces you need and send a pull
request: the idea is to have a good, free (as in freedom) library to make
billing in Italy with Python easier for everyone.

The library can generate various kinds of fatture that pass validation, and can
parse all the example XML files distributed by
[fatturapa.gov.it](https://www.fatturapa.gov.it/it/lafatturapa/esempi/)


## Dependencies

Required: dateutil, pytz, asn1crypto, and the python3 standard library.

Optional:
 * yapf for formatting `a38tool python` output
 * lxml for rendering to HTML
 * the wkhtmltopdf command for rendering to PDF
 * requests for downloading CA certificates for signature verification


## `a38tool` script

A simple command line wrapper to the library functions is available as `a38tool`:

```text
$ a38tool --help
usage: a38tool [-h] [--verbose] [--debug]
               {json,xml,python,diff,validate,html,pdf,update_capath} ...

Handle fattura elettronica files

positional arguments:
  {json,xml,python,diff,validate,html,pdf,update_capath}
                        actions
    json                output a fattura in JSON
    xml                 output a fattura in XML
    python              output a fattura as Python code
    diff                show the difference between two fatture
    validate            validate the contents of a fattura
    html                render a Fattura as HTML using a .xslt stylesheet
    pdf                 render a Fattura as PDF using a .xslt stylesheet
    update_capath       create/update an openssl CApath with CA certificates
                        that can be used to validate digital signatures

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         verbose output
  --debug               debug output
```

See [a38tool.md](a38tool.md) for more details.



## Example code

```py
import a38
from a38.validation import Validation
import datetime
import sys

cedente_prestatore = a38.CedentePrestatore(
    a38.DatiAnagraficiCedentePrestatore(
        a38.IdFiscaleIVA("IT", "01234567890"),
        codice_fiscale="NTNBLN22C23A123U",
        anagrafica=a38.Anagrafica(denominazione="Test User"),
        regime_fiscale="RF01",
    ),
    a38.Sede(indirizzo="via Monferrato", numero_civico="1", cap="50100", comune="Firenze", provincia="FI", nazione="IT"),
    iscrizione_rea=a38.IscrizioneREA(
        ufficio="FI",
        numero_rea="123456",
        stato_liquidazione="LN",
    ),
    contatti=a38.Contatti(email="local_part@pec_domain.it"),
)

cessionario_committente = a38.CessionarioCommittente(
    a38.DatiAnagraficiCessionarioCommittente(
        a38.IdFiscaleIVA("IT", "76543210987"),
        anagrafica=a38.Anagrafica(denominazione="A Company SRL"),
    ),
    a38.Sede(indirizzo="via Langhe", numero_civico="1", cap="50142", comune="Firenze", provincia="FI", nazione="IT"),
)

bill_number = 1

f = a38.FatturaPrivati12()
f.fattura_elettronica_header.dati_trasmissione.id_trasmittente = a38.IdTrasmittente("IT", "10293847561")
f.fattura_elettronica_header.dati_trasmissione.codice_destinatario = "FUFUFUF"
f.fattura_elettronica_header.cedente_prestatore = cedente_prestatore
f.fattura_elettronica_header.cessionario_committente = cessionario_committente

body = f.fattura_elettronica_body[0]
body.dati_generali.dati_generali_documento = a38.DatiGeneraliDocumento(
    tipo_documento="TD01",
    divisa="EUR",
    data=datetime.date.today(),
    numero=bill_number,
    causale=["Test billing"],
)

body.dati_beni_servizi.add_dettaglio_linee(
    descrizione="Test item", quantita=2, unita_misura="kg",
    prezzo_unitario="25.50", aliquota_iva="22.00")

body.dati_beni_servizi.add_dettaglio_linee(
    descrizione="Other item", quantita=1, unita_misura="kg",
    prezzo_unitario="15.50", aliquota_iva="22.00")

body.dati_beni_servizi.build_dati_riepilogo()
body.build_importo_totale_documento()

res = Validation()
f.validate(res)
if res.warnings:
    for w in res.warnings:
        print(str(w), file=sys.stderr)
if res.errors:
    for e in res.errors:
        print(str(e), file=sys.stderr)

filename = "{}{}_{:05d}.xml".format(
    f.fattura_elettronica_header.cedente_prestatore.dati_anagrafici.id_fiscale_iva.id_paese,
    f.fattura_elettronica_header.cedente_prestatore.dati_anagrafici.id_fiscale_iva.id_codice,
    bill_number)

tree = f.build_etree()
with open(filename, "wb") as out:
    tree.write(out, encoding="utf-8", xml_declaration=True)
```


# Digital signatures

Digital signatures on Firma Elettronica are
[CAdES](https://en.wikipedia.org/wiki/CAdES_(computing)) signatures.

openssl cal verify the signatures, but not yet generate them. A patch to sign
with CAdES [has been recently merged](https://github.com/openssl/openssl/commit/e85d19c68e7fb3302410bd72d434793e5c0c23a0)
but not yet released as of 2019-02-26.

## Downloading CA certificates

CA certificates for validating digital certificates are
[distributed by the EU in XML format](https://ec.europa.eu/cefdigital/wiki/display/cefdigital/esignature).
See also [the AGID page about it](https://www.agid.gov.it/it/piattaforme/firma-elettronica-qualificata/certificati).

There is a [Trusted List Browser](https://webgate.ec.europa.eu/tl-browser/) but
apparently no way of getting a simple bundle of certificates useable by
openssl.

`a38tool` has basic features to download and parse CA certificate information,
and maintain a CA certificate directory:

```
a38tool update_capath certdir/ --remove-old
```

No particular effort is made to validate the downloaded certificates, besides
the standard HTTPS checks performed by the [requests
library](http://docs.python-requests.org/en/master/).

## Verifying signed `.p7m` files

Once you have a CA certificate directory, verifying signed p7m files is quite
straightforward:

```
openssl cms -verify -in tests/data/test.txt.p7m -inform der -CApath certs/
```


# Useful links

XSLT stylesheets for displaying fatture:

* From [fatturapa.gov.it](https://www.fatturapa.gov.it/),
  among the [FatturaPA resources](https://www.fatturapa.gov.it/it/norme-e-regole/documentazione-fattura-elettronica/formato-fatturapa/index.html)
* From [AssoSoftware](http://www.assosoftware.it/allegati/assoinvoice/FoglioStileAssoSoftware.zip)


# Copyright

Copyright 2019-2022 Truelite S.r.l.

This software is released under the Apache License 2.0

Run the `download-docs` script to populate this directory with official
documentation. Note that the URLS may change, and the script may need to be
updated from time to time.

Normativa: <https://www.fatturapa.gov.it/it/norme-e-regole/normativa/>

Formato: <https://www.fatturapa.gov.it/it/norme-e-regole/documentazione-fattura-elettronica/formato-fatturapa/>

Assocons validator: <https://fatturazione-elettronica-pa.assocons.it/validazione-fattura-elettronica.html>

Agenzia delle Entrate validator: <https://www.fatturapa.gov.it/it/sistemainterscambio/controlli-ed-errori/>

# TODO

Get documentation from <https://www.agenziaentrate.gov.it/wps/content/nsilib/nsi/schede/comunicazioni/fatture+e+corrispettivi/fatture+e+corrispettivi+st/st+invio+di+fatturazione+elettronica>
(it covers Fattura Elettronica Semplificata)

