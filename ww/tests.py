"""
docker-compose run web python manage.py test -k -v 3 ts
"""
import sys
from django.test import SimpleTestCase

from ts.models import Property

class testProperty(SimpleTestCase):
    def testPropertyTypeFromString(self):
        self.assertTrue(True)
        # Todo: add more test cases when we change Property.PROPERTY_TYPE_CHOICES
        data = (
            ('CommerCial', 'Commercial',1),
            ('redident', 'Residential', 2),
            ('Residential', 'Residential', 2),
            ('RESIDENTIal', 'Residential', 2),
            ('Mixed Use', 'Mixed Use',3),
            ('Data Center', 'Data Center',4),
            ('Unknown', 'Unknown',5 ),
        )
        for tst in data:
            (val, st) = Property.propertyTypeFromString(tst[0])
            print >>sys.stderr,"returned st ", st
            self.assertEqual(st, tst[1])
            self.assertEqual(val, tst[2])
