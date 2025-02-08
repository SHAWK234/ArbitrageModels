from alpha_vantage.foreignexchange import ForeignExchange
from pprint import pprint
cc = ForeignExchange(key='W0BJCLRW7YVPSRJO')


# API: WKPRZN72FYG5Q6YZYUGSGJF1
currency_codes = [
     "USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD",
     "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "RUB", "INR", "BRL", "ZAR",
     "DKK", "PLN", "TWD", "THB", "MYR", "IDR", "CZK", "ILS", "CLP", "PHP",
     "AED", "COP", "SAR", "MYR", "RON", "HUF", "PKR", "EGP", "BDT", "VND",
     "UAH", "KES", "ARS", "PEN", "QAR", "NGN", "XOF", "PGK", "XAF", "CHF",
     "ISK", "JOD", "LBP", "OMR", "BHD", "SYP", "YER", "IRR", "IQD", "SDG",
     "LYD", "TND", "MAD", "DZD", "MUR", "NAD", "ZWL", "BWP", "GTQ", "HNL",
     "PYG", "UYU", "CRC", "PAB", "BOB", "GHS", "FJD", "SRD", "HTG", "BMD",
     "KZT", "AZN", "AMD", "GEL", "KGS", "TJS", "UZS", "MNT", "IRR", "AFN",
     "LKR", "NPR", "MMK", "KHR", "LAK", "BND", "SBD", "VUV", "WST", "TOP",
     "IQD", "SOS", "DJF", "ETB", "GMD", "SHP", "SLL", "SCR", "CDF", "MGA",
     "MZN", "RWF", "LSL", "BIF", "MWK", "AOA", "TZS", "UGX", "ZMW", "SRD",
     "FKP", "JEP", "GGP", "IMP", "KMF", "TVD", "ERN", "KPW", "CUP", "SVC"
]


# A = 'USD'
for A in currency_codes:
    AtoBList = []
    for B in currency_codes:
        data, _ = cc.get_currency_exchange_rate(from_currency=B,to_currency=A)
        AtoBList.append(data['5. Exchange Rate'])

    d1 = min(AtoBList)
    minIndex1 = AtoBList.index(d1)

    B = currency_codes[minIndex1]

    BtoCList = []
    for C in currency_codes:
        data, _ = cc.get_currency_exchange_rate(from_currency=B,to_currency=C)
        BtoCList.append(data['5. Exchange Rate'])

    d2 = min(BtoCList)
    minIndex2 = currency_codes.index(m2)
    C = currency_coes[minIndex2]

    data, _ = cc.get_currency_exchange_rate(from_currency=C,to_currency=A)

    d3 = data['5. Exchange Rate']

    if (d2*d3)/d1 > 1:
        print("Arb can be found in: ")
        print(f'A: {A}, B: {B}, C: {C}')



