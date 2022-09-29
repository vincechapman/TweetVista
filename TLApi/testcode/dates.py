from datetime import date,datetime

dte = date(1999,12,1)
if isinstance(dte,date):
    print(f'id date:{dte}')
else:
    print(f'is not date:{dte}')
