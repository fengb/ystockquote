import ystockquote
from ystockquote import orig


def pytest_generate_tests(metafunc):
    # called once per each test function
    for funcargs in metafunc.cls.params[metafunc.function.__name__]:
        # schedule a new test function run with applied **funcargs
        metafunc.addcall(funcargs=funcargs)


# FIXME: there has to be a better way of getting the module API
API_NAMES = [f for f in dir(orig) if not f.startswith('_')
                                  and callable(getattr(orig, f))
                                  and getattr(orig, f).__module__ == orig.__name__]


class TestApiConsistency(object):
    params = {
        'test_equals': [{'func_name': n} for n in API_NAMES]
    }


    def test_equals(self, func_name):
        orig_func = getattr(orig, func_name)
        impr_func = getattr(ystockquote, func_name)
        assert impr_func('KO') == orig_func('KO')
