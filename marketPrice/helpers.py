from MarketPrice.models import StockPrice
from datetime import datetime


def parse_date(data):
    """
    A helper function which parses the block of a company's stock price data.
    Transforms the date field to datetime (YYYY-MM-DD) format.
    """
    temp = data['date'].split("T")[0]
    temp = datetime.strptime(temp, '%Y-%m-%d')
    data['date'] = datetime.strftime(temp, '%Y-%m-%d')
    return data


def save_data(data_list):
    """
    A helper function that accepts the list of dictionaries,
    with each dictionary consisting of a company's stock price data of a working day.
    Each dictionary is saved onto the database in StockPrice table

    :param data_list: <list> A list of dictionary

    sample dictionary:
    {
        "open": 236.28,
        "high": 240.05,
        "low": 235.94,
        "close": 237.71,
        "volume": 26460729.0,
        "adj_high": 240.055,
        "adj_low": 235.94,
        "adj_close": 237.71,
        "adj_open": 236.28,
        "adj_volume": 28092196.0,
        "split_factor": 1.0,
        "symbol": "MSFT",
        "exchange": "XNAS",
        "date": "2021-03-16T00:00:00+0000"
    }
    """

    try:
        for item in data_list:
            data = parse_date(item)

            result = StockPrice.objects.filter(symbol=data['symbol'], date=data['date']).exists()

            if not result:
                StockPrice.objects.create(
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    volume=data['volume'],
                    adj_high=data['adj_high'],
                    adj_low=data['adj_low'],
                    adj_close=data['adj_close'],
                    adj_open=data['adj_open'],
                    adj_volume=data['split_factor'],
                    split_factor=data['split_factor'],
                    symbol=data['symbol'],
                    exchange=data['exchange'],
                    date=data['date'],
                )

    except Exception as e:
        raise e
