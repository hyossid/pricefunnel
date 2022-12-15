from django.test import TestCase

from MarketPrice.test_data import test_data
from MarketPrice.models import StockPrice
from MarketPrice.helpers import save_data
from MarketPrice.config import AMAZON_SYMBOL


class MarketPriceTestCase(TestCase):

    def setUp(self):
        save_data(test_data[:30])

    def test_highest_increment(self):
        result = StockPrice.objects.highest_increment()
        self.assertEqual(result, AMAZON_SYMBOL)

    def test_highest_increment_exception(self):
        with self.assertRaises(IndexError):
            date = StockPrice.objects.all().order_by('-date').values('date').distinct()[4]['date']
            StockPrice.objects.filter(date=date).delete()
            StockPrice.objects.highest_increment()
