"""Test utils for loading finance data."""
import os
import os.path as op
import shutil
import tempfile
from unittest import TestCase

from django.conf import settings
from django.core.management import call_command

# From django 1.10, django.test.utils https://docs.djangoproject.com/en/1.10/_modules/django/test/utils/
class TestContextDecorator(object):
    """
    A base class that can either be used as a context manager during tests
    or as a test function or unittest.TestCase subclass decorator to perform
    temporary alterations.

    `attr_name`: attribute assigned the return value of enable() if used as
                 a class decorator.

    `kwarg_name`: keyword argument passing the return value of enable() if
                  used as a function decorator.
    """
    def __init__(self, attr_name=None, kwarg_name=None):
        self.attr_name = attr_name
        self.kwarg_name = kwarg_name

    def enable(self):
        raise NotImplementedError

    def disable(self):
        raise NotImplementedError

    def __enter__(self):
        return self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def decorate_class(self, cls):
        if issubclass(cls, TestCase):
            decorated_setUp = cls.setUp
            decorated_tearDown = cls.tearDown

            def setUp(inner_self):
                context = self.enable()
                if self.attr_name:
                    setattr(inner_self, self.attr_name, context)
                decorated_setUp(inner_self)

            def tearDown(inner_self):
                decorated_tearDown(inner_self)
                self.disable()

            cls.setUp = setUp
            cls.tearDown = tearDown
            return cls
        raise TypeError('Can only decorate subclasses of unittest.TestCase')

    def decorate_callable(self, func):
        @wraps(func, assigned=available_attrs(func))
        def inner(*args, **kwargs):
            with self as context:
                if self.kwarg_name:
                    kwargs[self.kwarg_name] = context
                return func(*args, **kwargs)
        return inner

    def __call__(self, decorated):
        if isinstance(decorated, type):
            return self.decorate_class(decorated)
        elif callable(decorated):
            return self.decorate_callable(decorated)
        raise TypeError('Cannot decorate object of type %s' % type(decorated))


class with_form460A_data(TestContextDecorator):
    def __init__(self, *args, **kwargs):
        self.test_agency = kwargs.get('test_agency', 'CSD')
        self.test_year = kwargs.get('test_year', '2015')
        super(with_form460A_data, self).__init__()

    def enable(self):
        # Create a tempdir for netfile downloads
        self._saved_download_dir = getattr(settings, 'NETFILE_DOWNLOAD_DIR', None)
        settings.NETFILE_DOWNLOAD_DIR = tempfile.mkdtemp()

        # Copy test fixture data
        # TODO we silently don't do anything if we don't have fixture data for
        # the test agency. It would be better to accept a filename to the
        # fixture data so the test has full control over what it's setting up
        test_fixture_src = op.join(op.dirname(__file__), 'data', 'test_%s.csv' % self.test_agency)
        if op.exists(test_fixture_src):
            test_fixture_dst = op.join(settings.NETFILE_DOWNLOAD_DIR, 'csv', 'netfile_%s_%s_cal201_export.csv' % (self.test_year, self.test_agency))
            os.mkdir(op.dirname(test_fixture_dst))
            shutil.copyfile(test_fixture_src, test_fixture_dst)

        call_command('xformnetfilerawdata',
                     agencies=self.test_agency, years=self.test_year,
                     forms='A', verbosity=0)

    def disable(self):
        # Clean up tempdir and restore settings
        _t = settings.NETFILE_DOWNLOAD_DIR
        setattr(settings, 'NETFILE_DOWNLOAD_DIR', self._saved_download_dir)
        if self._saved_download_dir is None:
            del settings.NETFILE_DOWNLOAD_DIR

        shutil.rmtree(_t, True)
