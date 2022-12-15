from django.http import HttpResponse
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from MarketPrice.models import StockPrice
from MarketPrice.config import COMPANY_LIST, NUM_OF_HISTORY_DAYS


def index(request):
    return HttpResponse("Hello, You're at the MarketPrice App index")


class LineChartJSONView(BaseLineChartView):
    """
    Class extends from BaseLineChartView of Django chartjs library,
    used to create the line chart visualisation of closing price of all companies in COMPANY_LIST in configured number
    of historical days
    """
    def __init__(self):
        # fetch closing price of all companies in last 5 (No of History days needed, currently set to 5) working days
        self.result = StockPrice.objects.values_list('date',
                                                     'symbol',
                                                     'close'
                                                     ).order_by('-date')[: NUM_OF_HISTORY_DAYS * len(COMPANY_LIST)]

    def get_labels(self):
        """
        Return list of dates for the x-axis.
        """
        dates = [self.result[idx][0] for idx in range(0, len(self.result), len(COMPANY_LIST))]
        # setting the dates in ascending order
        dates = dates[::-1]
        return dates

    def get_providers(self):
        """
        Return names of companies in list format
        """
        return COMPANY_LIST

    def get_data(self):
        """
        Return a 2D list containing closing price of stock of all the companies in COMPANY_LIST in past 5
        (required number of historical days) working days, each nested list representing prices of a company

        sample structure:
        [
            [Company 1 prices over past 5 working days],
            [Company 2 prices over past 5 working days],
            ...
        ]
        """
        total_companies = len(COMPANY_LIST)

        # initializes a blank 2D list, number of inner list equal to number of companies in COMPANY_LIST
        price_list = list()
        for company in range(total_companies):
            price_list.append(list())

        # populate the above initialized list with prices from self.result
        for idx in range(len(self.result)):
            price_list[idx % total_companies].append(self.result[idx][2])

        return price_list


line_chart = TemplateView.as_view(template_name='price_history.html')
line_chart_json = LineChartJSONView.as_view()
