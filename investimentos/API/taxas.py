from obter_taxas import obter_valores

cdi, selic = obter_valores()

cdi = float(cdi.replace(',', '.'))
selic = float(selic.replace(',', '.'))