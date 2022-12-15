from __future__ import absolute_import, unicode_literals

from celery import shared_task
import requests

from MarketPrice.config import COMPANY_LIST, MARKETSTACK_API_KEY, MARKETSTACK_LAST_EOD_URL
from MarketPrice.helpers import save_data


@shared_task
def get_data():
    """
    Function that integrates Market Stack API to fetch price data of companies (defined in COMPANY_LIST)
    of the last working day.

    This function is executed by a cronjob defined in celery.py.
    It configured to execute at 4:30 am HKT which is 30 mins past NYSE closing time.

    Function makes get request at Market Stack latest EOD endpoint, and a successful API response is stored onto the
    database using a helper method save_data which parses the response and stores the data.
    """
    try:
        company_list = ",".join(COMPANY_LIST)

        # populating params for get request
        params = {
            "access_key": MARKETSTACK_API_KEY,
            "symbols": company_list
        }

        # Making get request using the params to Market Stack API
        api_result = requests.get(MARKETSTACK_LAST_EOD_URL, params)
        api_response = api_result.json()
        data = api_response.get("data")

        # save data onto the database using save_data helper method
        save_data(data)

    except Exception as e:
        print(e)
        # log and raise the exception (future work)

