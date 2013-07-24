#! /bin/env python2
# set encoding=utf-8

A_URI = r'http://www.russianpost.ru/autotarif/Autotarif.aspx'
DEFAULTS = dict(
    countryCode=643,  # код РФ
    typePost=1,  # тип пересылки (= Наземн.)
    weight=100,  # если забыли передать вес, посчитаем по минимуму
    value1=100,  # объявленная ценность, если вдруг не передали (руб.)
    viewPost=26  # по умолчанию считаем ценную бандероль
    )

PARCEL_TYPES = (
    26,  # "Ценная бандероль"),
    36,  # "Ценная посылка")
    )
PARCEL_THRESHOLD = 1900
debuglevel = 0


class RusPostConnectionError(Exception):
    pass

from HTMLParser import HTMLParser
import httplib2


class TarifHolder(dict):
    def __setitem__(self, item, value):
        if item in (
                'viewpostname',  # Вид отправления как Ценная бандероль
                'countryname',
                'typepost',  # Способ пересылки как Наземн.
                'postoffice',  # Индекс получателя
                ):
            value = value.decode('utf-8')
        elif item in (
                'avalue',  # Объявленная ценность
                'tarifvalue',  # Собственно тариф, т.е. искомое
                ):
            value = float(value.replace(',', '.'))
        elif item in ('weight'):
            value = float(value) / 1000
        super(TarifHolder, self).__setitem__(item, value)


class TarifParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.result = TarifHolder()
        self.resultKey = None
        self.reconnect = None
        self.secretKey = None
        self.method = None

    def handle_starttag(self, tag, attrs):
        attrs = {key: value for key, value in attrs}
        try:
            getattr(self, "handle{}".format(tag))(attrs)
        except AttributeError: pass

    def handle_data(self, data):
        if self.resultKey:
            self.result[self.resultKey] = data
            self.resultKey = None

    def handlespan(self, attrs):
        if 'id' in attrs:
            _id = attrs['id'].lower().strip()
            if _id in (
                    'viewpostname',  # Вид отправления как Ценная бандероль
                    'countryname',
                    'typepost',  # Способ пересылки как Наземн.
                    'weight',
                    'postoffice',  # Индекс получателя
                    'avalue',  # Объявленная ценность
                    'tarifvalue',  # Собственно тариф, т.е. искомое
                    ):
                self.resultKey = _id

    def handlebody(self, attrs):
        if 'onload' in attrs:
            self.reconnect = True

    def handleinput(self, attrs):
        if 'id' in attrs and 'value' in attrs:
            if attrs['id'].strip().lower() == 'key':
                self.secretKey = attrs['value'].strip()

    def handleform(self, attrs):
        self.method = attrs['method'].strip().upper()


class TarifGetter():

    def __init__(self, **kwargs):
        httplib2.debuglevel = debuglevel
        self.countConnections = 0
        self.method = 'GET'
        self.uri = A_URI
        self.data = DEFAULTS.copy()
        if kwargs:
            self.data.update(kwargs)
            if not 'viewPost' in kwargs:
                self.updateParcelType()

    def __setitem__(self, item, value):
        self.data[item] = value

    def __getitem__(self, item):
        return self.data[item]

    def updateParcelType(self):
        self.data['viewPost'] = PARCEL_TYPES[0] if \
            self.data['weight'] < PARCEL_THRESHOLD else PARCEL_TYPES[1]

    def connect(self, **qdict):
        self.countConnections += 1
        if not qdict:
            qdict = self.data
        from httplib2 import Http
        import urlparse as parse
        from urllib import urlencode
        parts = parse.urlsplit(self.uri)
        qs = urlencode(qdict)
        uri = parse.urlunsplit((
            parts.scheme,
            parts.netloc,
            parts.path,
            qs if self.method == 'GET' else None,
            None))
        if debuglevel:
            print "sending {} request".format(self.method)
            print "uri is {}".format(uri)

            print "body is {}".format(qs)
        return Http().request(
            uri,
            self.method,
            qs if self.method == 'POST' else None)

    def resetMethod(self):
        self.method = 'GET'

    def getTarif(self, **kwargs):
        if self.countConnections > 4:
            raise RusPostConnectionError("Too many reconnections")
        if kwargs:
            self.data.update(kwargs)
            if not 'viewPost' in kwargs:
                self.updateParcelType()
        header, contents = self.connect()
        if header.status != 200:
            raise RusPostConnectionError(
                "Server returned error {}".format(header.status))
        parser = TarifParser()
        parser.feed(contents)
        if parser.reconnect:
            if parser.method:
                self.method = parser.method
            if parser.secretKey:
                self.connect(key=parser.secretKey)
                self.resetMethod()
            return self.getTarif()
        else:
            if debuglevel:
                print 'gotcha...?'
                print "contents: {} ... \n {}".format(
                    contents[:200], contents[-1000:])
            parser.reset()
            parser.feed(contents)
            parser.close()
            return parser.result


def calculate(weight, zipCode, price):

    for i in range(3):
        try:
            result = TarifGetter().getTarif(
                weight=int(weight),
                postOfficeId=zipCode,
                value1=int(price))
            return result['viewpostname'], result['tarifvalue']
        except RusPostConnectionError as e:
            import time
            time.sleep(30)
    raise e
