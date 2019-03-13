import unittest
import pydictchecker.config.global_config as config
from pydictchecker.dynamic_operator import DynamicOperation


class DynamicOperatorTest(unittest.TestCase):

    def test_compare(self):

        self.assertTrue(DynamicOperation.compare(2, '==', 2))

        self.assertFalse(DynamicOperation.compare(2, '==', 3))

        self.assertTrue(DynamicOperation.compare('2', '<', 3, ':int:'))

        self.assertFalse(DynamicOperation.compare(None, '<', 3, ':int:'))

        self.assertFalse(DynamicOperation.compare('', '==', 3, ':int:'))

        self.assertTrue(DynamicOperation.compare('', '==', ''))

        self.assertTrue(DynamicOperation.compare(None, '==', None))

        self.assertTrue(DynamicOperation.compare(True, '!=', False))

        self.assertTrue(DynamicOperation.compare(True, '==', True))

        try:
            DynamicOperation.compare(2, '$$', 3)
        except Exception:
            self.assertTrue(True, 'Exception is expected because the comparator is not valid')

        try:
            DynamicOperation.compare('2', '<', 3, ':johnny:')
        except Exception:
            self.assertTrue(True, 'Exception is expected because the cast_to is not valid')

if __name__ == '__main__':
    unittest.main()
