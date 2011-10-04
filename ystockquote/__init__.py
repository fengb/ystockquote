import operator
import warnings

from . import orig


_DIRECTIVES = [
    ('l1', 'price'),
    ('c1', 'change'),
    ('v' , 'volume'),
    ('a2', 'avg_daily_volume'),
    ('x' , 'stock_exchange'),
    ('j1', 'market_cap'),
    ('b4', 'book_value'),
    ('j4', 'ebitda'),
    ('d' , 'dividend_per_share'),
    ('y' , 'dividend_yield'),
    ('e' , 'earnings_per_share'),
    ('k' , '52_week_high'),
    ('j' , '52_week_low'),
    ('m3', '50day_moving_avg'),
    ('m4', '200day_moving_avg'),
    ('r' , 'price_earnings_ratio'),
    ('r5', 'price_earnings_growth_ratio'),
    ('p5', 'price_sales_ratio'),
    ('p6', 'price_book_ratio'),
    ('s7', 'short_ratio'),
]
_STATS = map(operator.itemgetter(0), _DIRECTIVES)
_FIELDS = map(operator.itemgetter(1), _DIRECTIVES)


def _get_no_cache(symbol):
    values = orig.__request(symbol, ''.join(_STATS)).split(',')
    data = {}
    for (i, field) in enumerate(_FIELDS):
        data[field] = values[i]

    return data


@deprecated
def get_all(symbol, cache={}):
    if symbol not in cache:
        cache[symbol] = _get_no_cache(symbol)

    return cache[symbol]


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


# FIXME: metaprogram evilness
for field in _FIELDS:
    # 'Simpler' implementation has wonky closure shadowing
    #func = lambda symbol: get_all(symbol)[field]
    # DOUBLE YOU TEE EFF: http://lackingrhoticity.blogspot.com/2009/04/python-variable-binding-semantics-part.html#c5923214396394060839
    func = (lambda field: lambda symbol: get_all(symbol)[field].strip('"'))(field)
    func = deprecated(func)

    func.__name__ = 'get_' + field
    locals()[func.__name__] = func
