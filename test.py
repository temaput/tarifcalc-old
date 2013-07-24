#! /bin/env python2
# set encoding=utf-8

import tarifcalc
import unittest

CONTROL = (
        ({'weight':1000, 'zipCode':'111402', 'price':2000.00}, 139.00),
        ({'weight':2000, 'zipCode':'111402', 'price':5030.00}, 376.00)
        )

PARCEL_TYPES = (u"Ценная бандероль", u"Ценная посылка")

class SimpleGoodInputTest(unittest.TestCase):
    def testPostType(self):
        """ Тип отправления должен быть бандероль или посылка в зависимости от веса """
        zipCode, price = '111402', 1000.00
        for weight in (100, 1500, 5000):
            parcelType, tarifValue = tarifcalc.calculate(weight, zipCode, price)
            correctPT = PARCEL_TYPES[0]  if weight < 2000 \
                    else PARCEL_TYPES[1]

            self.assertEqual(parcelType, correctPT)
    def testCorrectCalc(self):
        """Сумма тарифа должна совпадать с контрольными значениями"""
        for parcel in CONTROL:
            parcelType, tarifValue = tarifcalc.calculate(**parcel[0])
            self.assertEqual(tarifValue, parcel[1])
if __name__ == '__main__':
    unittest.main()
