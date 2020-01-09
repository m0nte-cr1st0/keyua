# Python imports
from datetime import date

RATES = [
    {
        'id': 'Minimum',
        'title': 'Minimum',
        'min': 50,
        'max': 999,
        'year_percent': 12,
        'simple': True
    },
    {
        'id': 'Standart',
        'title': 'Standart',
        'min': 1000,
        'max': 4999,
        'year_percent': 15,
        'simple': True
    },
    {
        'id': 'Gold',
        'title': 'Gold',
        'min': 5000,
        'max': 49999,
        'year_percent': 17,
        'simple': False,
        'complicated_rate': {
            'title': 'Gold +',
            'year_percent': 17,
        }
    },
    {
        'id': 'Platinum',
        'title': 'Platinum',
        'min': 50000,
        'max': 100000,  # TODO: maybe other value
        'year_percent': 20,
        'simple': False,
        'complicated_rate': {
            'title': 'Platinum +',
            'year_percent': 25,
        }
    },
]


class RateCalculation(object):

    def __init__(self, deposit, period, start_date=None):
        self.deposit = deposit
        self.period = period
        self.start_date = start_date or date.today()
