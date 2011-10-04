import ystockquote
from ystockquote import legacy, compat as impr


def pytest_generate_tests(metafunc):
    # called once per each test function
    for funcargs in metafunc.cls.params[metafunc.function.__name__]:
        # schedule a new test function run with applied **funcargs
        metafunc.addcall(funcargs=funcargs)


# FIXME: there has to be a better way of getting the module API
API_NAMES = [f for f in dir(legacy) if not f.startswith('_')
                                    and callable(getattr(legacy, f))
                                    and getattr(legacy, f).__module__ == legacy.__name__]


class TestApiConsistency(object):
    params = {
        'test_equals': [{'func_name': n} for n in API_NAMES]
    }


    def test_equals(self, func_name):
        legacy_func = getattr(legacy, func_name)
        impr_func = getattr(impr, func_name)
        assert impr_func('KO') == legacy_func('KO')
