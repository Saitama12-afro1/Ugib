from django.test import TestCase
from crud.models import UdsMeta, UdsMetaApr

class UdsMeta(TestCase):
    def setUp(self) -> None:
        UdsMeta.objects.create(stor_folder  = "dada", uniq_id = "12412531531")
        
        
    def test_create(self):
        t = UdsMeta.objects.get(arr = "dada")
        self.assertEqual(t.arr, "kar")
    