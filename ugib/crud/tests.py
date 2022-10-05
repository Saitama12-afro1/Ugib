from django.test import TestCase
from .models import Test

class UdsMeta(TestCase):
    def setUp(self) -> None:
        Test.objects.create(arr = "dada")
        
        
    def test_create(self):
        t = Test.objects.get(arr = "dada")
        self.assertEqual(t.arr, "kar")
    