"""
Utility functions to support data generation etc.
"""

from random import randint, choice, uniform, randrange
from datetime import datetime, date, time, timedelta
from decimal import Decimal

def get_latlon():
    """
    Return a random pair of [latitude, longitude] values.
    """
    latlon = [0, 0]
    latlon[0] = str(float(Decimal(randrange(-90, 90))))
    latlon[1] = str(float(Decimal(randrange(-180, 180))))
    return(latlon)


def random_dtstr(start=None, end=None):
    """
    Return a random datetime string.
    """
    if not start:
        start = datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')

    if not end:
        end = datetime.strptime('2015-12-31', '%Y-%m-%d')
    rand_dts = datetime.strftime(
        start + timedelta(seconds=randint(0, int((end - start).total_seconds()))), '%Y-%m-%dT%H:%M:%S')
    return rand_dts


def valid_cardinality(self, v):
    """
    A dictionary of valid cardinality values and the lower and upper values of the minimum and maximum 
    occurrences allowed.
    
    The requested setting is then tested for a valid setting.
    Example:
    
                 minOccurs      maxOccurs
    'setting':((lower,upper),(lower,upper))
    
    A Python value of 'None' equates to 'unbounded' or 'unlimited'.
    """
    c = {'act': ((0, 1), (0, 1)), 'ev': ((0, 1), (0, 1)), 'vtb': ((0, 1), (0, 1)), 'vte': ((0, 1), (0, 1)), 'tr': ((0, 1), (0, 1)),
         'modified': ((0, 1), (0, 1)), 'location': ((0, 1), (0, 1)), 'relation_uri': ((0, 1), (0, 1)), 'value': ((0, 1), (0, 1)),
         'units': ((0, 1), (0, 1)), 'size': ((0, 1), (0, 1)), 'encoding': ((0, 1), (0, 1)), 'language': ((0, 1), (0, 1)),
         'formalism': ((0, 1), (0, 1)), 'media_type': ((0, 1), (0, 1)), 'compression_type': ((0, 1), (0, 1)), 'link': ((0, 1), (0, 1)),
         'hash_result': ((0, 1), (0, 1)), 'hash_function': ((0, 1), (0, 1)), 'alt_txt': ((0, 1), (0, 1)), 'referencerange': ((0, 1), (0, Decimal('Infinity'))),
         'normal_status': ((0, 1), (0, 1)), 'magnitude_status': ((0, 1), (0, 1)), 'error': ((0, 1), (0, 1)), 'accuracy': ((0, 1), (0, 1)),
         'numerator': ((0, 1), (0, 1)), 'denominator': ((0, 1), (0, 1)), 'numerator_units': ((0, 1), (0, 1)),
         'denominator_units': ((0, 1), (0, 1)), 'xdratio_units': ((0, 1), (0, 1)), 'date': ((0, 1), (0, 1)), 'time': ((0, 1), (0, 1)),
         'datetime': ((0, 1), (0, 1)), 'day': ((0, 1), (0, 1)), 'month': ((0, 1), (0, 1)), 'year': ((0, 1), (0, 1)), 'year_month': ((0, 1), (0, 1)),
         'month_day': ((0, 1), (0, 1)), 'duration': ((0, 1), (0, 1)), 'view': ((0, 1), (0, 1)), 'proof': ((0, 1), (0, 1)),
         'reason': ((0, 1), (0, 1)), 'committer': ((0, 1), (0, 1)), 'committed': ((0, 1), (0, 1)), 'system_user': ((0, 1), (0, 1)),
         'location': ((0, 1), (0, 1)), 'performer': ((0, 1), (0, 1)), 'function': ((0, 1), (0, 1)), 'mode': ((0, 1), (0, 1)),
         'start': ((0, 1), (0, 1)), 'end': ((0, 1), (0, 1)), 'party_name': ((0, 1), (0, 1)), 'party_ref': ((0, 1), (0, 1)),
         'party_details': ((0, 1), (0, 1))}

    key = c.get(v[0])

    if key is None:
        raise ValueError("The requested setting; " + str(v[0]) + " is not a valid cardinality setting value.")
    else:
        if v[1][0] < c[v[0]][0][0] or v[1][0] > c[v[0]][0][1]:
            raise ValueError("The minimum occurences value for " + str(v) + "is out of range. The allowed values are " + str(c[v[0]][0]))
        if v[1][1] < c[v[0]][1][0] or v[1][1] > c[v[0]][1][1]:
            raise ValueError("The maximum occurences value for " + str(v) + "is out of range. The allowed values are " + str(c[v[0]][1]))
        return(True)

