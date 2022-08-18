from django.test import TestCase

# # TEST MODELS
# class Barcode(models.Model):
#     bc = BarcodeField()
#
#
# class BarcodePK(models.Model):
#     bc = BarcodeField(primary_key=True)
#
#
# class BarcodeUnique(models.Model):
#     bc = BarcodeField(unique=True)
#
#
# class BarcodeCB(models.Model):
#     bc = BarcodeField(country='123', brand='1234')
#
#
# class BarcodeAll(models.Model):
#     bc = BarcodeField(primary_key=True, unique=True, country='123', brand='1234')
#
#
# # TESTS
# class BarcodeTestCase(TestCase):
#     def setUp(self):
#         Barcode.objects.create()
#         BarcodePK.objects.create()
#         BarcodeUnique.objects.create()
#         BarcodeCB.objects.create()
#         BarcodeAll.objects.create()
#
#     def test_barcode(self):
#         """ Test simple barcode creation """
#         bc = Barcode.objects.all().first()
#         bcpk = BarcodePK.objects.all().first()
#         bcu = BarcodeUnique.objects.all().first()
#         bccb = BarcodeCB.objects.all().first()
#         bcall = BarcodeAll.objects.all().first()
#
#         self.assertEqual(bc is not None, True)
#         self.assertEqual(bcpk is not None, True)
#         self.assertEqual(bcu is not None, True)
#         self.assertEqual(bccb is not None, True)
#         self.assertEqual(bcall is not None, True)