from django.db import models
import operator


class StockPriceManager(models.Manager):
    """
    It derives from django model Manager defines a model manager method
    """

    def highest_increment(self):
        """
        A method that finds the company with the highest increment in stock price in last 5 (defined number of
        historical working days) working days.

        :return: <str> Stock symbol of the company which has the highest increment in closing stock price in past 5
        (defined number of historical working days) working days
        """
        try:
            dates = StockPrice.objects.all().order_by('-date').values('date').distinct()    # list of all working days
            start_date = dates[0]['date']   # save date of the last working day
            end_date = dates[4]['date']     # save date of the 5th last working day

            start_data = StockPrice.objects.filter(date=start_date).values_list('date', 'symbol', 'close')
            end_data = StockPrice.objects.filter(date=end_date).values_list('date', 'symbol', 'close')

            data_dict = dict()
            for idx in range(len(start_data)):
                data_dict[start_data[idx][1]] = start_data[idx][2] - end_data[idx][2]

            result = max(data_dict.items(), key=operator.itemgetter(1))[0]
            return result

        except IndexError:
            print("Historical Data of 5 working days not available")
            raise

        except Exception as e:
            print(e)
            raise e


class StockPrice(models.Model):
    """
    StockPrice class derives from django models class used to store the API response of Market Stack get the latest EOD
    API
    """
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    adj_high = models.FloatField()
    adj_low = models.FloatField()
    adj_close = models.FloatField()
    adj_open = models.FloatField()
    adj_volume = models.FloatField()
    split_factor = models.FloatField()
    symbol = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)
    date = models.DateField()
    objects = StockPriceManager()

    class Meta:
        unique_together = (('date', 'symbol'),)
