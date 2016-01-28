import json
import os.path as op

from django.conf import settings
from django.test import TestCase


class CivicJsonTest(TestCase):

    def is_valid_civic_json(self, civic_json):

        # Test top-level keys
        good_keys = ('bornAt', 'categories', 'geography', 'needs',
                     'politicalEntity', 'status', 'tags', 'thumbnailUrl',
                     'type')
        self.assertTrue(len(set(civic_json.keys()) - set(good_keys)) == 0,
                        "Only recognized top-level keys")

        # Test top-level values are strings.
        for key in ('bornAt', 'geography', 'politicalEntity', 'status',
                    'thumbnailUrl', 'type'):
            self.assertTrue(isinstance(civic_json.get(key, ''), basestring),
                            "%s value is a string" % key)

        # Test top-level lists
        for key in ('tags',):
            self.assertTrue(isinstance(civic_json.get(key, []), list),
                            "%s is a list" % key)
            for ii, val in enumerate(civic_json.get(key, [])):
                self.assertTrue(isinstance(val, basestring),
                                "%s[%d] is a string" % (key, ii))

        # Test second-level objects
        for key_sing, key_plur in (('need', 'needs'),
                                   ('category', 'categories')):
            for ii, val in enumerate(civic_json.get(key_plur, {})):
                self.assertTrue(
                    key_sing in val and len(val) == 1,
                    "%s[%d] is a %s dict" % (key_plur, ii, key_sing))
                self.assertTrue(
                    isinstance(val[key_sing], basestring),
                    "%s[%d]['%s'] is a string" % (key_plur, ii, key_sing))

        return True

    def test_civic_json(self):
        """ Test civic.json"""
        json_path = op.join(settings.REPO_DIR, 'civic.json')
        self.assertTrue(op.exists(json_path), json_path)

        with open(json_path, 'r') as fp:
            civic_json = json.load(fp)
        self.assertTrue(self.is_valid_civic_json(civic_json))
